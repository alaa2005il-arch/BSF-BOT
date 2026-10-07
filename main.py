import discord
from discord.ext import commands
from discord.ui import View, Button
import random, os, json
from datetime import datetime
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "BSF MERGED OK"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

HAIR_FILE = "hair.json"
def load_hair():
    if os.path.exists(HAIR_FILE):
        try:
            with open(HAIR_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}
def save_hair(d):
    with open(HAIR_FILE, "w") as f: json.dump(d, f)
hair_data = load_hair()

def get_len(uid):
    uid=str(uid)
    if uid not in hair_data:
        hair_data[uid]={"last_cut":datetime.now().isoformat(),"cuts":0}
        save_hair(hair_data)
        return 0
    last=datetime.fromisoformat(hair_data[uid]["last_cut"])
    return min(int((datetime.now()-last).total_seconds()/3600),50)

class HelpView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Games", emoji="🎮", style=discord.ButtonStyle.primary)
    async def g(self, i: discord.Interaction, b: Button):
        await i.response.send_message("25+ games: xo, rps, etc", ephemeral=True)
    @discord.ui.button(label="Challenges", emoji="⚔️", style=discord.ButtonStyle.primary)
    async def c(self, i: discord.Interaction, b: Button):
        await i.response.send_message("Challenges: Ajeeb 1000% POWER", ephemeral=True)
    @discord.ui.button(label="Fun", emoji="🔥", style=discord.ButtonStyle.primary)
    async def f(self, i: discord.Interaction, b: Button):
        await i.response.send_message("Fun: jokes, memes, hair system!", ephemeral=True)
    @discord.ui.button(label="Main", emoji="🏠", style=discord.ButtonStyle.secondary, row=1)
    async def m(self, i: discord.Interaction, b: Button):
        e=discord.Embed(title="BSF KINGDOM", description="25+ games\n5 fun commands\nPremium features\n\nUse /help", color=0x0018A8)
        await i.response.send_message(embed=e, ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("ONLINE")

@bot.tree.command(name="help", description="BSF help menu")
async def help_cmd(interaction: discord.Interaction):
    embed=discord.Embed(title="BSF KINGDOM - Bot Ajeeb", description="All commands\nVote for bot\n\nFeatures\n• 25+ games\n• 5 fun commands\n• Premium", color=0x0018A8)
    await interaction.response.send_message(embed=embed, view=HelpView())

@bot.tree.command(name="sh3ri", description="Check hair")
async def sh3ri(interaction: discord.Interaction):
    l=get_len(interaction.user.id)
    s="Bald!" if l==0 else "Short" if l<5 else "Need cut" if l<10 else "Long like palm tree" if l<20 else "50cm!"
    e=discord.Embed(title=f"Hair: {l} cm", description=s, color=0xFFD700)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="halaka", description="Cut hair")
async def halaka(interaction: discord.Interaction, member: discord.Member):
    uid=str(member.id)
    l=get_len(member.id)
    if l==0:
        await interaction.response.send_message(f"{member.mention} already bald!")
        return
    if uid not in hair_data: hair_data[uid]={"last_cut":"", "cuts":0}
    hair_data[uid]["last_cut"]=datetime.now().isoformat()
    hair_data[uid]["cuts"]=hair_data[uid].get("cuts",0)+1
    save_hair(hair_data)
    e=discord.Embed(title="Haircut Done!", description=f"Barber: Ajeeb\nCustomer: {member.mention}\nWas: {l} cm", color=0x00FF00)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="mqamleen", description="Longest hair")
async def mqamleen(interaction: discord.Interaction):
    if not hair_data:
        await interaction.response.send_message("No data")
        return
    sorted_h=sorted([(u, get_len(u)) for u in hair_data], key=lambda x:x[1], reverse=True)[:5]
    txt=""
    for i,(u,ln) in enumerate(sorted_h):
        try:
            us=await bot.fetch_user(int(u))
            name=us.display_name
        except: name=u[:4]
        txt+=f"{i+1}. {name} - {ln} cm\n"
    e=discord.Embed(title="Longest Hair", description=txt, color=0xFF0000)
    await interaction.response.send_message(embed=e)

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
