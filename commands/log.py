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

class Log(commands.Cog):
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


    class CreateChannel(Modal):
        def __init__(self) -> None:
            super().__init__(title="Set Channel ID")
            self.add_item(InputText(label="Logging channel ID", placeholder="Input Logging Channel ID: ", required=True))
        async def callback(self, interaction:discord.Interaction):
            id = self.children[0].value
            data = json.load(open("./config.json"))
            data["logging_channel"] = id
            json.dump(data, open("./config.json", 'w'), sort_keys=False, indent=4)
            await interaction.response.send_message(f"Log channel has been set. \n\nLog channel: <#{id}>")

    @commands.slash_command(description="Create or set a logs channel")
    async def logs(self, ctx, choice:discord.Option(str, choices=['Set a channel id', 'Create a channel for me'])):
        if not self.perms:
            embed=discord.Embed(title="Insufficient perms", description="It seems you don't have permissions to use this command", color=self.embedcolor, timestamp=self.times)
            await ctx.respond(embed=embed) 
        else:
            if choice == 'Set a channel id':
                modal = self.CreateChannel()
                await ctx.interaction.response.send_modal(modal)
            elif choice == 'Create a channel for me':
                channel = await self.bot.create_text_channel(name="logs")
                await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                data = json.load(open("./config.json"))
                data["logging_channel"] = channel.id
                json.dump(data, open("./config.json", 'w'), sort_keys=False, indent=4)
                await ctx.respond(f"I have created a logs channel for you. {channel.mention}")

def setup(bot):
    bot.add_cog(Log(bot))