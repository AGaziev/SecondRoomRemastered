import logging
import os
from pathlib import Path

from dotenv import load_dotenv

try:
    dotenv_path = os.path.join(Path(__file__).parent.parent, '.env')
    if not os.path.exists(dotenv_path):
        raise Exception('Switch to local machine env')
except Exception as e:
    logging.warning(e)
    dotenv_path = os.path.join(Path(__file__).parent.parent, '.env.local')
finally:
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        logging.info('all variables have loaded to env')
    else:
        logging.fatal('env file not found')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = os.getenv('DATABASE_PATH')
SHOP_CHANNEL_ID = os.getenv('SHOP_CHANNEL_ID')
USED_COMMANDS = ['/login', '/add']
