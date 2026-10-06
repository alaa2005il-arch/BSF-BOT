import os
import json
import random
import io
import discord
from discord.ext import commands
from discord.ui import View, Button
from PIL import Image, ImageDraw, ImageFont
from flask import Flask
from threading import Thread

# ========== Keep Alive (عشان Render ما يطفيه) ==========
app = Flask('')

@app.route('/')
def home():
    return "BSF-BOT is Online! ♾️🔥"

def run():
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()

# ========== اعداد البوت ==========
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

GOLD = 0xFFD700
BLACK = 0x0A0A0A
CYAN = 0x00FFFF

COLORS_HEX = {
    "ذهبي": "#FFD700",
    "تركواز": "#40E0D0",
    "احمر": "#FF2D2D"
}

LEVEL_FILE = "bsf_levels.json"

def load_levels():
    try:
        with open(LEVEL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_levels(data):
    with open(LEVEL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

BSF_QUOTES = [
    "الهيبة مش بالكلام، الهيبة BSF ♾️",
    "أسود وذهبي، هذا ستايلنا 👑",
    "الغامض ما بينكشف.. BSF ما بتنهزم",
    "عجيب أكل شاورما ورجع يجلد 🌯🐯",
    "موشي بيكود واحنا بنسيطر 🤓"
]

def create_bsf_frame(name="BSF ♾️", color_hex="#FFD700"):
    W, H = 960, 540
    img = Image.new("RGB", (W, H), "#0a0a0a")
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, W-8, H-8], outline=color_hex, width=6)
    draw.rectangle([22, 22, W-22, H-22], outline=color_hex, width=1)
    try:
        font_big = ImageFont.truetype("arial.ttf", 95)
        font_name = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_big = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_small = ImageFont.load_default()

    title = "BSF ♾️"
    bbox = draw.textbbox((0,0), title, font=font_big)
    draw.text(((W - (bbox[2]-bbox[0]))/2, 70), title, font=font_big, fill=color_hex)

    bbox2 = draw.textbbox((0,0), name, font=font_name)
    draw.text(((W - (bbox2[2]-bbox2[0]))/2, 240), name, font=font_name, fill="white")

    sub = f"BLACK & GOLD EMPIRE | {color_hex}"
    bbox3 = draw.textbbox((0,0), sub, font=font_small)
    draw.text(((W - (bbox3[2]-bbox3[0]))/2, 350), sub, font=font_small, fill="#888888")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

class ColorPickerView(View):
    def __init__(self, target_name="عجيب"):
        super().__init__(timeout=None)
        self.target_name = target_name

    @discord.ui.button(label="ذهبي", style=discord.ButtonStyle.secondary, custom_id="color_gold", emoji="🟡")
    async def gold_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["ذهبي"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_GOLD.png"), ephemeral=True)

    @discord.ui.button(label="تركواز", style=discord.ButtonStyle.secondary, custom_id="color_turquoise", emoji="🟢")
    async def turq_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["تركواز"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_TURQ.png"), ephemeral=True)

    @discord.ui.button(label="احمر", style=discord.ButtonStyle.secondary, custom_id="color_red", emoji="🔴")
    async def red_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["احمر"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_RED.png"), ephemeral=True)

class FrameDownloadView(View):
    def __init__(self, target_name="عجيب"):
        super().__init__(timeout=None)
        self.target_name = target_name

    @discord.ui.button(label="⬇️ تحميل PNG", style=discord.ButtonStyle.success, custom_id="dl_png_real")
    async def download_png(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["ذهبي"])
        await interaction.followup.send(content=f"تفضل فريم **{self.target_name}** ♾️", file=discord.File(buffer, f"BSF_{self.target_name}.png"), ephemeral=True)

    @discord.ui.button(label="🎨 تعديل الألوان", style=discord.ButtonStyle.primary, custom_id="edit_colors_real")
    async def edit_colors(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"اختار لون لفريم **{self.target_name}**:", view=ColorPickerView(self.target_name), ephemeral=True)

class BSFView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🦁 قوانين BSF", style=discord.ButtonStyle.secondary, custom_id="rules")
    async def rules_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="📜 قوانين BSF ♾️", description="1️⃣ احترام الكل\n2️⃣ ممنوع السبام\n3️⃣ الهيبة فوق كل شي 👑\n4️⃣ أسود وذهبي للأبد", color=GOLD)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="👑 طلب انضمام", style=discord.ButtonStyle.success, custom_id="join")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="✅ تم استلام طلبك!", description=f"{interaction.user.mention} طلبك انضم لـ BSF وصل للإدارة ♾️", color=CYAN)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="💬 شات الكلان", style=discord.ButtonStyle.primary, custom_id="chat")
    async def chat_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} روح على <#general> واحكي هيبتك 🔥", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} - BSF ULTIMATE شغال!')
    bot.add_view(BSFView())
    bot.add_view(ColorPickerView())
    bot.add_view(FrameDownloadView())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN ♾️ |!bsf"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # نظام ليفلات بسيط
    data = load_levels()
    uid = str(message.author.id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 0}
    data[uid]["xp"] += 5
    if data[uid]["xp"] >= (data[uid]["level"]+1)*100:
        data[uid]["level"] += 1
        await message.channel.send(f"🔥 {message.author.mention} وصل ليفل **{data[uid]['level']}** في BSF ♾️!")
    save_levels(data)
    await bot.process_commands(message)

@bot.command(name="bsf")
async def bsf_cmd(ctx, *, name="عجيب"):
