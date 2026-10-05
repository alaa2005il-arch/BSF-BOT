from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import os
import json

app = Flask(__name__)
@app.route('/')
def home():
    return "BSF ULTIMATE BOT ONLINE ♾️"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} Online!")

@bot.command()
async def bsf(ctx):
    await ctx.send("🔥 BSF BOT شغال 24/7 يا عطيب ♾️")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

keep_alive()
TOKEN = os.getenv('TOKEN') or os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)