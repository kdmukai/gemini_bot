import requests
import json
import base64
import hmac
import hashlib
import datetime
import time
from decimal import Decimal



class GeminiRequestException(Exception):
    def __init__(self, status_code, response_json):
        self.status_code = status_code
        self.response_json = response_json
        super().__init__(json.dumps(self.response_json))



class GeminiApiConnection(object):

    def __init__(self, client_key: str, client_secret: str, sandbox: bool):
        self.client_key = client_key
        self.client_secret = client_secret.encode()
        self.sandbox = sandbox


    def _make_public_request(self, endpoint: str):
        base_url = "https://api.gemini.com/v1"
        if self.sandbox:
            base_url = "https://api.sandbox.gemini.com/v1"
        url = base_url + endpoint

        r = requests.get(url)

        if r.status_code == 200:
            return r.json()
        else:
            raise GeminiRequestException(r.status_code, r.json())


    def _make_authenticated_request(self, verb: str, endpoint: str, payload: dict = {}):
        base_url = "https://api.gemini.com/v1"
        if self.sandbox:
            base_url = "https://api.sandbox.gemini.com/v1"
        url = base_url + endpoint

        t = datetime.datetime.now()
        payload["nonce"] = str(int(time.mktime(t.timetuple())*1000))
        payload["request"] = "/v1" + endpoint

        encoded_payload = json.dumps(payload).encode()
        b64 = base64.b64encode(encoded_payload)
        signature = hmac.new(self.client_secret, b64, hashlib.sha384).hexdigest()

        request_headers = { 'Content-Type': "text/plain",
                            'Content-Length': "0",
                            'X-GEMINI-APIKEY': self.client_key,
                            'X-GEMINI-PAYLOAD': b64,
                            'X-GEMINI-SIGNATURE': signature,
                            'Cache-Control': "no-cache" }

        r = requests.post(url,
                          data=None,
                          headers=request_headers)

        if r.status_code == 200:
            return r.json()
        else:
            raise GeminiRequestException(r.status_code, r.json())


    """ **************************** Public Market Data **************************** """
    def symbol_details(self, market: str):
        """
            {
                'symbol': 'BTCUSD',
                'base_currency': 'BTC',
                'quote_currency': 'USD',
                'tick_size': 0.00000001,
                'quote_increment': 0.01,
                'min_order_size': '0.00001',
                'status': 'open'
            }
        """
        return self._make_public_request(f"/symbols/details/{market}")


    def current_order_book(self, market: str):
        """
            {
                "bids": [
                    {
                        "price": "3607.85",
                        "amount": "6.643373",
                        "timestamp": "1547147541"
                    },
                    ...,
                ],
                "asks": [
                    {
                        "price": "3607.86",
                        "amount": "14.68205084",
                        "timestamp": "1547147541"
                    },
                    ...,
                ]
            }
        """
        return self._make_public_request(f"/book/{market}")



    """ **************************** Authenticated Requests **************************** """
    def new_order(self, market: str, side: str, amount: Decimal, price: Decimal):
        if side not in ["buy", "sell"]:
            raise Exception(f"Invalid 'side': {side}")

        payload = {
            "symbol": market,
            "amount": str(amount),
            "price": str(price),
            "side": side,
            "type": "exchange limit",
            "options": ["maker-or-cancel"]  
        }
        return self._make_authenticated_request("POST", "/order/new", payload=payload)


    def order_status(self, order_id: str):
        payload = {
            "order_id": order_id,
            "include_trades": False,
        }
        return self._make_authenticated_request("POST", "/order/status", payload=payload)
