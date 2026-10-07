import discord
from discord.ext import commands
from discord.ui import View, Button
import random
import os
from flask import Flask
from threading import Thread

# --- كود الـ Render عشان ما يطفي (هاد اللي انمسح بالصورة) ---
app = Flask('')
@app.route('/')
def home():
    return "BSF-BOT is Online! BSF KINGDOM 1000% POWER"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- اعدادات البوت ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- زر التحدي ---
class ChallengeView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="⚔️ تحداني", style=discord.ButtonStyle.primary, emoji="⚡")
    async def challenge_btn(self, interaction: discord.Interaction, button: Button):
        power = random.choice([800, 1000, 1200, 1500, 2000])
        if power >= 1500:
            msg = f"💥 يا ساتر {interaction.user.mention} طلعلك **{power}% POWER** - هزمت عجيب السمين! 👑"
        else:
            msg = f"😂 {interaction.user.mention} قوتك **{power}%** - عجيب السمين ضحك عليك!"
        await interaction.response.send_message(msg)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'BSF KINGDOM ONLINE: {bot.user}')

# --- الأوامر اللي عملناها امبارح ---
@bot.tree.command(name="عجيب", description="قصة عجيب السمين - بطل BSF KINGDOM")
async def ajeeb(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🪔 عجيب السمين - بطل BSF KINGDOM",
        description=(
            "**كان يا ما كان في أريحا...**\n"
            "شاب اسمه **عجيب السمين** لقى فانوس سحري تحت كرسي الحلاقة 💈\n\n"
            "مسحو وطلع برق أزرق **1000% POWER** ⚡\n"
            "قال الجني: شبيك لبيك\n"
            "قال عجيب: بدي مملكة!\n\n"
            "ومن يومها صار أسطورة المملكة 👑💥"
        ),
        color=0x0018A8
    )
    embed.add_field(name="✂️ السلاح", value="المقص الذهبي", inline=True)
    embed.add_field(name="⚡ القوة", value="1000% POWER", inline=True)
    embed.add_field(name="🏰 اللقب", value="KING OF LIGHTNING", inline=True)
    embed.set_footer(text="اضغط تحداني وشوف اذا بتقدر تهزمو!")
    
    try:
        file = discord.File("ajeeb.png", filename="ajeeb.png")
        embed.set_thumbnail(url="attachment://ajeeb.png")
        await interaction.response.send_message(file=file, embed=embed, view=ChallengeView())
    except:
        await interaction.response.send_message(embed=embed, view=ChallengeView())

@bot.tree.command(name="قوة", description="شوف قوتك اليوم")
async def power_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(f'⚡ {interaction.user.mention} قوتك: **{random.choice([800,1000,1500,2000])}% POWER**')

@bot.tree.command(name="موسى", description="MUSA JUICE")
async def musa_cmd(interaction: discord.Interaction):
    await interaction.response.send_message('🧴 ION TONIC MUSA JUICE - 1000% POWER - FUELED BY BSF KINGDOM')

@bot.tree.command(name="تحدي", description="تحدي عشوائي من عجيب")
async def tahadi_cmd(interaction: discord.Interaction):
    q = random.choice(["شو لون برق الفانوس؟ أزرق", "وين لقى عجيب الفانوس؟ تحت الكرسي", "كم مقص بالشعار؟ 2"])
    await interaction.response.send_message(f'🔥 **تحدي عجيب:** {q}')

# --- التشغيل النهائي ---
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
