# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.ui import View, Button
import random, os, json
from datetime import datetime
from flask import Flask
from threading import Thread

# --- موقع ---
app = Flask('')
@app.route('/')
def home(): return "BSF BOT - MERGED ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# --- نظام الشعر ---
HAIR_FILE = "hair.json"
def load_hair():
    if os.path.exists(HAIR_FILE):
        try:
            with open(HAIR_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}
def save_hair(data):
    with open(HAIR_FILE, "w") as f: json.dump(data, f)
hair_data = load_hair()

def get_length(user_id):
    uid = str(user_id)
    if uid not in hair_data:
        hair_data[uid] = {"last_cut": datetime.now().isoformat(), "total_cuts": 0}
        save_hair(hair_data)
        return 0
    last = datetime.fromisoformat(hair_data[uid]["last_cut"])
    diff = datetime.now() - last
    cm = int(diff.total_seconds() / 3600) # كل ساعة 1 سم
    return min(cm, 50)

# --- View القديم اللي بالصورة ---
class MainHelpView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ألعاب", style=discord.ButtonStyle.primary, emoji="🎮")
    async def games(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="🎮 ألعاب - أكثر من 25 لعبة", description="xo - حجر ورقة مقص - فكك - اكس او - صراحة - لو خيروك - كتابة - سرعة - وغيرهم كثير", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="تحديات", style=discord.ButtonStyle.primary, emoji="
