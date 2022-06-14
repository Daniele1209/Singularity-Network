from queue import Queue
from threading import Thread


class BlockChooser(Thread):
    def __init__(self, blockchain):
        super().__init__()
        self._chain = blockchain
        self._queue = Queue()

        self.__best_block = None
        self.__block_penalty = None
        self.__running = True

    def set_break(self):
        self.__running = False

    def set_best_block(self):
        self.__best_block = None

    # TODO
    def set_block_penalty(self):
        self.__block_penalty = None

    def add_block(self):
        if self.__best_block is not None:
            self._chain.process_block(self.__best_block)
        self.set_best_block()
        self.set_block_penalty()

    def scan_block(self, block):
        self._chain.validate_block(block)
        self._queue.put(item=block)

    def block_checker(self):
        try:
            block: Block = self._queue.get(timeout=1)
        except Exception:
            return
        current_block_penalty = self._chain.block_penalty(block)

        if self.__block_penalty is None or current_block_penalty < self.__block_penalty:
            self.__best_block = block
            self.__block_penalty = current_block_penalty

    def run(self):
        while self.__running:
            self.block_checker()
            self.add_block()
