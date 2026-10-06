import os
import json
import random
import io
import discord
from discord.ext import commands
from discord.ui import View, Button
from PIL import Image, ImageDraw, ImageFont

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

GOLD = 0xFFD700
BLACK = 0x0A0A0A
CYAN = 0x00FFFF

COLORS_HEX = {
    "ذهبي": "#FFD700",
    "تركواز": "#40E0D0",
    "احمر": "#FF2D2D"
}

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

def create_bsf_frame(name="BSF ♾️", color_hex="#FFD700"):
    W, H = 960, 540
    img = Image.new("RGB", (W, H), "#0a0a0a")
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, W-8, H-8], outline=color_hex, width=6)
    draw.rectangle([22, 22, W-22, H-22], outline=color_hex, width=1)
    try:
        font_big = ImageFont.truetype("arial.ttf", 95)
        font_name = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_big = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_small = ImageFont.load_default()

    title = "BSF ♾️"
    bbox = draw.textbbox((0,0), title, font=font_big)
    draw.text(((W - (bbox[2]-bbox[0]))/2, 70), title, font=font_big, fill=color_hex)

    bbox2 = draw.textbbox((0,0), name, font=font_name)
    draw.text(((W - (bbox2[2]-bbox2[0]))/2, 240), name, font=font_name, fill="white")

    sub = f"BLACK & GOLD EMPIRE | {color_hex}"
    bbox3 = draw.textbbox((0,0), sub, font=font_small)
    draw.text(((W - (bbox3[2]-bbox3[0]))/2, 350), sub, font=font_small, fill="#888888")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

class ColorPickerView(View):
    def __init__(self, target_name="عجيب"):
        super().__init__(timeout=None)
        self.target_name = target_name

    @discord.ui.button(label="ذهبي", style=discord.ButtonStyle.secondary, custom_id="color_gold", emoji="🟡")
    async def gold_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["ذهبي"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_GOLD.png"), ephemeral=True)

    @discord.ui.button(label="تركواز", style=discord.ButtonStyle.secondary, custom_id="color_turquoise", emoji="🟢")
    async def turq_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["تركواز"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_TURQ.png"), ephemeral=True)

    @discord.ui.button(label="احمر", style=discord.ButtonStyle.secondary, custom_id="color_red", emoji="🔴")
    async def red_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["احمر"])
        await interaction.followup.send(file=discord.File(buffer, f"BSF_{self.target_name}_RED.png"), ephemeral=True)

class FrameDownloadView(View):
    def __init__(self, target_name="عجيب"):
        super().__init__(timeout=None)
        self.target_name = target_name

    @discord.ui.button(label="⬇️ تحميل PNG", style=discord.ButtonStyle.success, custom_id="dl_png_real")
    async def download_png(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        buffer = create_bsf_frame(self.target_name, COLORS_HEX["ذهبي"])
        await interaction.followup.send(content=f"تفضل فريم **{self.target_name}** ♾️", file=discord.File(buffer, f"BSF_{self.target_name}.png"), ephemeral=True)

    @discord.ui.button(label="🎨 تعديل الألوان", style=discord.ButtonStyle.primary, custom_id="edit_colors_real")
    async def edit_colors(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"اختار لون لفريم **{self.target_name}**:", view=ColorPickerView(self.target_name), ephemeral=True)

class BSFView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🦁 قوانين BSF", style=discord.ButtonStyle.secondary, custom_id="rules")
    async def rules_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="📜 قوانين BSF ♾️", description="1️⃣ احترام الكل\n2️⃣ ممنوع السبام\n3️⃣ الهيبة فوق كل شي 👑\n4️⃣ أسود وذهبي للأبد", color=GOLD)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="👑 طلب انضمام", style=discord.ButtonStyle.success, custom_id="join")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="✅ تم استلام طلبك!", description=f"{interaction.user.mention} طلبك انضم لـ BSF وصل للإدارة ♾️", color=CYAN)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="💬 شات الكلان", style=discord.ButtonStyle.primary, custom_id="chat")
    async def chat_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} روح على <#general> واحكي هيبتك 🔥", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} - BSF ULTIMATE شغال!')
    # اصلاح: لازم بدون باراميترات عشان الازرار الدائمة
    bot.add_view(BSFView())
    bot.add_view(ColorPickerView())
    bot.add_view(FrameDownloadView())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BSF CLAN ♾️ |!bsf"))

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="ترحيب") or member.guild.system_channel
    if not channel: return
    embed = discord.Embed(title=f"👑 أهلا {member.display_name} في BSF ♾️", description=f"نورت الكلان!\n{random.choice(BSF_QUOTES)}", color=GOLD)
    embed.set_thumbnail(url=member.display_avatar.url)
    try:
        await channel.send(embed=embed, view=BSFView())
    except: pass

@bot.event
async def on_message(message):
    if message.author.bot: return
    levels = load_levels()
    uid = str(message.author.id)
    if uid not in levels: levels[uid] = {"xp": 0, "level": 1}
    levels[uid]["xp"] += random.randint(5, 15)
    if levels[uid]["xp"] > levels[uid]["level"] * 100:
        levels[uid]["level"] += 1
        levels[uid]["xp"] = 0
        embed = discord.Embed(title="🎉 LEVEL UP! ♾️", description=f"{message.author.mention} وصل **لفل {levels[uid]['level']}**!", color=CYAN)
        await message.channel.send(embed=embed)
    save_levels(levels)
    await bot.process_commands(message)

@bot.command(name='bsf')
async def bsf_ultimate(ctx):
    embed = discord.Embed(title="🦁 BSF ULTIMATE PANEL ♾️", description="**TWO BROTHERS BROTHERHOOD**\n```ansi\n\u001b[2;33m♾️ BSF = هيبة لا تنتهي ♾️\u001b[0m\n```", color=GOLD)
    embed.add_field(name="🔥 الأوامر", value="`!اعضاء` `!فريم` `!لفل` `!توب` `!اقتباس`", inline=False)
    await ctx.send(embed=embed, view=BSFView())

@bot.command(name='فريم')
async def frame_pro(ctx, *, name="عجيب"):
    embed = discord.Embed(title=f"🎨 FRAME: {name} ♾️", description=f"**Style:** Black 960x540 | Gold border\n**Status:** ✅ جاهز للتحميل الحقيقي", color=GOLD)
    await ctx.send(embed=embed, view=FrameDownloadView(target_name=name))

@bot.command(name='اعضاء')
async def members_pro(ctx):
    embed = discord.Embed(title="👑 مجلس BSF الأعلى ♾️", color=BLACK)
    members = [("🦁 أبو عيسى", "الزعيم"), ("🐯 عجيب", "المجنون 🌯"), ("👻 الغامض", "المؤسس"), ("🤓 موشي", "العبقري"), ("💤 موسى", "النايم"), ("♾️ MUSA", "اللامنتهي")]
    for n, d in members: embed.add_field(name=n, value=d, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='لفل')
async def level_pro(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = load_levels().get(str(member.id), {"xp": 0, "level": 1})
    need = data["level"] * 100
    bar = "█" * int(data["xp"]/need*10) + "░" * (10 - int(data["xp"]/need*10))
    embed = discord.Embed(title=f"📊 BSF CARD - {member.display_name} ♾️", color=CYAN)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Level", value=f"**{data['level']}** 👑", inline=True)
    embed.add_field(name="XP", value=f"{data['xp']}/{need}", inline=True)
    embed.add_field(name="Progress", value=f"`{bar}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='توب')
async def leaderboard(ctx):
    levels = load_levels()
    sorted_levels = sorted(levels.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:10]
    text = ""
    for i, (uid, data) in enumerate(sorted_levels, 1):
        try: name = (await bot.fetch_user(int(uid))).display_name
        except: name = f"User {uid[:4]}"
        text += f"**{i}.** {name} - لفل {data['level']}\n"
    embed = discord.Embed(title="🏆 توب BSF ♾️", description=text or "لسا ما حد كتب", color=GOLD)
    await ctx.send(embed=embed)

@bot.command(name='اقتباس')
async def quote(ctx):
    embed = discord.Embed(description=f"**\"{random.choice(BSF_QUOTES)}\"**", color=GOLD)
    await ctx.send(embed=embed)

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("❌ ما لقيت TOKEN")
else:
    bot.run(TOKEN)
