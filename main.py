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
bot = commands.Bot(command_prefix='!', intents=intents)

# --- نظام الليفلات ---
def load_levels():
    try:
        with open("levels.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_levels(data):
    with open("levels.json", "w") as f:
        json.dump(data, f)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    levels = load_levels()
    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = {"xp": 0, "level": 1}
    
    levels[user_id]["xp"] += random.randint(5, 15)
    xp = levels[user_id]["xp"]
    lvl = levels[user_id]["level"]
    need = lvl * 100
    
    if xp >= need:
        levels[user_id]["level"] += 1
        levels[user_id]["xp"] = 0
        await message.channel.send(f"🎉 مبروك {message.author.mention} وصلت لفل **{levels[user_id]['level']}**!")
    
    save_levels(levels)
    await bot.process_commands(message)

# --- View للأزرار ---
class BSFView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="BSF", url="https://discord.gg/bsf"))

# --- الأوامر ---
@bot.command(name='bsf')
async def bsf_ultimate(ctx):
    embed = discord.Embed(title="🦁 BSF ULTIMATE", color=0xFFD700)
    embed.add_field(name="🔥 الأوامر", value="`!اعضاء` - مجلس الإدارة\n`!لفل` - شوف لفلك\n`!bsf` - قائمة الأوامر")
    await ctx.send(embed=embed, view=BSFView())

@bot.command(name='اعضاء')
async def members_pro(ctx):
    embed = discord.Embed(title="👑 مجلس BSF", color=0xFF0000)
    members = [("🦁 الزعيم", "أبو عيسى"), ("🐯 النائب", "فلان"), ("🦊 المستشار", "فلان")]
    for name, desc in members:
        embed.add_field(name=name, value=desc, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='لفل')
async def level_pro(ctx, member: discord.Member = None):
    member = member or ctx.author
    levels = load_levels()
    data = levels.get(str(member.id), {"xp": 0, "level": 1})
    lvl = data["level"]
    xp = data["xp"]
    need = lvl * 100
    
    progress = min(xp / need if need > 0 else 0, 1)
    bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
    
    embed = discord.Embed(title=f"📊 {member.display_name}", color=0x00FF00)
    embed.add_field(name="Level", value=f"**{lvl}**")
    embed.add_field(name="XP", value=f"{xp}/{need}")
    embed.add_field(name="Progress", value=f"`{bar}` {int(progress*100)}%")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    TOKEN = os.getenv('TOKEN') or os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
