from importlib.abc import InspectLoader
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.colour import Colour
from discord.ext.commands import Bot as Base
from pathlib import Path
from discord import Intents, guild
from discord import Embed
from datetime import datetime
from glob import glob
from discord.ext.commands.errors import CommandNotFound

PREFIX = "+"
OWNER_IDS = [776937055325913108]
par_parent = Path(__file__).parent.parent.resolve()
COGS = [path.split("\\")[-1][:-3] for path in glob(f"{par_parent}/cogs/*.py")]
print(COGS)
class Bot(Base):
    
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.stdout = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all(), case_insensitive=True)

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
            print(f"i the great {cog} loaded ;)")

    async def on_connect(self):
        print('Bot Connected')

    async def on_disconnect(self):
        print("i'm not there")
    
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("i'm sad and something is wrong")
        raise

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            pass
        elif hasattr(exception,"original"):
            raise exception.original
        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(self.guilds[0].id)
            self.ready = True
            print("Bot readyyyy")
        else:
            print("Bot reconnected")
        #get the channel
        self.stdout=self.get_channel(self.guild.channels[2].id)
        channel = self.get_channel(self.guild.channels[2].id)
        #instructions embed
        instructions = Embed(title="What do I Have ?", description="Just \"SHOWING YOU WHAT I GOT\"")
        instructions.set_author(name="Instructions")
        instructions.set_thumbnail(url="https://media.tenor.com/images/9fffd1be4fdecdc1836a7be8b86f4ba9/tenor.gif")
        instructions.add_field(name="chooseforme", value="I Take little decisions for you ;)")
        instructions.add_field(name="slap_member", value="I... Slap others")
        instructions.set_footer(text="For More Info's Type +help ♥")
        instructions.set_image(url="https://media1.tenor.com/images/0efb7c1066dc4a1030633b867aa42e32/tenor.gif?itemid=4768981")
        await channel.send(embed=instructions)
    #might override this one later >
    # async def on_message(self, message):
    #     pass

bot = Bot()