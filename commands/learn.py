import os
from utils.data import database
from discord.ext import commands

coll = database["learn"]
ignore = ["학습량", "티르봇", "프젝", "프로젝트"]
disallowed = ["@everyone", "@here"]

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
    async def learn(self, ctx: commands.Context, str, *, message: str):
        for i in ignore:
            if str == i:
                await ctx.reply("이 단어는 배울 수 없는 단어예요", mention_author=False)
                return
            
        for i in disallowed:
            if message in i:
                await ctx.reply("이 단어의 설명은 금지된 말이에요", mention_author=False)
                return

        if not self.exist(str):
            coll.insert_one({
                "str": str,
                "message": message,
                "author": ctx.author.name,
                "author_id": ctx.author.id
            })
            await ctx.reply("\"{}\"라는 단어를 배웠어요".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        if ctx.author.id == int(data["author_id"]):
            coll.update_one({"str": str}, {
                "$set": {
                    "message": message
                }
            })

            await ctx.reply("\"{}\"라는 단어를 다시 배웠어요".format(str), mention_author=False)
            return
        
        await ctx.reply("이미 \"{}\"라는 단어를 {}님한테서 배웠어요".format(data["str"], data["author"]), mention_author=False)

    @commands.command(name="잊어")
    async def forget(self, ctx: commands.Context, str):
        for i in ignore:
            if str == i:
                await ctx.reply("이 단어는 잊을 수 없는 단어예요", mention_author=False)
                return
            
        if not self.exist(str):
            await ctx.reply("\"{}\"라는 단어를 배운적이 없어요".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        if ctx.author.id != int(data["author_id"]) and ctx.author.id != int(os.getenv("OWNER")):
            await ctx.reply("\"{}\"라는 말을 가르친 사람이 아니예요".format(str), mention_author=False)
            return
        
        coll.delete_one({"str": str})
        await ctx.reply("\"{}\"라는 말을 잊을게요".format(str), mention_author=False)

async def setup(bot):
    await bot.add_cog(Learn(bot))
