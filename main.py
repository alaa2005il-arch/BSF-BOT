import os
import json
import random
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord.ui import View, Button

app = Flask(__name__)
@app.route('/')
def home():
    return "BSF ULTIMATE BOT ONLINE ♾️"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

GOLD = 0xFFD700
BLACK = 0x0A0A0A
CYAN = 0x00FFFF

LEVEL_FILE = "bsf_levels.json"
def load_levels():
    try:
        with open(LEVEL_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}
def save_levels(data):
    with open(LEVEL_FILE, 'w') as f:
        json.dump(data, f)

BSF_QUOTES = ["الهيبة مش بالكلام، الهيبة BSF ♾️", "أسود وذهبي، هذا ستايلنا 👑", "الغامض ما بينكشف.. BSF ما بتنهزم"]

class BSFView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="🦁 قوانين BSF", style=discord.ButtonStyle.secondary, custom_id="rules"))
        self.add_item(Button(label="👑 طلب انضمام", style=discord.ButtonStyle.success, custom_id="join"))
        self.add_item(Button(label="💬 شات الكلان", style=discord.ButtonStyle.primary, custom_id="chat"))

@bot.event
async def on_ready():
    print(f'{bot.user} - BSF ULTIMATE شغال!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN ♾️ | !bsf"))

# ... كل اوامرك القديمة موجودة هون !bsf !اعضاء !فريم !لفل !توب !اقتباس !روليت !موشي !عجيب ...

@bot.command(name='bsf')
async def bsf_ultimate(ctx):
    embed = discord.Embed(title="🦁 BSF ULTIMATE PANEL ♾️", description="TWO BROTHERS BROTHERHOOD", color=GOLD)
    embed.add_field(name="🔥 الأوامر", value="`!اعضاء` `!فريم` `!لفل` `!موشي` `!عجيب` `!اقتباس` `!توب` `!بنر` `!روليت`", inline=False)
    await ctx.send(embed=embed, view=BSFView())

@bot.command(name='اعضاء')
async def members_pro(ctx):
    embed = discord.Embed(title="👑 مجلس BSF الأعلى ♾️", color=BLACK)
    members = [("🦁 أبو عيسى", "الزعيم"), ("🐯 عجيب", "المجنون"), ("👻 الغامض", "المؤسس"), ("🤓 موشي", "العبقري"), ("💤 موسى", "النايم"), ("♾️ MUSA", "اللامنتهي")]
    for name, desc in members:
        embed.add_field(name=name, value=desc, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='لفل')
async def level_pro(ctx, member: discord.Member = None):
    member = member or ctx.author
    levels = load_levels()
    data = levels.get(str(member.id), {"xp": 0, "level": 1})
    lvl = data["level"]; xp = data["xp"]; need = lvl * 100
    bar = "█" * int(xp/need*10) + "░" * (10 - int(xp/need*10))
    embed = discord.Embed(title=f"📊 {member.display_name} ♾️", color=CYAN)
    embed.add_field(name="Level", value=f"**{lvl}**", inline=True)
    embed.add_field(name="XP", value=f"{xp}/{need}", inline=True)
    embed.add_field(name="Progress", value=f"`{bar}`", inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    TOKEN = os.getenv('TOKEN') or os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
