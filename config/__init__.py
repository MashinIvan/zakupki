from config.config import Config
import logging


config = Config()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

logging.root.handlers = [
    logging.FileHandler("logs.log", mode="w"),
]
