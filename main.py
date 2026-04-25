import os
import requests
from datetime import datetime
import sys
from dotenv import load_dotenv

def get_exchange_rate():
    try:
        url = "https://open.er-api.com/v6/latest/AUD"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None

        data = response.json()
        if data.get("result") != "success":
            print(f"Error: API returned result={data.get('result')}")
            return None

        rates = data.get("rates", {})
        krw_rate = rates.get("KRW")
        usd_rate = rates.get("USD")
        if krw_rate is None or usd_rate is None:
            print("Error: KRW or USD rate not found in API response.")
            return None

        usd_krw = krw_rate / usd_rate
        return {"aud_krw": float(krw_rate), "usd_krw": float(usd_krw)}

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
        aud_krw = f"{result['aud_krw']:.2f}"
        usd_krw = f"{result['usd_krw']:.2f}"

        message = (
            f"🇦🇺 1 AUD = 🇰🇷 <b>{aud_krw} KRW</b>\n"
            f"🇺🇸 1 USD = 🇰🇷 <b>{usd_krw} KRW</b>"
        )

        success = send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
        if not success:
            sys.exit(1)
    else:
        print("Failed to retrieve exchange rate.")
        sys.exit(1)

if __name__ == "__main__":
    main()