import discord
from discord.ext import commands
from discord.ui import View, Button
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- نظام الأزرار ---
class ChallengeView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="⚔️ تحداني", style=discord.ButtonStyle.primary, emoji="⚡")
    async def challenge_btn(self, interaction: discord.Interaction, button: Button):
        power = random.choice([800, 1000, 1200, 1500, 2000])
        if power >= 1500:
            msg = f"💥 يا ساتر {interaction.user.mention} طلعلك **{power}% POWER** - هزمت عجيب السمين! صرت ملك اليوم 👑"
        else:
            msg = f"😂 {interaction.user.mention} قوتك **{power}%** - عجيب السمين ضحك عليك! جرب مرة تانية"
        await interaction.response.send_message(msg)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'BSF KINGDOM - عجيب السمين ONLINE: {bot.user}')

# --- الأوامر ---

@bot.tree.command(name="عجيب", description="قصة عجيب السمين - بطل BSF KINGDOM")
async def ajeeb(interaction: discord.Interaction):
    file = discord.File("ajeeb.png", filename="ajeeb.png") # حط صورة عجيب جنب الملف
    embed = discord.Embed(
        title="🪔 عجيب السمين - بطل BSF KINGDOM",
        description="**كان يا ما كان في أريحا...**\nشاب اسمه **عجيب السمين** لقى فانوس تحت كرسي الحلاقة 💈\nمسحو وطلع برق أزرق **1000% POWER** ⚡\nقال الجني: شبيك لبيك\nقال عجيب: بدي مملكة!\nومن يومها صار أسطورة المملكة 👑",
        color=0x0018A8
    )
    embed.set_thumbnail(url="attachment://ajeeb.png")
    embed.add_field(name="✂️ السلاح", value="المقص الذهبي", inline=True)
    embed.add_field(name="⚡ القوة", value="1000% POWER", inline=True)
    embed.add_field(name="🏰 اللقب", value="KING OF LIGHT
