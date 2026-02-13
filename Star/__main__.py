import os
import sys
import asyncio
import importlib
from threading import Thread

from flask import Flask
from pyrogram import idle

import config
from Star import LOGGER, StarX
from Star.modules import ALL_MODULES

app = Flask(__name__)


@app.route('/')
def home():
    return "✅ Bot is alive!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 2. Start the Pyrogram bot
async def start_bot():
    try:
        await StarX.start()
    except Exception as ex:
        LOGGER.exception("Failed to start Telegram client: %s", ex)
        sys.exit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Star.modules." + all_module)

    LOGGER.info(f"@{StarX.username} Started.")
    await idle()

if __name__ == '__main__':
    missing_vars = config.validate_required_config()
    if missing_vars:
        LOGGER.error(
            "Missing required environment variables: %s",
            ", ".join(missing_vars),
        )
        LOGGER.error(
            "Render pe BOT_TOKEN aur MONGO_URL set karo, fir service re-deploy karo."
        )
        sys.exit(1)

    Thread(target=run_flask, daemon=True).start()
    asyncio.get_event_loop().run_until_complete(start_bot())
