import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# connection test
client = MongoClient(os.getenv("MONGO_URL"), server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("Database connected!")
except Exception as err:
    print(err)

bot = commands.Bot(command_prefix="$", intents=intents)

async def load():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension("commands.{}".format(filename[:-3]))

    await bot.tree.sync()

@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user))
    await load()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("TirBot"))

@bot.command(name="reload")
async def hotswap_reload(ctx: commands.Context):
    if ctx.author.id != int(os.getenv("OWNER")):
        await ctx.reply("이 명령어는 봇 관리자만 사용 할 수 있습니다", mention_author=False)
        return

    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.reload_extension("commands.{}".format(filename[:-3]))
    
    print("all command reload complete")
    await ctx.reply("모든 명령어를 다시 불러 왔습니다", mention_author=False)

@bot.tree.command(name="reload", description="명령어를 다시 불러 옵니다")
async def reload(interaction: discord.Interaction):
    if interaction.user.id != int(os.getenv("OWNER")):
        await interaction.response.send_message("이 명령어는 봇 관리자만 사용 할 수 있습니다", ephemeral=True)
        return

    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.reload_extension("commands.{}".format(filename[:-3]))
    
    print("all command reload complete")
    await interaction.response.send_message("모든 명령어를 다시 불러 왔습니다", ephemeral=True)

bot.run(os.getenv("TOKEN"))
