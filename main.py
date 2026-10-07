import discord
from discord.ext import commands
from discord.ui import View, Button
import random, os, json
from datetime import datetime
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "BSF OK"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

FILE = "hair.json"
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(d):
    with open(FILE, "w") as f:
        json.dump(d, f)

hair = load_data()

def get_len(uid):
    uid = str(uid)
    if uid not in hair:
        hair[uid] = {"last": datetime.now().isoformat(), "cuts": 0}
        save_data(hair)
        return 0
    last = datetime.fromisoformat(hair[uid]["last"])
    diff = datetime.now() - last
    return min(int(diff.total_seconds() / 3600), 50)

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Games", style=discord.ButtonStyle.primary)
    async def b1(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("25+ games available", ephemeral=True)
    @discord.ui.button(label="Challenges", style=discord.ButtonStyle.primary)
    async def b2(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Challenges system", ephemeral=True)
    @discord.ui.button(label="Fun", style=discord.ButtonStyle.primary)
    async def b3(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Fun commands + hair system", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Online {bot.user}")

@bot.tree.command(name="help", description="help menu")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="BSF KINGDOM", description="All Commands\n25+ games\n5 fun commands", color=0x0018A8)
    await interaction.response.send_message(embed=embed, view=HelpView())

@bot.tree.command(name="sh3ri", description="check hair")
async def sh3ri(interaction: discord.Interaction):
    l = get_len(interaction.user.id)
    await interaction.response.send_message(f"Hair: {l} cm")

@bot.tree.command(name="halaka", description="cut hair")
async def halaka(interaction: discord.Interaction, member: discord.Member):
    uid = str(member.id)
    l = get_len(member.id)
    if l == 0:
        await interaction.response.send_message(f"{member.mention} bald already")
        return
    if uid not in hair:
        hair[uid] = {"last": "", "cuts": 0}
    hair[uid]["last"] = datetime.now().isoformat()
    hair[uid]["cuts"] = hair[uid].get("cuts", 0) + 1
    save_data(hair)
    await interaction.response.send_message(f"Cut done for {member.mention} - was {l} cm")

@bot.tree.command(name="mqamleen", description="longest hair")
async def mqamleen(interaction: discord.Interaction):
    if not hair:
        await interaction.response.send_message("No data yet")
        return
    sorted_h = sorted([(u, get_len(u)) for u in hair], key=lambda x: x[1], reverse=True)[:5]
    txt = ""
    for i, (u, ln) in enumerate(sorted_h):
        txt += f"{i+1}. User {u[:4]} - {ln} cm\n"
    await interaction.response.send_message(txt)

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
