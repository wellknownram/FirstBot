from discord.ext.commands import command
from discord.ext.commands import Cog
import random

class ChooseForME(Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @command(name = 'chooseforme', aliases=['ch', 'chm', 'choose'])
    async def chooseforme(self, ctx):
        """
        If You called me then you probably are a Libra
        I take a simple Yes/No desision for you
        LEARN TO TAKE RESPONSIPILTY FOR YOUR CHOICES
        """
        choice = random.randint(0, 1)
        if choice == 1:
            await ctx.send("Yes :)")
        else:
            await ctx.send("No :(")
       
def setup(bot):
    bot.add_cog(ChooseForME(bot))