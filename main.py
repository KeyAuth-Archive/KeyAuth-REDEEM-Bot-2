import discord
from discord.utils import get
from colorama import Fore as color
import asyncio
import platform
import random
import os
import datetime
import json
from discord.ext import commands
from discord.ui import InputText, Modal
from discord import SyncWebhook
from datetime import datetime
# pip install -U git+https://github.com/Pycord-Development/pycord

with open('config.json') as f:
    data = json.load(f)
    token = data.get('token')
    prefix = data.get('prefix')
    sellerkey = data.get('sellerkey')
    dell = data.get('delete_after')
    permsrole = data.get('perms_role_id')
    mask = data.get('mask')
    logcha = data.get('logging_channel')

int = discord.Intents.all() # enable all intents on discord developer portal
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=int)

async def ch_pr():
    await bot.wait_until_ready()
    statuses = ['KeyAuth', 'Redeem', 'Bot']
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=5, name=status))
        await asyncio.sleep(5)
        
number = 0
@bot.event
async def on_ready():
    launch_time = datetime.now()
    host_name = os.environ['COMPUTERNAME']
    print(f"{color.RED}-------------------------------------------------------")
    print(f"{color.GREEN}Logged in as {bot.user.name} : {bot.user.id}")
    print(f"{color.YELLOW}Running on python version: {platform.python_version()}")
    print(f"{color.CYAN}OS Information: {platform.system()} {platform.release()} ({host_name})")
    print(f"{color.LIGHTBLACK_EX}Cogs loaded: {number}")
    print(f"{color.RED}-------------------------------------------------------")

cogfiles = [
    f"commands.{filename[:-3]}" for filename in os.listdir("commands") if filename.endswith(".py")
]

for cogfile in cogfiles:
    try:
        bot.load_extension(cogfile)
        number += 1
    except Exception as err:
        print(err)

bot.loop.create_task(ch_pr())
bot.run(token)