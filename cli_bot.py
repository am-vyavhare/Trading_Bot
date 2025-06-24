# cli_bot.py
from bot import BasicBot
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

bot = BasicBot(API_KEY, API_SECRET)

def main():
    print("Welcome to Binance CLI Trading Bot")
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    order_type = input("Order Type (MARKET / LIMIT / STOP_MARKET): ").upper()
    quantity = float(input("Quantity: "))

    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = float(input("Enter Limit Price: "))
        result = bot.place_order(symbol, side, order_type, quantity, price)
    elif order_type == "STOP_MARKET":
        stop_price = float(input("Enter Stop Price: "))
        result = bot.place_stop_limit_order(symbol, side, quantity, stop_price)
    else:
        result = bot.place_order(symbol, side, order_type, quantity)

    print("Order Response:")
    print(result)

if __name__ == "__main__":
    main()
