from flask import Flask, render_template, request
from bot import BasicBot
import logging
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename="logs/bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

app = Flask(__name__)
bot = None

@app.route("/", methods=["GET", "POST"])
def index():
    global bot
    result = None
    if request.method == "POST":
        symbol = request.form["symbol"]
        side = request.form["side"]
        order_type = request.form["type"]
        quantity = float(request.form["quantity"])
        price = request.form.get("price")
        stop_price = request.form.get("stop_price")

        if price:
            price = float(price)
        if stop_price:
            stop_price = float(stop_price)

        if order_type == "STOP_MARKET":
            result = bot.place_stop_limit_order(symbol, side, quantity, stop_price)
        else:
            result = bot.place_order(symbol, side, order_type, quantity, price)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    from binance.client import Client
    try:
        # Sync system time with Binance server time manually
        temp_client = Client(API_KEY, API_SECRET)
        temp_client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        server_time = temp_client.futures_time()['serverTime']
        print(f"Binance server time: {server_time}")
    except Exception as e:
        print(f"[Warning] Could not sync server time: {e}")

    bot = BasicBot(API_KEY, API_SECRET)
    app.run(debug=True)


