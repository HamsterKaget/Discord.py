import discord
import os
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import guild_only
from dotenv import load_dotenv
import requests
import json
import asyncio
import youtube_dl

# ================================================================================ #

client = discord.Client()
client = commands.Bot(command_prefix=('!' or '?'))
load_dotenv()

# ================================================================================ #

def get_quote(ctx):
    # Request API
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return quote

# ================================================================================ #

# Login Ke Bot
@client.event
async def on_ready():
    print('Berhasil Login Sebagai {0.user}'.format(client))

# =================================| List Command |============================== #

# Command Ping Lattency
@client.command()
async def ping(ctx):
    await ctx.reply('**pong ! 🏓 {0}ms**'.format(round(client.latency, 3)))

# Command Invite Bot
@client.command()
async  def invite(ctx):
    embedInvite = discord.Embed(title="Invite My Bot !", description="Click [This to invite Me !](https://discord.com/api/oauth2/authorize?client_id=952791683911786516&permissions=8&scope=bot)", color=0x00ff00)
    await ctx.reply(embed=embedInvite)

# Command Request API
@client.command()
async def quote(ctx):
    isi = get_quote(ctx)
    await ctx.channel.send(isi)

# Command Kick Member
@client.command(name='kick', pass_context=True)
@guild_only()
@has_permissions(ban_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'**{member} telah di tendang keluar server !**')

@kick.error
async def kick_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.reply("Sorry {0}, kamu tidak memiliki permission yang diperlukan!".format(ctx.message.author))

# Command untuk ban member
@client.command(name='ban')
@guild_only()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'**{member} telah di ban dari server ini !**')

# Command untuk unban member
@client.command(name='unban')
@guild_only()
@has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.channel.send('**{0} Telah di un-ban**'.format(user))


# Command Server Invite
@client.command()
@guild_only()
async def serverinvite(ctx):
    link = await ctx.channel.create_invite(max_age = 0, max_uses = 0, xkcd = 0)
    await ctx.send('Server Link : {0}'.format(link))



client.run(os.getenv('TOKEN'))





