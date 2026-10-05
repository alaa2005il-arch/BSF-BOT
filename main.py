import os
import json
import random
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord.ui import View, Button

# ===== Flask for Render =====
app = Flask(__name__)
@app.route('/')
def home():
    return "BSF BOT is Live! ♾️"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='+', intents=intents)
GOLD = 0xFFD700
BLACK = 0x0A0A0A
CYAN = 0x00FFFF
RED_FIRE = 0xFF4500

LEVEL_FILE = "bsf_levels.json"
def load_levels():
    try:
        with open(LEVEL_FILE, 'r') as f: return json.load(f)
    except: return {}
def save_levels(data):
    with open(LEVEL_FILE, 'w') as f: json.dump(data, f)

BSF_QUOTES = [
    "الهيبة مش بالكلام، الهيبة BSF ♾️",
    "أسود وذهبي، هذا ستايلنا 👑",
    "الغامض ما بينكشف.. BSF ما بتنهزم",
    "عجيب أكل شاورما ورجع يجلد 🌯🐯",
    "موشي بيكود واحنا بنسيطر 🤓"
]

class BSFView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="🦁 قوانين BSF", style=discord.ButtonStyle.secondary, custom_id="rules"))
        self.add_item(Button(label="👑 طلب انضمام", style=discord.ButtonStyle.success, custom_id="join"))
        self.add_item(Button(label="💬 شات الكلان", style=discord.ButtonStyle.primary, custom_id="chat"))

@bot.event
async def on_ready():
    print(f'{bot.user} - BSF ULTIMATE شغال! ♾️')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN ♾️ |!bsf"))

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="ترحيب") or member.guild.system_channel
    if not channel: return
    embed = discord.Embed(title=f"👑 أهلا {member.display_name} في BSF ♾️", description=f"نورت الكلان يا أسطورة!\n{random.choice(BSF_QUOTES)}", color=GOLD)
    embed.set_thumbnail(url=member.display_avatar.url)
    await channel.send(embed=embed, view=BSFView())

@bot.event
async def on_message(message):
    if message.author.bot: return
    levels = load_levels()
    uid = str(message.author.id)
    if uid not in levels: levels[uid] = {"xp": 0, "level": 1}
    levels[uid]["xp"] += random.randint(5, 15)
    if levels[uid]["xp"] > levels[uid]["level"] * 100:
        levels[uid]["level"] += 1
        levels[uid]["xp"] = 0
        embed = discord.Embed(title="🎉 LEVEL UP! ♾️", description=f"{message.author.mention} وصل **لفل {levels[uid]['level']}**!", color=CYAN)
        await message.channel.send(embed=embed)
    save_levels(levels)
    await bot.process_commands(message)

@bot.command(name='bsf')
async def bsf_ultimate(ctx):
    embed = discord.Embed(title="🦁 BSF ULTIMATE PANEL ♾️", description="**TWO BROTHERS BROTHERHOOD**", color=GOLD)
    embed.add_field(name="🔥 الأوامر", value="`!اعضاء` `!فريم` `!لفل` `!موشي` `!عجيب` `!اقتباس` `!توب`", inline=False)
    await ctx.send(embed=embed, view=BSFView())

@bot.command(name='اعضاء')
async def members_pro(ctx):
    embed = discord.Embed(title="👑 مجلس BSF الأعلى ♾️", color=BLACK)
    members = [("🦁 أبو عيسى", "الزعيم"), ("🐯 عجيب", "المجنون 🌯"), ("👻 الغامض", "المؤسس"), ("🤓 موشي", "العبقري"), ("💤 موسى", "النايم"), ("♾️ MUSA", "اللامنتهي")]
    for name, desc in members: embed.add_field(name=name, value=desc, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='فريم')
async def frame_pro(ctx, *, name="عجيب"):
    embed = discord.Embed(title=f"🎨 FRAME: {name} ♾️", description="Black gaming frame, golden border, cyan glow", color=GOLD)
    await ctx.send(embed=embed)

@bot.command(name='لفل')
async def level_pro(ctx, member: discord.Member = None):
    member = member or ctx.author
    levels = load_levels()
    data = levels.get(str(member.id), {"xp": 0, "level": 1})
    embed = discord.Embed(title=f"📊 {member.display_name} ♾️", color=CYAN)
    embed.add_field(name="Level", value=str(data["level"]))
    embed.add_field(name="XP", value=str(data["xp"]))
    await ctx.send(embed=embed)

@bot.command(name='توب')
async def leaderboard(ctx):
    levels = load_levels()
    sorted_levels = sorted(levels.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:10]
    embed = discord.Embed(title="🏆 توب BSF ♾️", color=GOLD)
    text = ""
    for i, (uid, data) in enumerate(sorted_levels, 1):
        text += f"**{i}.** {uid[:4]} - لفل {data['level']}\n"
    embed.description = text or "لسا ما حد كتب"
    await ctx.send(embed=embed)

@bot.command(name='اقتباس')
async def quote(ctx):
    await ctx.send(embed=discord.Embed(description=random.choice(BSF_QUOTES), color=GOLD))

@bot.command(name='روليت')
async def roulette(ctx):
    result = random.choice(["🔥 فزت 100 XP!", "💀 خسرت..", "👑 بونص ذهبي!", "👻 الغامض سرق نقاطك"])
    await ctx.send(embed=discord.Embed(title="🎰 روليت BSF", description=result, color=GOLD))

@bot.command(name='موشي')
async def moshi_pro(ctx):
    await ctx.send(embed=discord.Embed(title="🤓 موشي العبقري 👑", description="while True:\n print('BSF ♾️')", color=CYAN))

@bot.command(name='عجيب')
async def ajib_pro(ctx):
    await ctx.send(embed=discord.Embed(title="🐯 عجيب", description="🌯 + 🔫 = BSF STYLE", color=RED_FIRE))
if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        token = os.environ.get("TOKEN")
    print(f"TOKEN EXISTS: {bool(token)}")
    if not token:
        print("NO TOKEN FOUND!")
        import time
        while True:
            time.sleep(60)
    print("Starting bot...")
    bot.run(token)
