import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Kicer jalan!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo Met! Bot Kicer udah online dan nggak bakal mati lagi.")

@bot.message_handler(func=lambda m: True)
def balas(message):
    bot.reply_to(message, f"Kamu kirim: {message.text}")

def jalanin_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=jalanin_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
