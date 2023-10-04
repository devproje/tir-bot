import os
from pymongo import MongoClient
from discord.ext import commands
from pymongo.server_api import ServerApi

client = MongoClient(os.getenv("MONGO_URL"), server_api=ServerApi("1"))
db = client["tir_bot"]
coll = db["learn"]

class Tir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_data(self, str):
        return coll.find_one({"str": str})
    
    def exist(self, str):
        res = self.get_data(str)
        if res != None:
            return True
        
        return False

    @commands.command(name="티르야")
    async def tir(self, ctx: commands.Context, str):
        match str:
            case "학습량":
                if ctx.author.id != int(os.getenv("OWNER")):
                    await ctx.reply("이 명령어는 봇 관리자만 사용 할 수 있습니다", mention_author=False)
                    return

                dt = "```yaml\n"
                i = 0
                for d in coll.find({}):
                    dt += "word: {}:\n".format(d["str"])
                    dt += " response_word: {}\n".format(d["message"])
                    dt += " word_id: {}\n".format("_id")
                    dt += " teaching_person: {}\n".format(d["author_name"])
                    dt += " teaching_person_id: {}\n".format(d["author_id"])
                    i += 1

                dt += "```\n"
                dt += "학습된 단어: {}개".format(i)

                await ctx.reply(dt, mention_author=False)
                return

        if not self.exist(str):
            await ctx.reply("{}라는 단어는 아직 배운적이 없어요\n`$배워 <단어> <메시지>` 명령어로 추가 해보는건 어떨까요?".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        await ctx.reply("{}\n이 단어는 {}님이 가르쳐 줬어요".format(data["message"], data["author_name"]), mention_author=False)

async def setup(bot):
    await bot.add_cog(Tir(bot))
