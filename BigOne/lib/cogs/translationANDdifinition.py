from libretranslatepy import LibreTranslateAPI
from discord.ext.commands import command
from discord.errors import HTTPException
from discord.ext.commands import Cog
from discord import Embed
import requests
import json
class Translator(Cog):
    def __init__(self, bot):
        self.bot = bot 

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('translator')

    @command(name="translate", aliases=["meaning", "tran"])
    async def translate(self, ctx, *, message):
        """
        Input 3 argumens, the word(e.g food), from (e.g en), to (e.g ar)
        """
        parts = message.split()
        lt = LibreTranslateAPI("https://translate.astian.org/")
        lt.detect(message)
        await ctx.send(lt.translate(" ".join(parts[:-2]), parts[-2], parts[-1]))

class Definition(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Definition')

    @command(name="define", aliases=[])
    async def definition(self, ctx, *, message):
        """
        Gives back the definition of the word and other infos
        Code   	 Language

        ==================

        en_US 	 English (US)
        hi 	     Hindi
        es 	     Spanish
        fr	     French
        ja       Japanese
        ru	     Russian
        en_GB 	 English (UK)
        de 	     German
        it       Italian
        ko 	     Korean
        pt-BR 	 Brazilian Portuguese
        ar       Arabic
        tr       Turkish
        """
        parts = message.split()
        url =f'https://api.dictionaryapi.dev/api/v2/entries/{parts[0]}/{parts[1]}'
        response = requests.get(url)
        def_list = response.json()[0]["meanings"]
        definitions = list()
        for d in def_list:
            for dd in d['definitions']:
                syn = None
                if "synonyms" in dd:
                    syn = dd['synonyms']
                definitions.append((d['partOfSpeech'], dd['definition'], syn))
        #definitions embed
        defines = Embed(title="Definitions", description="Got all available defines of the word")
        defines.set_author(name="Defines")
        for x, y, z in definitions:
            defines.add_field(name=f'part of speech :{x}\n', value=f'def : {y}')
        defines.set_footer(text="For More Info's Type +help ♥")
        if len(parts) > 2:
            if parts[2] == "syn":
                for x, y, z in definitions:
                    defines.add_field(name=f'part of speech :{x}\n', value=f'synonyms : {"|".join(z) if z != None else "No Synonyms"}')
        await ctx.send(embed=defines)

def setup(bot):
    bot.add_cog(Translator(bot))
    bot.add_cog(Definition(bot))
