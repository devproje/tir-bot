import discord, time
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Discord API의 레이턴시를 확인 합니다")
    async def ping(self, interaction: discord.Interaction):
        before = time.monotonic()
        await interaction.response.send_message(":hourglass: Just wait seconds...")
        after = round((time.monotonic() * 1000) - (before * 1000))
        BOT = "BOT: **{}**ms".format(after)
        API = "API: **{}**ms".format(round(interaction.client.latency * 1000))
        await interaction.edit_original_response(content=":ping_pong: **Pong!**\n{}\n{}".format(BOT, API))

async def setup(bot):
    await bot.add_cog(Ping(bot))
