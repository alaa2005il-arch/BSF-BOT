import discord, os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "OK"
def run(): app.run(host='0.0.0.0', port=10000)
Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"READY {bot.user}")

@bot.tree.command(name="help", description="help")
async def help_cmd(i: discord.Interaction):
    await i.response.send_message("BSF BOT شغال! جرب /sh3ri")

@bot.tree.command(name="sh3ri", description="hair")
async def sh3ri(i: discord.Interaction):
    await i.response.send_message(f"شعرك 10 سم يا {i.user.mention}")

bot.run(os.getenv("DISCORD_TOKEN"))
