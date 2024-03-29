from aiogram.utils import executor
from repositories.bot import dp
import datetime
import logging
from config.handlersRegistrar import registerAll

if __name__ == "__main__":
    async def on_startup(_):
        logging.info('Bot online! timestamp:' + str(datetime.datetime.now()))

    registerAll(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
