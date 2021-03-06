import redis
import threading
class quote_cache:
    def __init__(self):
        self.load_env()
        self.r = redis.Redis(host=self.redis_host, port=self.redis_port)
        self.mutex = threading.Lock()

    def load_env(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        self.redis_host = os.environ.get("redis_host")
        self.redis_port = int(os.environ.get("redis_port"))

    def sanitize_byte_keys_and_vals(self, response):
        sanitized_dict = {}
        keys = response.keys()
        for key in keys:
            sanitized_dict[str(key, encoding="utf-8")] = str(response[key], encoding="utf-8")
        return sanitized_dict

    def cache_quote(self, data):
        stock_symbol = data["stock_symbol"]
        dollars = data["dollars"]
        cents = data["cents"]
        quote_time = data["quote_time"]
        cryptokey = data["cryptokey"]
        response = {}

        self.mutex.acquire()

        try:
            bool_result = self.r.hmset(stock_symbol, {"dollars": dollars, "cents": cents, "quote_time": quote_time, "cryptokey": cryptokey})
            if (bool_result):
                response["status"] = "SUCCESS"
            else:
                response["status"] = "ERROR"

        finally:
            self.mutex.release()

        return response

    def get_quote(self, stock_symbol):
        response = {"status": "ERROR"}
        response["data"] = self.sanitize_byte_keys_and_vals(self.r.hgetall(stock_symbol))
        if (response["data"] != None and len(response["data"]) != 0):
            response["status"] = "SUCCESS"
        return response