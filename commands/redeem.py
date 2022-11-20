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

class Redeem(commands.Cog):
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

    class RedeemModal(Modal):
        def __init__(self) -> None:
            super().__init__(title="Redeem Your License")
            self.add_item(InputText(label="Username", placeholder="Input Username: ", required=True)),
            self.add_item(InputText(label="Password", placeholder="Input Password: ", required=True)),
            self.add_item(InputText(label="License", placeholder="Input License: ", required=True))
        async def callback(self, interaction:discord.Interaction):
            with open('./config.json') as f:
                data = json.load(f)
                sellerkey = data.get('sellerkey')
                role = data.get('customer_role_id')
            embedcolor = 0xf47fff
            times = datetime.now()
            un = self.children[0].value
            pw = self.children[1].value
            key = self.children[2].value
            req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=activate&user={un}&key={key}&pass={pw}&format=text")
            if req.json()["success"]:
                await interaction.response.defer()
                embed=discord.Embed(title=f"License Successfully Activated", color=embedcolor, timestamp=times)
                embed.set_footer(text=f"Command run by: {interaction.user}", icon_url=interaction.user.avatar)
                embed.add_field(name="Username", value=un, inline=False)
                embed.add_field(name="Password", value=pw, inline=False)
                embed.add_field(name="License", value=key, inline=False)
                await interaction.user.send(embed=embed)
                roles = interaction.user.guild.get_role(role)
                await interaction.user.add_roles(roles)
            else:
                embed=discord.Embed(title="Error with api", description=f"Note: `Your seller key is most likely not set. Please tell the owner.`", color=self.embedcolor, timestamp=self.times)
                embed.set_footer(text=f"Command run by: {interaction.user}", icon_url=interaction.user.avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            req.close()

    @commands.slash_command(description="Sends redeem panel")
    async def redeempanel(self, ctx, channel:discord.Option(discord.TextChannel, "Where am I sending the panel?")):
        await ctx.defer()
        if not self.perms(ctx):
            embed=discord.Embed(title="Insufficient perms", description="It seems you don't have permissions to use this command", color=self.embedcolor, timestamp=self.times)
            await ctx.respond(embed=embed) 
        else:
            try:
                button = Button(label="Redeem", style=discord.ButtonStyle.blurple)
                modal = self.RedeemModal()
                async def callback(interaction):
                    await interaction.response.send_modal(modal)
                button.callback = callback
                embed=discord.Embed(description=f"Ready to redeem your key? Click the button!", color=self.embedcolor, timestamp=self.times)
                view = View(timeout=None)
                view.add_item(button)
                await channel.send(embed=embed, view=view)
                await ctx.respond(f"Panel sent! {channel.mention}", ephemeral=True)
            except Exception as m:
                await ctx.respond(f"An error has occured. \nError: `{m}`")
def setup(bot):
    bot.add_cog(Redeem(bot))
