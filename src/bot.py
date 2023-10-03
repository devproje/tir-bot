import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user))

@bot.tree.command(name="ping", description="Discord API의 레이턴시를 확인 합니다")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! {}ms".format(round(interaction.client.latency)))

bot.run(os.getenv("TOKEN"))
