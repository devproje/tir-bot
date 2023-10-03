import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension("cogs.{}".format(filename[:-3]))

    await bot.tree.sync()

@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user))
    await load()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("TirBot"))

@bot.tree.command(name="reload", description="명령어를 다시 불러 옵니다")
async def reload(interaction: discord.Interaction):
    if interaction.user.id != int(os.getenv("OWNER")):
        await interaction.response.send_message("이 명령어는 봇 관리자만 사용 할 수 있습니다", ephemeral=True)
        return

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.reload_extension("cogs.{}".format(filename[:-3]))
    
    print("all command reload complete")
    await interaction.response.send_message("모든 명령어를 다시 불러 왔습니다", ephemeral=True)

bot.run(os.getenv("TOKEN"))
