from discord.ext.commands import (CommandNotFound, MissingRequiredArgument, BadArgument)
from discord.ext.commands.errors import UserInputError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands.context import Context
from discord.ext.commands import Bot as Base
from discord.errors import HTTPException
from importlib.abc import InspectLoader
from discord import Intents, guild
from discord.colour import Colour
from asyncio.tasks import sleep
from datetime import datetime
from discord import Embed
from pathlib import Path
from glob import glob
import discord
PREFIX = "+"

par_parent = Path(__file__).parent.parent.resolve()
COGS = [path.split("/")[-1][:-3] for path in glob(f"{par_parent}/cogs/*.py")]

class Ready(object):
    
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(Base):

    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        self.stdout = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=PREFIX,
            intents=Intents.all(),
            case_insensitive=True
        )


    def run(self, version):
        self.VERSION = version

        path = Path(__file__).parent / "token.0"
        self.TOKEN = path.read_text()

        print("running the setup ...")
        self.setup()

        print("i'm running :)")
        super().run(self.TOKEN, reconnect=True)


    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"I the great {cog} loaded ;)")


    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else: 
                await ctx.send('Don\'t rush me human')


    async def on_connect(self):
        print('Bot Connected')


    async def on_disconnect(self):
        print("I'm not there")


    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("I'm sad and something is wrong")
        raise


    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc,"original"):
            raise exc.original
        elif isinstance(exc, UserInputError):
            pass
        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(self.guilds[0].id)
            #get the channel
            channel_id = None
            for chan in self.guild.channels:
                if isinstance(chan, discord.channel.TextChannel):
                    channel_id = chan.id
                    break
            self.stdout = self.get_channel(channel_id)

            # while not self.cogs_ready.all_ready():
            #     await sleep(0.1)

            self.ready = True
            print("Bot readyyyy")
        else:
            print("Bot reconnected")

        
        #instructions embed
        instructions = Embed(title="What do I Have ?", description="Just \"SHOWING YOU WHAT I GOT\"")
        instructions.set_author(name="Instructions")
        instructions.set_thumbnail(url="https://media.tenor.com/images/9fffd1be4fdecdc1836a7be8b86f4ba9/tenor.gif")
        instructions.add_field(name="chooseforme", value="I Take little decisions for you ;)")
        instructions.add_field(name="slap_member", value="I... Slap others")
        instructions.set_footer(text="For More Info's Type +help ♥")
        instructions.set_image(url="https://media1.tenor.com/images/0efb7c1066dc4a1030633b867aa42e32/tenor.gif?itemid=4768981")
        await self.stdout.send(embed=instructions)
    #might override this one later >
    async def on_message(self, message):
        if not message.author.bot:
            if message.content.startswith(PREFIX):
                await self.process_commands(message)

bot = Bot()