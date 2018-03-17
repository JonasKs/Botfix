import discord
from discord.ext import commands
import random
import sqlite3
import html

description = '''A bot to update the banlog site.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def botupdategame(game : str):
    """Update what I'm playing"""
    await bot.change_presence(game=discord.Game(name=game))

@bot.event
async def on_message(message):
    """Ban command, editing reason in database. NO FAULTHANDLING IMPLEMENTED AT THIS POINT"""
    #Check that the message is sent to a mod channel:
    if message.channel.id == str(237642214824476673) or message.channel.id == str(255804937651355648):
        if message.content.startswith('!update ban'):
            content = message.content
            crop = content[12:]
            string = crop.split(' ', 1)
            username = string[0]
            lowername = username.lower()
            reason = html.escape(string[1])
            melding = 'Updating ban for `{}` with reason `{}`'.format(lowername,reason)
            await bot.send_message(message.channel, melding)


            sqlite_file = '/home/ubuntu/twitch-bans/db.sql'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("UPDATE bans SET reason=? WHERE username=? AND type='ban'", (reason, lowername))
            conn.commit()
            conn.close()

        elif message.content.startswith('!update unban'):
            """Unban command, editing reason in database. NO FAULTHANDLING IMPLEMENTED AT THIS POINT"""
            content = message.content
            crop = content[14:]
            string = crop.split(' ', 1)
            username = string[0]
            lowername = username.lower()
            reason = html.escape(string[1])
            melding = 'Updating unban for `{}` with reason `{}`'.format(lowername,reason)
            await bot.send_message(message.channel, melding)


            sqlite_file = '/home/ubuntu/twitch-bans/db.sql'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("UPDATE bans SET reason=? WHERE username=? AND type='unban'", (reason, lowername))
            conn.commit()
            conn.close()
bot.run('DiscordBotToken')
