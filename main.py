import os
import requests
from datetime import datetime
import sys
from dotenv import load_dotenv

def get_naver_rate(reuters_code):
    url = "https://m.stock.naver.com/front-api/marketIndex/prices"
    params = {"category": "exchange", "reutersCode": reuters_code}
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for {reuters_code}")
        return None

    data = response.json()
    if not data.get("isSuccess"):
        print(f"Error: Naver API returned failure for {reuters_code}: {data.get('message')}")
        return None

    result = data.get("result") or []
    if not result:
        print(f"Error: No rate data returned for {reuters_code}")
        return None

    close_price = result[0].get("closePrice")
    if close_price is None:
        print(f"Error: closePrice missing for {reuters_code}")
        return None

    fluctuations_ratio = result[0].get("fluctuationsRatio")
    if fluctuations_ratio is not None:
        # Naver ratio already carries "-" for falls but omits "+" for rises
        change_pct = f"{float(fluctuations_ratio):+.2f}%"
    else:
        change_pct = "N/A"

    return {
        "price": float(close_price.replace(",", "")),
        "change_pct": change_pct,
    }

def get_exchange_rate():
    try:
        aud = get_naver_rate("FX_AUDKRW")
        usd = get_naver_rate("FX_USDKRW")
        nzd = get_naver_rate("FX_NZDKRW")

        if aud is None or usd is None or nzd is None:
            return None

        return {
            "aud_krw": aud["price"], "aud_change": aud["change_pct"],
            "usd_krw": usd["price"], "usd_change": usd["change_pct"],
            "nzd_krw": nzd["price"], "nzd_change": nzd["change_pct"],
        }

    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
        return True
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return False
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def main():
    # Load secrets from .env file (if it exists)
    load_dotenv()

    # Load secrets from environment variables
    # These should be set in GitHub Actions Secrets or .env file
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_TOKEN or CHAT_ID environment variables are not set.")
        # Local test instructions
        print("For local test: Create a .env file or set export TELEGRAM_TOKEN='your_token' && export CHAT_ID='your_id'")
        sys.exit(1)

    result = get_exchange_rate()

    if result:
        aud_krw = f"{result['aud_krw']:,.2f}"
        usd_krw = f"{result['usd_krw']:,.2f}"
        nzd_krw = f"{result['nzd_krw']:,.2f}"

        separator = "\n────────────────────\n"
        message = separator.join([
            f"🇳🇿 1 NZD = 🇰🇷 <b>{nzd_krw} KRW</b> ({result['nzd_change']}, 24H)",
            f"🇦🇺 1 AUD = 🇰🇷 <b>{aud_krw} KRW</b> ({result['aud_change']}, 24H)",
            f"🇺🇸 1 USD = 🇰🇷 <b>{usd_krw} KRW</b> ({result['usd_change']}, 24H)",
        ])

        success = send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
        if not success:
            sys.exit(1)
    else:
        print("Failed to retrieve exchange rate.")
        sys.exit(1)

if __name__ == "__main__":
    main()