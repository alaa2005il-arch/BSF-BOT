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
    return "BSF Discord BOT is Running! ♾️🔥"

@bot.event
async def on_ready():
    print(f"BSF شغال: {bot.user} ♾️")

@bot.command()
async def ping(ctx):
    await ctx.send("بوت BSF شغال! 🔥")

@bot.command()
async def bsf(ctx):
    await ctx.send("**BSF ♾️ - الهيبة مش بالكلام، الهيبة BSF** 🦁🐯👻")

@bot.event
async def on_message(message):
    if message.author
