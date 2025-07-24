import os
import asyncio
from aiogram import Bot, Dispatcher, types
from flask import Flask, request

# === Настройки ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-bot.onrender.com
PORT = int(os.getenv("PORT", 10000))

# === Инициализация ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)

# === Обработчики команд ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Привет! Я работаю через webhook.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я — эхо-бот. Всё, что ты пишешь, я повторяю.")

# === Эхо-обработчик ===
@dp.message()
async def echo_message(message: types.Message):
    if message.text:
        await message.answer(f"💬 Ты написал: {message.text}")

# === Webhook endpoint (Telegram будет слать сюда обновления) ===
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = types.Update(**request.get_json())
    await dp.feed_update(bot, update)
    return {'status': 'ok'}

# === Главная страница (для UptimeRobot и проверки) ===
@app.route('/')
def home():
    return "✅ Бот работает через веб-сервер!"

# === Установка webhook при запуске ===
async def on_startup():
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"🟢 Webhook установлен: {webhook_url}")

# === Запуск сервера ===
def run():
    asyncio.run(on_startup())
    app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    run()
