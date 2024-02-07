import os
import json
import logging.config
import logging.handlers
import queue
import logging
import pathlib
import discord
from discord import app_commands
from src.utils.queue_handler import QueueHandler

LOGGER = logging.getLogger(__name__)


class BotConfig:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        # Create the logs directory if it doesn't exist
        os.makedirs("./logs", exist_ok=True)
        path = pathlib.Path(__file__).parent.parent / "logger.json"
        with open(path, "r") as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)

        # Create a queue for the logs
        self.log_queue = queue.Queue(-1)
        queue_handler = QueueHandler(self.log_queue)

        # Replace the handlers on your root logger with the custom QueueHandler
        root_logger = logging.getLogger()
        root_logger.handlers = [queue_handler]

    def get_client(self) -> discord.Client:
        """
        Create and return an instance of the bot with the desired prefix and intents

        Args:
            None

        Returns:
            discord.Client: An instance of the bot
        """
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(
            intents=intents,
            command_prefix='!'
        )

        self.cogs = []
        self.tree = app_commands.CommandTree(client)

        return client
