import os
import json
import random
import discord
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime

# BSF ULTIMATE BOT ♾️ - TWO BROTHERS BROTHERHOOD
# by موشي العبقري + الغامض - Fixed Version

# === إعداد الـ Intents الصح ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

GOLD = 0xFFD700
BLACK = 0x0A0A0A
CYAN = 0x00FFFF
RED_FIRE = 0xFF4500

LEVEL_FILE = "bsf_levels.json"

def load_levels():
    try:
        with open(LEVEL_FILE, 'r', encoding='utf-8') as f: 
            return json.load(f)
    except: 
        return {}

def save_levels(data):
    with open(LEVEL_FILE, 'w', encoding='utf-8') as f: 
        json.dump(data, f, ensure_ascii=False, indent=2)

BSF_QUOTES = [
    "الهيبة مش بالكلام، الهيبة BSF ♾️",
    "أسود وذهبي، هذا ستايلنا 👑",
    "الغامض ما بينكشف.. BSF ما بتنهزم",
    "عجيب أكل شاورما ورجع يجلد 🌯🐯",
    "موشي بيكود واحنا بنسيطر 🤓"
]

# === إصلاح نظام الأزرار ===
class BSFView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🦁 قوانين BSF", style=discord.ButtonStyle.secondary, custom_id="rules")
    async def rules_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📜 قوانين BSF ♾️",
            description="1️⃣ احترام الكل\n2️⃣ ممنوع السبام\n3️⃣ الهيبة فوق كل شي 👑\n4️⃣ أسود وذهبي للأبد",
            color=GOLD
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="👑 طلب انضمام", style=discord.ButtonStyle.success, custom_id="join")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="✅ تم استلام طلبك!",
            description=f"{interaction.user.mention} طلبك انضم لـ BSF وصل للإدارة ♾️\nانتظر أبو عيسى أو الغامض يوافق",
            color=CYAN
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="💬 شات الكلان", style=discord.ButtonStyle.primary, custom_id="chat")
    async def chat_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} روح على <#general> واحكي هيبتك 🔥", ephemeral=True)

@bot.event
async def on_ready():
    print(f'''
    ██████╗ ███████╗███████╗
    ██╔══██╗██╔════╝██╔════╝
    ██████╔╝███████╗███████╗ ♾️ BOT ONLINE
    ██╔══██╗╚════██║╚════██║
    ██████╔╝███████║███████║
    ╚═════╝ ╚══════╝╚══════╝
    {bot.user} - BSF ULTIMATE شغال!
    ''')
    # مهم جدا للأزرار الدائمة
    bot.add_view(BSFView())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN ♾️ | !bsf"))

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="ترحيب") or member.guild.system_channel
    if not channel: 
        return
    embed = discord.Embed(
        title=f"👑 أهلا {member.display_name} في BSF ♾️",
        description=f"نورت الكلان يا أسطورة!\n{random.choice(BSF_QUOTES)}\n\n**اقرأ القوانين وخذ رتبتك:**",
        color=GOLD
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"BSF | العضو رقم {member.guild.member_count}")
    try:
        await channel.send(embed=embed, view=BSFView())
    except Exception as e:
        print(f"خطأ في الترحيب: {e}")

@bot.event
async def on_message(message):
    if message.author.bot: 
        return
    # نظام XP تلقائي
    levels = load_levels()
    uid = str(message.author.id)
    if uid not in levels:
        levels[uid] = {"xp": 0, "level": 1}
    levels[uid]["xp"] += random.randint(5, 15)
    if levels[uid]["xp"] > levels[uid]["level"] * 100:
        levels[uid]["level"] += 1
        levels[uid]["xp"] = 0
        embed = discord.Embed(
            title="🎉 LEVEL UP! ♾️",
            description=f"{message.author.mention} وصل **لفل {levels[uid]['level']}**!\nهيبة BSF بتزيد 🔥",
            color=CYAN
        )
        await message.channel.send(embed=embed)
    save_levels(levels)
    await bot.process_commands(message)

# ===== الأوامر =====

@bot.command(name='bsf')
async def bsf_ultimate(ctx):
    embed = discord.Embed(
        title="🦁 BSF ULTIMATE PANEL ♾️",
        description="**TWO BROTHERS BROTHERHOOD - BLACK & GOLD EMPIRE**\n```ansi\n\u001b[2;33m♾️ BSF = هيبة لا تنتهي ♾️\u001b[0m\n```",
        color=GOLD
    )
    embed.add_field(name="🔥 الأوامر الأسطورية", value="`!اعضاء` `!فريم` `!لفل` `!موشي` `!عجيب` `!اقتباس` `!توب`", inline=False)
    embed.add_field(name="⚡ الجديد", value="`!بنر` - بنر 960x540 للسيرفر\n`!ترحيب` - رسالة ترحيب فخمة\n`!روليت` - لعبة حظ BSF", inline=False)
    embed.set_footer(text="Coded by موشي العبقري 👑 | Idea by الغامض 👻")
    await ctx.send(embed=embed, view=BSFView())

@bot.command(name='اعضاء')
async def members_pro(ctx):
    embed = discord.Embed(title="👑 مجلس BSF الأعلى ♾️", color=BLACK)
    embed.description = "```\nالطاقم الأسود الذهبي\n```"
    members = [
        ("🦁 أبو عيسى", "الزعيم - بدلة سودا ونظارة"),
        ("🐯 عجيب", "المجنون - سلاح وشاورما 🌯"),
        ("👻 الغامض", "المؤسس - هودي أسود وعيون زرقا"),
        ("🤓 موشي", "العبقري - print('BSF') + تاج"),
        ("💤 موسى", "النايم - Zzz أسطورة"),
        ("♾️ MUSA", "اللامنتهي - Circuit Gold"),
    ]
    for name, desc in members:
        embed.add_field(name=name, value=desc, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='فريم')
async def frame_pro(ctx, *, name="عجيب"):
    frames = {
        "عجيب": {"border": "ذهبي + نار تركواز", "text": "عجيب"},
        "موشي": {"border": "سايبر + تاج", "text": "موشي"},
        "MUSA": {"border": "circuit + cyan energy", "text": "MUSA - BSF ♾️"},
        "ابو عيسى": {"border": "ملكي فاخر", "text": "أبو عيسى 👑"},
    }
    f = frames.get(name, frames["عجيب"])
    embed = discord.Embed(
        title=f"🎨 FRAME: {f['text']} ♾️",
        description=f"**Border:** {f['border']}\n**Style:** Black gaming frame, luxury golden border, small cyan neon glow, fire corners\n**Status:** ✅ جاهز للاستخدام",
        color=GOLD
    )
    view = View()
    view.add_item(Button(label="⬇️ تحميل PNG", style=discord.ButtonStyle.success, custom_id="dl"))
    view.add_item(Button(label="🎨 تعديل الألوان", style=discord.ButtonStyle.primary, custom_id="edit"))
    await ctx.send(embed=embed, view=view)

@bot.command(name='لفل')
async def level_pro(ctx, member: discord.Member = None):
    member = member or ctx.author
    levels = load_levels()
    data = levels.get(str(member.id), {"xp": 0, "level": 1})
    lvl = data["level"]
    xp = data["xp"]
    need = lvl * 100
    bar = "█" * int(xp/need*10) + "░" * (10 - int(xp/need*10))
    
    embed = discord.Embed(title=f"📊 BSF CARD - {member.display_name} ♾️", color=CYAN)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Level", value=f"**{lvl}** 👑", inline=True)
    embed.add_field(name="XP", value=f"{xp}/{need}", inline=True)
    embed.add_field(name="Progress", value=f"`{bar}` {int(xp/need*100)}%", inline=False)
    embed.set_footer(text="BSF Level System | كل رسالة = XP")
    await ctx.send(embed=embed)

@bot.command(name='بنر')
async def banner(ctx):
    embed = discord.Embed(title="🖼️ BSF BANNER 960x540", description="البنر اللي سويناه: موشي على اليسار بيكود، لوجو BSF بالنص، موسى نايم وعجيب بالشاورما على اليمين، خلفية سودا وإطار ذهبي", color=GOLD)
    embed.add_field(name="المقاس", value="960x540 - جاهز للديسكورد", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='توب')
async def leaderboard(ctx):
    levels = load_levels()
    sorted_levels = sorted(levels.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:10]
    embed = discord.Embed(title="🏆 توب BSF - أكثر ناس هيبة ♾️", color=GOLD)
    text = ""
    for i, (uid, data) in enumerate(sorted_levels, 1):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.display_name
        except:
            name = f"User {uid[:4]}"
        text += f"**{i}.** {name} - لفل {data['level']} ({data['xp']} XP)\n"
    embed.description = text or "لسا ما حد كتب.. ابدأ انت!"
    await ctx.send(embed=embed)

@bot.command(name='اقتباس')
async def quote(ctx):
    q = random.choice(BSF_QUOTES)
    embed = discord.Embed(description=f"**\"{q}\"**", color=GOLD)
    embed.set_footer(text="BSF Wisdom ♾️")
    await ctx.send(embed=embed)

@bot.command(name='روليت')
async def roulette(ctx):
    result = random.choice(["🔥 فزت 100 XP!", "💀 خسرت.. عجيب أكل شاورماتك", "👑 جاك بونص ذهبي!", "👻 الغامض سرق نقاطك"])
    embed = discord.Embed(title="🎰 روليت BSF", description=result, color=random.choice([GOLD, CYAN, RED_FIRE]))
    await ctx.send(embed=embed)

@bot.command(name='موشي')
async def moshi_pro(ctx):
    embed = discord.Embed(
        title="🤓 موشي العبقري 👑",
        description="```py\nwhile True:\n    print('BSF ♾️')\n    code()\n    dominate()\n```",
        color=CYAN
    )
    await ctx.send(embed=embed)

@bot.command(name='عجيب')
async def ajib_pro(ctx):
    embed = discord.Embed(title="🐯 عجيب - وضع مجنون", description="🌯 + 🔫 = BSF STYLE", color=RED_FIRE)
    await ctx.send(embed=embed)

# تشغيل
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("❌ خطأ: ما لقيت TOKEN في متغيرات البيئة! حطه في .env أو في إعدادات الاستضافة")
else:
    bot.run(TOKEN)
