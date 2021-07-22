from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.colour import Colour
from discord.ext.commands import Bot as Base
from pathlib import Path
from discord import Intents, guild
from discord import Embed
PREFIX = "*"
OWNER_IDS = [776937055325913108]

class Bot(Base):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def run(self, version):
        self.VERSION = version
        path = Path(__file__).parent / "token.0"
        self.TOKEN = path.read_text()
        
        print("i'm running :)")
        super().run(self.TOKEN, reconnect = True)

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        print("i'm not there")
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(self.guilds[0].id)
            print("Bot readyyyy")
        else:
            print("Bot reconnected")

        channel = self.get_channel(self.guild.channels[2].id)
        await channel.send("i'm there")

        embed = Embed(title = "I AM A Piece Of Shit", description = "You Know, Brown And Not So Wanted", colour = 0x0000FF)
        embed.add_field(name= "This field is to say that Ilove You", value= "the value is priceless ♥")
        await channel.send(embed=embed)

    async def on_message(self, message):
        pass

bot = Bot()