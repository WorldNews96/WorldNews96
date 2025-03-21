import os
import time
import feedparser
import logging
from telegram import Bot

# Настройки (замени своими данными)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен бота
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # ID канала (например, @news_channel)
RSS_FEED_URL = os.getenv("RSS_FEED_URL")  # Ссылка на RSS-ленту
CHECK_INTERVAL = 300  # Проверка новостей каждые 5 минут

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
posted_links = set()

def fetch_news():
    """Получает новости из RSS и отправляет в Telegram."""
    global posted_links
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries[:5]:  # Берём последние 5 новостей
        if entry.link not in posted_links:
            message = f"📰 *{entry.title}*\n{entry.link}"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
            posted_links.add(entry.link)
            logging.info(f"Отправлено: {entry.title}")

if __name__ == "__main__":
    logging.info("Бот запущен...")
    while True:
        fetch_news()
        time.sleep(CHECK_INTERVAL)
