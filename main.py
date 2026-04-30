import os
import logging
from logging.handlers import RotatingFileHandler
from sorter.watcher import SentinelWatcher

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(os.path.join(log_dir, "sentinel.log"), maxBytes=1000000, backupCount=3),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    sentinel = SentinelWatcher(config_file)
    sentinel.start()