import os, json, random, io
import discord
from discord.ext import commands
from discord.ui import View, Button
from PIL import Image, ImageDraw, ImageFont
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "BSF-BOT is Online!"
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive():
    Thread(target=run, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
GOLD = 0xFFD700

def create_bsf_frame(name="BSF", color_hex="#FFD700"):
    W, H = 960, 540
    img = Image.new("RGB", (W, H), "#0a0a0a")
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, W-8, H-8], outline=color_hex, width=6)
    font_big = ImageFont.load_default()
    draw.text((W//2, H//2), f"BSF {name} {color_hex}", font=font_big, fill="white", anchor="mm")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@bot.event
async def on_ready():
    print(f'{bot.user} ONLINE!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN"))

@bot.command(name="bsf")
async def bsf_cmd(ctx, *, name="Ajeeb"):
    buffer = create_bsf_frame(name, "#FFD700")
    await ctx.send(file=discord.File(buffer, f"BSF_{name}.png"))

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms BSF ONLINE!")

keep_alive()
bot.run(os.getenv("TOKEN"))
