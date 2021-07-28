from discord.ext.commands.errors import BadArgument, UserInputError
from discord.ext.commands import command
from discord.errors import HTTPException
from discord.ext.commands import Cog
import random


class ChooseForME(Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('ChooseForME')

    @command(name = 'chooseforme', aliases=['ch', 'chm', 'choose', 'pick', 'rand'])
    async def chooseforme(self, ctx, *, message):
        """
        If You called me then you probably are a Libra
        I Pick A Random Choice For You
        - Provide the optionS seperated by a space -
        """
        if message == "":
            await ctx.send('GIMME OPTIONS')
        else:
            options = message.split(' ')
            await ctx.send(random.choice(options))
    @chooseforme.error
    async def chooseforme_error(self, ctx, exc):
        if isinstance(exc, UserInputError):
            await ctx.send('You Did Not Input Any Options')

def setup(bot):
    bot.add_cog(ChooseForME(bot))