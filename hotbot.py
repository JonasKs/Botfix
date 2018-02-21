import discord
import asyncio
from discord.ext import commands
import urllib.request, json
import random
description = '''A blizzard armory lookup bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def updategame(game : str):
    """Update what I'm playing (Just for fun)"""
    await bot.change_presence(game=discord.Game(name=game))

@bot.command()
async def kills(user : str):
    """Gir tilbake honorable kills"""
    with urllib.request.urlopen("https://eu.api.battle.net/wow/character/kazzak/"+ user + "?fields=progression&locale=en_GB&apikey=APIKEY") as url:
        data = json.loads(url.read().decode())
        string = str(data['totalHonorableKills'])
        await bot.say(user + " has " + string + " kills.")

@bot.command()
async def IQ(user : str):
    """IQ-kommandoen, random nummer mellom 1-150"""
    answer = random.randint(1, 150)
    await bot.say("{} har en IQ på ufattelige {}".format(user,answer))

@bot.command()
async def ilevel(user : str):
    """Gir tilbake average ilevel"""
    with urllib.request.urlopen("https://eu.api.battle.net/wow/character/kazzak/"+ user + "?fields=items&locale=en_GB&apikey=APIKEY") as url:
        data = json.loads(url.read().decode())
        string = str(data['items']['averageItemLevelEquipped'])
        bags = str(data['items']['averageItemLevel'])
        await bot.say(user + " has an average ilvl of " + string + " equipped.(" + bags + " in his bags)")

@bot.command()
async def enchants(user : str):
    """Sier om items er enchanta eller ei"""
    with urllib.request.urlopen("https://eu.api.battle.net/wow/character/kazzak/"+ user + "?fields=items&locale=en_GB&apikey=APIKEY") as url:
        data = json.loads(url.read().decode())
        neck = (data['items']['neck']['tooltipParams'])
        ring1 = (data['items']['finger1']['tooltipParams'])
        ring2 = (data['items']['finger2']['tooltipParams'])
        back = (data['items']['back']['tooltipParams'])
        dict = {"neck" : neck, "ring1" : ring1, "ring2" : ring2, "back" : back}
        variabel = list()
        for k, v in dict.items():
            if 'enchant' in v:
                variabel.append(k)
                #await bot.say("Enchanted: {}".format(k))
        formatted = ('%s' % ', '.join(map(str, variabel)))
        if len(variabel) == 4:
            text = user + " har enchanta **alle** sine items: **{}** :white_check_mark:".format(formatted)
        elif len(variabel) !=4:
            text = user + " har **ikke** enchanta alle sine items. Enchanted items: **{}** :x:".format(formatted)
        em = discord.Embed(title="Enchanted items", description=text, colour=14108901)
        em.set_footer(icon_url='')
        #em.add_field(name='Enchants', value=enchants)
        await bot.say(embed=em)

@bot.command()
async def hvemerbest(user1 : str, user2 : str):
    nr1 = ""
    nr2 = ""
    with urllib.request.urlopen("https://eu.api.battle.net/wow/character/kazzak/"+ user1 + "?fields=items&locale=en_GB&apikey=APIKEY") as url:
        data = json.loads(url.read().decode())
        string = str(data['items']['averageItemLevelEquipped'])
        nr1 = string
    with urllib.request.urlopen("https://eu.api.battle.net/wow/character/kazzak/"+ user2 + "?fields=items&locale=en_GB&apikey=APIKEY") as url:
        data = json.loads(url.read().decode())
        string = str(data['items']['averageItemLevelEquipped'])
        nr2 = string
    if nr1 > nr2:
        await bot.say("{} er bedre enn {} med ilvl {} over {} sine ynklige {}! ".format(user1,user2,nr1,user2,nr2))
    if nr1 < nr2:
        await bot.say("{} er bedre enn {} med ilvl {} over {} sine ynklige {}! ".format(user2,user1,nr2,user1,nr1))
bot.run('DiscordTokenID')
