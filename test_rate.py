from main import get_exchange_rate
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("Checking KRW/AUD exchange rate...")
try:
    rates = get_exchange_rate()
    if rates:
        print(f"Success! {rates['aud_krw']:.1f} 🇦🇺 / {rates['usd_krw']:.1f} 🇺🇸")
    else:
        print("Failed to fetch rates. (Returned None)")
except Exception as e:
    print(f"An error occurred: {e}")
