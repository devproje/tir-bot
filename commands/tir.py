import os
from discord import File
from utils.data import database
from discord.ext import commands

coll = database["learn"]
tir_description = """티르봇은 프로젝트님이 만드신 오픈소스 봇이에요. discord.py 기반으로 만들어져 있으며 봇의 소스코드는 [Github](https://github.com/devproje/tir-bot)에 있어요. 저에게 기능 추가를 원하시는 분들께서는 봇을 포크 후 PR 넣어 주세요.
                                
`이 단어는 티르봇 기본 단어이므로 잊거나 수정할 수 없어요`
"""
project_description = """프로젝트님은 티르봇을 만드신 장본인이에요.

`이 단어는 티르봇 기본 단어이므로 잊거나 수정할 수 없어요`
"""

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

                dt = "<DataArray>\n"
                i = 0
                for d in coll.find({}):
                    dt += "\t<Data>\n"
                    dt += "\t\t<Word>{}</Word>\n".format(d["str"])
                    dt += "\t\t<Message>{}</Message>\n".format(d["message"])
                    dt += "\t\t<WordID>{}</WordID>\n".format(d["_id"])
                    dt += "\t\t<Author>{}</Author>\n".format(d["author"])
                    dt += "\t\t<AuthorID>{}</AuthorID>\n".format(d["author_id"])
                    dt += "\t</Data>\n"
                    i += 1
                
                dt += "</DataArray>\n"
                filename = "result.xml"

                try:
                    with open(filename, "x") as f:
                        f.write(dt)
                        f.close()
                
                except:
                    with open(filename, "w") as f:
                        f.write(dt)
                        f.close()

                await ctx.reply(content="학습된 단어: {}개".format(i), file=File(fp=filename, filename=filename), mention_author=False)
                return
            
            case "티르봇":
                await ctx.reply(tir_description, mention_author=False)
                return
            
            case "프젝":
                await ctx.reply(project_description, mention_author=False)
                return
            
            case "프로젝트":
                await ctx.reply(project_description, mention_author=False)
                return

        if not self.exist(str):
            await ctx.reply("{}라는 단어는 아직 배운적이 없어요\n`$배워 <단어> <메시지>` 명령어로 추가 해보는건 어떨까요?".format(str), mention_author=False)
            return
        
        data = self.get_data(str)
        await ctx.reply("{}\n\n`이 단어는 {}님이 가르쳐 줬어요`".format(data["message"], data["author"]), mention_author=False)

async def setup(bot):
    await bot.add_cog(Tir(bot))
