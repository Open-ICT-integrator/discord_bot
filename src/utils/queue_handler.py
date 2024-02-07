import logging.handlers
import atexit


class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue):
        super().__init__(queue)

        # Get the configured handlers
        queue_handler = logging.getLogger().handlers[0]

        self.listener = logging.handlers.QueueListener(queue, queue_handler)
        self.listener.start()
        atexit.register(self.listener.stop)
