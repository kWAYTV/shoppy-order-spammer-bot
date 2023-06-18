import asyncio
from queue import Queue
from src.util.logger import Logger
from src.shoppy.spammer import Spammer
from concurrent.futures import ThreadPoolExecutor

class QueueHandler:
    def __init__(self):
        self.queue = Queue()
        self.spammer = Spammer()
        self.logger = Logger()
        self.proccessing = False

    # Pushes an order to the queue
    def push_order(self, order):
        self.queue.put(order)

    # Returns the queue length
    def get_queue_length(self):
        return self.queue.qsize()

    # Returns the queue data as a list
    def get_queue_data(self):
        return self.queue.queue

    # Processes the queue
    async def process_queue(self):
        try:
            while not self.queue.empty():
                self.proccessing = True
                order = self.queue.get()
                amount = order['amount']
                product_id = order['product_id']
                requested_by = order['requested_by']

                self.logger.log("INFO", f"Processing order from user {requested_by} for amout of {amount} to product: {product_id}.")

                # Use asyncio's run_in_executor to run blocking functions in a thread
                with ThreadPoolExecutor() as executor:
                    await asyncio.get_event_loop().run_in_executor(executor, self.spammer.start, amount, product_id)

                # Remove the completed order from the queue
                self.queue.task_done()
        except Exception as e:
            self.proccessing = False
            self.logger.log("ERROR", f"Error processing queue: {e}")

    # Checks if the queue is empty and if it's not empty nor being processed, processes it
    async def force_check_start(self):
        try:
            if not self.queue.empty() and not self.proccessing:
                await self.process_queue()
        except Exception as e:
            self.proccessing = False
            self.logger.log("ERROR", f"Error force-checking the queue: {e}")