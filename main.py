import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import random, os, json
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "BSF - نظام الشعر شغال!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

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
    user_id = str(user_id)
    if user_id not in hair_data:
        hair_data[user_id] = {"last_cut": datetime.now().isoformat(), "total_cuts": 0}
        save_hair(hair_data)
        return 0
    
    last = datetime.fromisoformat(hair_data[user_id]["last_cut"])
    diff = datetime.now() - last
    # كل ساعة 1 سم بيطول
    cm = int(diff.total_seconds() / 3600)  # ساعة = 1 سم
    return min(cm, 50) # اقصى طول 50 سم

class AjeebView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="⚔️ تحداني", style=discord.ButtonStyle.primary, emoji="⚡")
    async def btn1(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f'⚡ {interaction.user.mention} قوتك {random.choice([800,1000,2000])}%')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ONLINE: {bot.user}')

# --- أمر شعري ---
@bot.tree.command(name="شعري", description="شوف طول شعرك الحالي 💇‍♂️")
async def my_hair(interaction: discord.Interaction):
    length = get_length(interaction.user.id)
    
    if length == 0:
        status = "قرعة بتلمع 🪔✨ نظيف!"
        emoji = "😎"
    elif length < 5:
        status = "خفيف ومرتب 😌"
        emoji = "💈"
    elif length < 10:
        status = "بدأ يطول، لازم حلاقة قريب ✂️"
        emoji = "😬"
    elif length < 20:
        status = "شعرك طويل! صرت زي شجرة نخيل أريحا 🌴😂"
        emoji = "🦁"
    else:
        status = "يا ساتر! شعرك 50 سم! عجيب بطردك من الصالون 😂🔥"
        emoji = "🧟‍♂️"

    embed = discord.Embed(title=f"{emoji} طول شعرك: {length} سم", description=f"**الحالة:** {status}", color=0xFFD700)
    embed.add_field(name="📏 الطول", value=f"{length} سم", inline=True)
    embed.add_field(name="✂️ حلاقاتك", value=f"{hair_data[str(interaction.user.id)]['total_cuts']}", inline=True)
    
    if length >= 10:
        embed.add_field(name="⚠️", value="لازم تحلق! استخدم `/حلاقة`", inline=False)
    
    await interaction.response.send_message(embed=embed)

# --- أمر حلاقة مطور ---
@bot.tree.command(name="حلاقة", description="احلق لحدا - بقص شعرو كلو 💈")
async def halaka(interaction: discord.Interaction, عضو: discord.Member):
    user_id = str(عضو.id)
    length = get_length(عضو.id)
    
    if length == 0:
        await interaction.response.send_message(f'😂 {عضو.mention} أصلع أصلا! شو بدك تحلق؟ {interaction.user.mention} بضحك عليك 💈')
        return

    قصات = ["قرعة 1000% POWER 🔥", "سوالف برق ⚡", "قصة الملوك 👑", "على الصفر ✨"]
    قصة = random.choice(قصات)

    # قص الشعر
    if user_id not in hair_data: hair_data[user_id] = {"last_cut": "", "total_cuts": 0}
    hair_data[user_id]["last_cut"] = datetime.now().isoformat()
    hair_data[user_id]["total_cuts"] = hair_data[user_id].get("total_cuts", 0) + 1
    save_hair(hair_data)

    embed = discord.Embed(
        title="💈 تمت الحلاقة بنجاح!",
        description=f"**الحلاق:** عجيب السمين 🪔\n**الزبون:** {عضو.mention}\n**كان طولو:** {length} سم\n**القصة الجديدة:** {قصة}",
        color=0x00FF00
    )
    embed.set_footer(text=f"حلاقة رقم {hair_data[user_id]['total_cuts']} • BSF KINGDOM")
    await interaction.response.send_message(embed=embed)

# --- ترتيب أطول شعر ---
@bot.tree.command(name="مقملين", description="مين أطول شعر في السيرفر 😂")
async def longest(interaction: discord.Interaction):
    if not hair_data:
        await interaction.response.send_message("لسا
