from binance.client import Client
import logging

class BasicBot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.client.API_URL = self.client.FUTURES_URL
        self.client._request_kwargs = {'timeout': 20}

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            order_data = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity,
                'recvWindow': 60000
            }
            if order_type.lower() == 'limit':
                order_data['price'] = price
                order_data['timeInForce'] = 'GTC'

            print(f"Order payload: {order_data}")
            order = self.client.futures_create_order(**order_data)
            logging.info(f"ORDER SUCCESS: {order}")
            return order

        except Exception as e:
            logging.error(f"ORDER FAILED: {str(e)}")
            print(f"ORDER ERROR: {str(e)}")
            return {'error': str(e)}

    def place_stop_limit_order(self, symbol, side, quantity, stop_price):
        try:
            order_data = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': 'STOP_MARKET',
                'stopPrice': stop_price,
                'quantity': quantity,
                'timeInForce': 'GTC',
                'recvWindow': 60000
            }
            print(f"Stop order payload: {order_data}")
            order = self.client.futures_create_order(**order_data)
            logging.info(f"STOP LIMIT ORDER SUCCESS: {order}")
            return order

        except Exception as e:
            logging.error(f"STOP LIMIT ORDER FAILED: {str(e)}")
            print(f"STOP ORDER ERROR: {str(e)}")
            return {'error': str(e)}
