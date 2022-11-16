import discord
import requests
from os import stat, system
from discord.utils import get
from colorama import Fore as color
import datetime
import json
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from discord.ext.commands import BucketType

class AntiSpam(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = commands.Bot = bot

    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention} dont spam!", delete_after=4.0)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                await message.author.timeout(timedelta(minutes=10), reason="Spamming")

def setup(bot):
    bot.add_cog(AntiSpam(bot))