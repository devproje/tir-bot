import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from discord.ext import commands

client = MongoClient(os.getenv("MONGO_URL"), server_api=ServerApi("1"))
db = client["tir_bot"]
coll = db["learn"]

class Learn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_data(self, str):
        return coll.find_one({"str": str})

    def exist(self, str):
        res = self.get_data(str)
        if res != None:
            return True
        
        return False

    @commands.command(name="배워")
    async def learn(self, ctx: commands.Context, str, *, message):
        if str == "학습량":
            await ctx.reply("이 단어는 배울 수 없는 단어예요")
            return
        
        if not self.exist(str):
            coll.insert_one({
                "str": str,
                "message": message,
                "author_id": ctx.author.id,
                "author_name": ctx.author.name
            })
            await ctx.reply("\"{}\"라는 단어를 배웠어요".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        await ctx.reply("이미 \"{}\"라는 단어를 {}님한테서 배웠어요".format(data["str"], data["author_name"]), mention_author=False)

    @commands.command(name="잊어")
    async def forget(self, ctx: commands.Context, str):
        if str == "학습량":
            await ctx.reply("이 단어는 잊을 수 없는 단어예요")
            return
            
        if not self.exist(str):
            await ctx.reply("\"{}\"라는 단어를 배운적이 없어요".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        if int(data["author_id"]) != ctx.author.id:
            await ctx.reply("\"{}\"라는 말을 가르친 사람이 아니예요".format(str), mention_author=False)
            return
        
        coll.delete_one({"str": str})
        await ctx.reply("\"{}\"라는 말을 잊을게요".format(str), mention_author=False)

async def setup(bot):
    await bot.add_cog(Learn(bot))
