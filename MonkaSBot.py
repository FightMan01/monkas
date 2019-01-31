import aiohttp
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import datetime, time
import os
import youtube_dl
from discord.voice_client import VoiceClient
global playing
playing = "No music playing right now :("
players = {}
global help_command
help_command = ["HELP"]
global chat_filter
global bypass_list
chat_filter = ["FUCK", "DICK", "SHIT", "FUCKING", "BITCH"]
bypass_list = []
client = commands.Bot(command_prefix='f!')
Client = discord.Client()

@client.event
async def on_ready():
    print ("The bot is ready to use.")
    print ("Name: " + client.user.name)
    print ("ID: " + client.user.id)
    counter = 0
    while not counter > 0:
        await client.change_presence(game=discord.Game(name='DM me for help!', type=3))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='Type: Help!', type=3))
        await asyncio.sleep(10)


@client.command(pass_context=True)
async def ping(ctx):
    '''A ping command'''
    if not ctx.message.author.bot:
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        embed=discord.Embed(title="Pong!", description='This message took around {}ms.'.format(round((t2-t1)*1000)), color=0xffff00)
        await client.say(embed=embed)
    else:
        return False

@client.command(pass_context=True)
async def purge(ctx, amount=301):
    '''Usage: f!purge [amount]'''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '416226732966936577':
        try:
            channel = ctx.message.channel
            messages = []
            async for message in client.logs_from(channel, limit=int(amount) + 1):
                messages.append(message)
            await client.delete_messages(messages)
            await client.say(":white_check_mark: Messages deleted. :thumbsup:")
        except:
            print (Exception)
            await client.say("The number must be between 1 and 300 and the message be maximum 14 days old.:x:")
    else:
        await client.say("You need Admin perms to use this. :x:")

@client.command(pass_context=True, no_pm=True)
async def kick(ctx, user: discord.Member, * ,reason : str = None):
    '''Usage: f!kick [member] [reason]'''
    if not ctx.message.author.bot:
        if ctx.message.author.server_permissions.administrator:
            if reason == "None":
                reason = "(No reason logged!)"
            await client.send_message(user, "You're kicked from **{}** server for this: **".format(ctx.message.server.name) + reason + "**")
            await client.say("Bye, {}. You got kicked :D".format(user.mention))
            await client.kick(user)  
        else:
            await client.say("You need Admin prems to use this! :x:")
    else:
        return False

@client.command(pass_context=True)
async def serverinfo(ctx):
    '''A useful command.'''
    if not ctx.message.author.bot:
        online = 0
        for i in ctx.message.server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        role_count = len(ctx.message.server.roles)
        emoji_count = len(ctx.message.server.emojis)
        embed = discord.Embed(title="Information from this server: {}".format(ctx.message.server.name), description="Here it is:", color=0x00ff00)
        embed.add_field(name="Name: ", value=ctx.message.server.name, inline=True)
        embed.add_field(name="ID: ", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Number of roles: ", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Members: ", value=len(ctx.message.server.members))
        embed.add_field(name='Currently online', value=online)
        embed.add_field(name="Server created at: ", value=ctx.message.server.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'), inline=True)
        embed.add_field(name="Channel crated at: ",value=ctx.message.channel.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'), inline=True)
        embed.add_field(name="Current channel: ",value=ctx.message.channel, inline=True)
        embed.add_field(name="Server owner's name: ",value=ctx.message.server.owner.mention, inline=True)
        embed.add_field(name="Server owner's status: ",value=ctx.message.server.owner.status, inline=True)
        embed.add_field(name="Server region: ",value=ctx.message.server.region, inline=True)
        embed.add_field(name='Moderation level', value=str(ctx.message.server.verification_level))
        embed.add_field(name='Number of emotes', value=str(emoji_count))
        embed.add_field(name='Highest role', value=ctx.message.server.role_hierarchy[0])
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_author(name=ctx.message.server.name, icon_url=ctx.message.server.icon_url)
        await client.say(embed=embed)
    else:
        return False

@client.command(pass_context = True)
async def ban(ctx, member: discord.Member, days: int, *, reason : str = None):
    if ctx.message.author.server_permissions.administrator:
        if reason == "None":
            reason = "(No reason logged!)"
        await client.send_message(member, "You got banned from this server {} for {} days for this reason: **{}**".format(ctx.message.server.name, days ,reason)) 
        await client.say(":white_check_mark: I banned this member! :thumbsup:")
        await client.ban(member, days)
    else:
        await client.say("You need Admin perms to use this :x:")

@client.event
async def on_message(message) :
   # if message.channel.type == discord.ChannelType.private:

    global help_command
    global bypass_list
    global chat_filter
    await client.process_commands(message)
    contents = message.content.split(" ")
    for word in contents:
        if word.upper() in help_command:
            if not message.author.id in bypass_list:
                try:
                    await client.send_message(message.author, "Thanks for contacting us! In a few minutes, one of our staff members will contact you! Please be patient! :white_check_mark:")
                except:
                    await client.send_message(message.author, ":x: Sorry, but I can't recognise that command! Please try using ``Help me`` or ``I need help``!")
                    

@client.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.private:
        global help_command
        await client.process_commands(message)
        content = message.content.split(" ")
        for word in content:
            if word.upper() in help_command:
                if not message.author.id in bypass_list:
                    try:
                        await client.send_message(message.author, "Thanks for contacting us! In a few minutes, one of our staff members will contact you! Please be patient! :white_check_mark:")
                        channel = discord.Object(id='539906456972165121')
                        await client.send_message(channel, "<@&356865020799221771>, <@&536498409104998400>, <@&353967662583513089>, {}, needs help! Please DM him/her about his/her problem(s)!".format(message.author))
                    except:
                        await client.send_message(message.author, ":x: Sorry, but I can't recognise that command! Please try using ``Help me`` or ``I need help``!")
                else:
                    return
            else:
                await client.send_message(message.author, ":x: Sorry, but I can't recognise that command! Please try using ``Help``!")



client.run("NTM5NDYyMTQxODQxODk5NTM2.DzCs8Q.1YK599IavzZ4JnkFmumyApTE4CA")
#client.run(os.environ.get('TOKEN'))