import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BSF-BOT is Running! ♾️ by Alaa"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "أهلا يا علاء! البوت شغال ♾️🔥\nاكتب أي شي")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"وصل: {m.text}")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
