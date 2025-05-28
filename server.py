from flask import Flask, request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

# Use your actual bot token environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Initialize Flask app
app = Flask(__name__)

@app.get("/")
def home():
    return "TON Payment Backend is running!"

@app.post("/telegram")
async def telegram_webhook():
    try:
        data = await request.get_json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        print(f"Error handling Telegram webhook: {e}")
        return {"ok": False}

# Optional: if you're also handling TON payment posts
@app.post("/webhook")
def ton_webhook():
    return {"ok": True}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080)
