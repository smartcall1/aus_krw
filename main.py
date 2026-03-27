import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
from dotenv import load_dotenv

def get_exchange_rate():
    try:
        url = "https://www.google.com/finance/quote/AUD-KRW"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"})
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Google Finance class for the exchange rate value
        rate_div = soup.find("div", {"class": "YMlKec fxKbKc"})
        
        if rate_div:
            # Remove any commas from the string and convert to float (e.g. "904.56")
            rate_str = rate_div.text.replace(",", "")
            return float(rate_str)
        else:
            print("Error: Could not find rate div on Google Finance.")
            return None
            
    except Exception as e:
        print(f"Error fetching exchange rate from Google: {e}")
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

    rate = get_exchange_rate()
    
    if rate:
        # Format the rate (e.g., 905.50)
        formatted_rate = f"{rate:.2f}"
        
        # Get current time (UTC) - GitHub Actions is usually UTC
        # If you want KST, you can adjust manually, but keeping it simple for now
        # Creating a nice message
        # Emoji flags: 🇦🇺 (AUD), 🇰🇷 (KRW)
        message = f"🇦🇺 1 AUD = 🇰🇷 <b>{formatted_rate} KRW</b>"
        
        success = send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
        if not success:
            sys.exit(1)
    else:
        print("Failed to retrieve exchange rate.")
        sys.exit(1)

if __name__ == "__main__":
    main()