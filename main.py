import discord
from discord.ext import commands
from discord.ui import View, Button
import random, os, json
from datetime import datetime
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "BSF BOT ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

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
    cm = int(diff.total_seconds() / 3600)
    return min(cm, 50)

class AjeebView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Challenge", style=discord.ButtonStyle.primary, emoji="⚡")
    async def btn1(self, interaction: discord.Interaction, button: Button):
        p = random.choice([800,1000,2000])
        await interaction.response.send_message(f"Power: {p}% for {interaction.user.mention}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ONLINE: {bot.user}')

@bot.tree.command(name="sh3ri", description="Check your hair length")
async def my_hair(interaction: discord.Interaction):
    length = get_length(interaction.user.id)
    if length == 0: status = "Bald shiny!"
    elif length < 5: status = "Nice and short"
    elif length < 10: status = "Needs cut soon"
    elif length < 20: status = "Long like palm tree!"
    else: status = "50cm! Go to barber!"
    embed = discord.Embed(title=f"Hair: {length} cm", description=status, color=0xFFD700)
    embed.add_field(name="Length", value=f"{length} cm", inline=True)
    embed.add_field(name="Cuts", value=str(hair_data[str(interaction.user.id)]["total_cuts"]), inline=True)
    if length >= 10:
        embed.add_field(name="Warning", value="Use /halaka", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="halaka", description="Cut someone hair")
async def halaka(interaction: discord.Interaction, member: discord.Member):
    uid = str(member.id)
    length = get_length(member.id)
    if length == 0:
        await interaction.response.send_message(f"{member.mention} already bald!")
        return
    styles = ["1000% POWER", "Lightning sides", "King style", "Zero with shine"]
    style = random.choice(styles)
    if uid not in hair_data: hair_data[uid] = {"last_cut": "", "total_cuts": 0}
    hair_data[uid]["last_cut"] = datetime.now().isoformat()
    hair_data[uid]["total_cuts"] = hair_data[uid].get("total_cuts", 0) + 1
    save_hair(hair_data)
    embed = discord.Embed(title="Haircut Done!", description=f"Barber: Ajeeb\nCustomer: {member.mention}\nWas: {length} cm\nNew: {style}", color=0x00FF00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mqamleen", description="Longest hair ranking")
async def longest(interaction: discord.Interaction):
    if not hair_data:
        await interaction.response.send_message("No hair data yet")
        return
    sorted_hair = sorted([(uid, get_length(uid)) for uid in hair_data], key=lambda x: x[1], reverse=True)[:5]
    text = ""
    for i, (uid, length) in enumerate(sorted_hair):
        try:
            member = await bot.fetch_user(int(uid))
            name = member.display_name
        except: name = f"User {uid[:4]}"
        text += f"{i+1}. {name} - {length} cm\n"
    embed = discord.Embed(title="Longest Hair Ranking", description=text, color=0xFF0000)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ajeeb", description="BSF hero")
async def ajeeb(interaction: discord.Interaction):
    embed = discord.Embed(title="Ajeeb Al-Sameen - 1000% POWER", description="Hero of Jericho found lamp under barber chair", color=0x0018A8)
    await interaction.response.send_message(embed=embed, view=AjeebView())

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
