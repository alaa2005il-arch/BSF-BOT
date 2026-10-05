import os
import threading
from flask import Flask
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def home():
    return "BSF BOT is Live!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"BSF BOT Online! Logged in as {bot.user}")

# حط كل الاوامر تبعتك هون

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(os.environ.get("DISCORD_TOKEN"))