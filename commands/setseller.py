import discord
import requests
from os import stat, system
from discord.utils import get
from colorama import Fore as color
import datetime
import json
from discord.ext import commands
from datetime import datetime
from discord.ui import InputText, Modal
from discord.ui import Select, View, Button
from discord.ext.commands import BucketType
# pip install -U git+https://github.com/Pycord-Development/pycord

class SetSeller(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = commands.Bot = bot

    with open('./config.json') as f:
        data = json.load(f)
        token = data.get('token')
        prefix = data.get('prefix')
        sellerkey = data.get('sellerkey')
        dell = data.get('delete_after')
        permsrole = data.get('perms_role_id')
        role = data.get('customer_role_id')

    url = f"https://keyauth.win/api/seller={sellerkey}&type="

    embedcolor = 0xf47fff
    times = datetime.now()

    def perms(self, ctx):
        role = ctx.guild.get_role(self.permsrole)
        return role in ctx.author.roles

    @commands.slash_command(description="Set your sellerkey")
    async def setseller(self, ctx, key:discord.Option(str, "What is your sellerkey?")):
        await ctx.defer()
        if not self.perms(ctx):
            embed=discord.Embed(title="Insufficient perms", description="It seems you don't have permissions to use this command", color=self.embedcolor, timestamp=self.times)
            await ctx.respond(embed=embed) 
        else:
            key = key
            data = json.load(open("./config.json"))
            data["sellerkey"] = key
            json.dump(data, open('./config.json'), sort_keys=False, indent=4)
            await ctx.respond("Your sellerkey has been set!", ephemeral=True)

def setup(bot):
    bot.add_cog(SetSeller(bot))