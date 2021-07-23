from typing import Optional
from discord.ext import commands
from discord.ext.commands import bot, command
from discord.ext.commands import Cog
from discord import Member
from asyncio.tasks import sleep
class slap(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="slap", aliases=["smack", "hit"])
    async def slap(self, ctx, member:Member, *, reason:Optional[str] = "They Probably Deserve It"):
        """
        No violence please sir :)
        """
        slap_order = ctx.message.clean_content.replace("*", "").split(" ")[0]
        if slap_order == "slap":
            slap_order = "slapped"
        elif slap_order == "hit":
            slap_order = "hit"
        else:
            slap_order = "smacked"
        await ctx.send(f'{ctx.author.name} {slap_order} {member.mention} Because {reason}')

def setup(bot):
    bot.add_cog(slap(bot))