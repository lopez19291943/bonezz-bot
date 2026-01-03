import discord
from discord.ext import commands
import asyncio
import io
import os
from datetime import datetime, timedelta

# ===================== CONFIG =====================
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ===================== IDS =====================
ROLE_IDS = {
    "Quickdrop Ping": 1457029272135798845,
    "Partner Ping": 1457029321091842049,
    "Bone Update Ping": 1457029356164616409,
    "Giveaway Ping": 1457029577074544693
}

STAFF_ROLE_IDS = [
    1457026393505271890,
    1457026561646657753,
    1457026599575883858,
    1457026630949273714,
    1457027006884479098
]

TRANSCRIPT_CHANNEL_ID = 1457046645975027714
LOG_CHANNEL_ID = 1457046666636034080

BONE_LOG_CHANNEL = 1457057222822723787
BONE_TRANSCRIPT_CHANNEL = 1457057210768036044

WELCOME_CHANNEL_ID = 1456438905556570282
AUTO_ROLE_ID = 1457026481850159205

# ===================== READY =====================
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

def is_staff(member: discord.Member):
    return any(r.id in STAFF_ROLE_IDS for r in member.roles)

# ===================== RULES =====================
@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title="<:bone:1457032953493459067> Bonezz Market | Server Rules",
        description="Please read these rules carefully. Breaking them may result in punishment.",
        color=0x2f3136
    )

    embed.add_field(
        name="General Rules",
        value=(
            "• No NSFW content\n"
            "• Do not share private or personal information\n"
            "• No discrimination of any kind\n"
            "• No ban or mute evasion\n"
            "• Do not unnecessarily ping staff\n"
            "• No malware or harmful content\n"
            "• Use channels only for their intended purpose\n"
            "• Be respectful to all members\n"
            "• No spamming\n"
            "• Report any bugs found in the server\n"
            "• NO IRL trading, cross trading, or invite rewards"
        ),
        inline=False
    )

    embed.add_field(
        name="Additional Rules",
        value=(
            "• Follow the rules of the DonutSMP Discord and Minecraft servers\n"
            "• Follow Discord's Terms of Service and Community Guidelines\n\n"
            "https://discord.com/terms\n"
            "https://discord.com/guidelines"
        ),
        inline=False
    )

    embed.add_field(
        name="Giveaway Rules",
        value=(
            "• No attempting to fake winning a giveaway\n"
            "• Do not claim a giveaway more than once\n"
            "• Disrespect towards staff will result in no payout\n"
            "• Do not use multiple accounts to join giveaways"
        ),
        inline=False
    )

    embed.add_field(
        name="Important",
        value=(
            "Use common sense at all times.\n"
            "Just because a rule is not listed here does not mean you cannot be punished.\n\n"
            "DM <@1422572547928621127> if needed."
        ),
        inline=False
    )

    embed.set_footer(text="Last Updated: January 03, 2026")
    await ctx.send(embed=embed)

# ===================== ROLES =====================
class RoleButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle(self, interaction, role_id):
        role = interaction.guild.get_role(role_id)
        member = interaction.user

        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"Removed **{role.name}**.", ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"Added **{role.name}**.", ephemeral=True
            )

    @discord.ui.button(label="Quickdrop Ping", style=discord.ButtonStyle.secondary)
    async def qd(self, interaction, _):
        await self.toggle(interaction, ROLE_IDS["Quickdrop Ping"])

    @discord.ui.button(label="Partner Ping", style=discord.ButtonStyle.secondary)
    async def partner(self, interaction, _):
        await self.toggle(interaction, ROLE_IDS["Partner Ping"])

    @discord.ui.button(label="Bone Update Ping", style=discord.ButtonStyle.secondary)
    async def update(self, interaction, _):
        await self.toggle(interaction, ROLE_IDS["Bone Update Ping"])

    @discord.ui.button(label="Giveaway Ping", style=discord.ButtonStyle.secondary)
    async def giveaway(self, interaction, _):
        await self.toggle(interaction, ROLE_IDS["Giveaway Ping"])

@bot.command()
async def roles(ctx):
    embed = discord.Embed(
        title="<:bone:1457032953493459067> Bonezz Market | Notification Roles",
        description=(
            "Click the buttons below to manage your notification roles.\n"
            "Click again to remove a role you already have."
        ),
        color=0x2f3136
    )

    embed.add_field(
        name="Available Roles",
        value=(
            "Quickdrop Ping\n"
            "Partner Ping\n"
            "Bone Update Ping\n"
            "Giveaway Ping"
        ),
        inline=False
    )

    await ctx.send(embed=embed, view=RoleButtons())

# ===================== SPAWNER =====================
@bot.command()
async def spawner(ctx, buying: str, selling: str):
    embed = discord.Embed(
        title="<:bone:1457032953493459067> Bonezz Market | Spawner Information",
        description="Current spawner prices and important trading information are listed below.",
        color=0x2f3136
    )

    embed.add_field(
        name="We're Buying (You sell to us)",
        value=f"<:spawner:1457026312517583098> Spawners | {buying}",
        inline=False
    )

    embed.add_field(
        name="We're Selling (You buy from us)",
        value=f"<:spawner:1457026312517583098> Spawners | {selling}",
        inline=False
    )

    embed.add_field(
        name="Information",
        value=(
            "• We never go first in trades for security reasons\n"
            "• We will never DM you first\n"
            "• Prices may change depending on the market\n"
            "• We try to keep prices updated daily"
        ),
        inline=False
    )

    embed.add_field(
        name="Note",
        value="Thank you for choosing Bonezz Market. Enjoy trading with us.",
        inline=False
    )

    await ctx.send(embed=embed)

# ===================== HELP =====================
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="<:bone:1457032953493459067> Bonezz Market | Help",
        description="List of all available commands.",
        color=0x2f3136
    )

    embed.add_field(
        name="General",
        value=(
            "`!rules`\n"
            "`!roles`\n"
            "`!help`"
        ),
        inline=False
    )

    embed.add_field(
        name="Market",
        value=(
            "`!spawner <buy> <sell>`\n"
            "`!restock <amount> <price>`"
        ),
        inline=False
    )

    embed.add_field(
        name="Support",
        value=(
            "`!ticket`\n"
            "`!bone <price>`"
        ),
        inline=False
    )

    await ctx.send(embed=embed)

# ===================== WELCOME =====================
@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    role = member.guild.get_role(AUTO_ROLE_ID)

    if channel:
        await channel.send(
            "<:bone:1457032953493459067> **New member joined!**\n\n"
            f"Hey {member.mention}, welcome to **Bonezz Market**.\n"
            "Enjoy your stay!"
        )

    if role:
        await member.add_roles(role, reason="Auto role on join")

# ===================== RUN =====================
bot.run(TOKEN)
