import discord
from discord.ext import commands
import random
import sqlite3

description = '''A bot to update the website database.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.channel.id == str('channel1ID') or message.channel.id == str('channel2ID'):
        await bot.process_commands(message)
#@bot.command()
#async def help(name="help"):
#    """Commands for this bot. Ask Hotfix#6638. """
#    await bot.say('You can use this bot to update the reason for bans and unbans on the website. Example: !update ban hotfix "Banned because of.."')

@bot.command()
async def updategame(game : str):
    """Update what I'm playing, just for fun."""
    await bot.change_presence(game=discord.Game(name=game))

@bot.group(pass_context=True)
async def update(ctx):
    """Example: !update <command> <name> "<Reason>" """
    if ctx.invoked_subcommand is None:
        await bot.say('You need to add a reason')

@update.command()
async def ban(user: str, reason: str):
    """Ban command, editing reason in database. NO FAULTHANDLING IMPLEMENTED AT THIS POINT"""
    sqlite_file = '/home/ubuntu/twitch-bans/db.sql'
    await bot.say('updating ban for {}: {}'.format(user, reason))
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("UPDATE bans SET reason=? WHERE username=? AND type='ban'", (reason, user))
    conn.commit()
    conn.close()

@update.command()
async def unban(user: str, reason: str):
    """Unban command, editing reason in database. NO FAULTHANDLING IMPLEMENTED AT THIS POINT"""
    sqlite_file = '/home/ubuntu/twitch-bans/db.sql'
    await bot.say('updating ban for {}: {}'.format(user, reason))
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("UPDATE bans SET reason=? WHERE username=? AND type='unban'", (reason, user))
    conn.commit()
    conn.close()

bot.run('DiscordBotToken')
