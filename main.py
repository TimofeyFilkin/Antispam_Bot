# bot.py
import os
import discord
from dotenv import load_dotenv
from art import tprint
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="/")

guild = None

repeats = 0
message_text = ""


@bot.event
async def on_ready():
    global guild
    guild = bot.get_guild(int(os.getenv('GUILD_TO_SECURE')))
    tprint("ANTISPAM   BOT")
    print("Securing server " + guild.name)


@bot.command()
async def ping_asb(ctx):
    await ctx.send("Pong!")


@bot.command()
async def terminate_bot(ctx):
    await ctx.channel.send("Killing bot...")
    exit()


@bot.event
async def on_message(msg):
    global repeats, message_text
    if msg.author == bot.user:
        return
    if msg.content == message_text:
        repeats += 1
        if repeats == 3:
            # noinspection PyUnresolvedReferences
            await guild.ban(msg.author, reason="spam")
            ban_kanava = await bot.fetch_channel(int(os.getenv('BAN_INFO_CHANNEL')))
            await ban_kanava.send("пользователь " + msg.author.name + " был забанен за спам в канале " + str(
                msg.channel.name) + "... А нефиг спамить было...")
    else:
        repeats = 1
        message_text = msg.content
    await bot.process_commands(msg)


bot.run(TOKEN)
