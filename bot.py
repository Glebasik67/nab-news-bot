
import os
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Токен Telegram-бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Функция для получения новостей с NBA.com
def get_nba_news():
    url = "https://www.nba.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("a", class_="ArticleTile_articleTitle__1ikvN")  # Класс заголовков
    if articles:
        latest_news = articles[0].text.strip()
        news_url = "https://www.nba.com" + articles[0]["href"]
        return latest_news, news_url
    return None, None

# Фоновая задача для проверки новостей
async def news_checker():
    last_news = None
    while True:
        news_title, news_url = get_nba_news()
        if news_title and news_title != last_news:
            last_news = news_title
            await bot.send_message(chat_id=os.getenv("YOUR_TELEGRAM_CHAT_ID"),
                                   text=f"📢 Новая новость NBA:
{news_title}
🔗 {news_url}")
        await asyncio.sleep(300)  # Проверяем каждые 5 минут

# Обрабатываем команду /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я буду присылать тебе свежие новости NBA!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_checker())  # Запускаем проверку новостей
    executor.start_polling(dp, skip_updates=True)
