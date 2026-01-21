from main import get_exchange_rate
import sys

print("Checking KRW/AUD exchange rate...")
try:
    rate = get_exchange_rate()
    if rate:
        print(f"Success! Current Rate: 1 AUD = {rate:.2f} KRW")
    else:
        print("Failed to fetch rate. (Returned None)")
except Exception as e:
    print(f"An error occurred: {e}")
