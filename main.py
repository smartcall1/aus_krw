import os
import requests
from datetime import datetime
import sys
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Naver's WAF silently drops requests lacking a browser-like User-Agent
# (especially from datacenter/CI IPs), which surfaces as a connect timeout
# rather than a clean 403. A realistic UA + Referer avoids that, and the
# retry adapter absorbs genuine transient network blips.
NAVER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; SM-G973N) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ),
    "Referer": "https://m.stock.naver.com/marketindex/home/exchange",
}

def _naver_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def get_naver_rate(reuters_code):
    url = "https://m.stock.naver.com/front-api/marketIndex/prices"
    params = {"category": "exchange", "reutersCode": reuters_code}
    session = _naver_session()
    response = session.get(url, params=params, headers=NAVER_HEADERS, timeout=10)

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

    return float(close_price.replace(",", ""))

def get_exchange_rate():
    try:
        aud = get_naver_rate("FX_AUDKRW")
        usd = get_naver_rate("FX_USDKRW")

        if aud is None or usd is None:
            return None

        return {
            "aud_krw": aud,
            "usd_krw": usd,
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
        message = f"{result['aud_krw']:.1f} 🇦🇺 / {result['usd_krw']:.1f} 🇺🇸"

        success = send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
        if not success:
            sys.exit(1)
    else:
        print("Failed to retrieve exchange rate.")
        sys.exit(1)

if __name__ == "__main__":
    main()