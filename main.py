import os
import discord
from discord.ext import commands
import threading
from flask import Flask

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route('/')
def home():
    return "BSF Discord BOT is Running! 🟢"

@bot.event
async def on_ready():
    print(f"شغال: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("بوت BSF شغال! 🔥")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
