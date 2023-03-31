import discord
import os
import random
import asyncio
import time
import randfacts
import json
import glob
import dataIO
import requests
import discord_interactions
#---------------------Discord--------------------
from discord import Client, Intents, Embed
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from typing import Optional
from requests.auth import HTTPBasicAuth
from aiohttp import request
from aiohttp import BasicAuth
from discord.ext.commands import MinimalHelpCommand
#------------------------------------------------
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from time import sleep
from os import path


os.chdir("/home/Guest/FurSec/furry_security")


mainshop = [{"name":"Old_PC","price":500,"description":"This PC sucks but you can play old games on it and get a feeling of nostalgia"},
            {"name":"Potato_PC","price":1000,"description":"This PC still sucks but it can run more games!"},
            {"name":"Medium_PC","price":2000,"description":"This PC is pretty good but still can't run the top tier games"},
            {"name":"Best_PC","price":4000,"description":"This PC can run every game but it sadly has no RGB which means lower FPS!"},
            {"name":"Best_PC (with RGB)","price":5000,"description":"This PC can run every game and has alot more FPS because of RGB"},
            {"name":"NASA_PC","price":200000,"description":"This PC can run everything at the highest FPS, it has RGB and the best components!"},
            {"name":"Alien_PC","price":1000000,"description":"a̴̛̜̮͈̿̚d̴̻̗̙̔́̾z̵̹̈́ṣ̶͚͂7̸̥̅͊͒8̷̩͕̑͜f̸̛̬̗6̶̡̬̅͂ś̸̯̹͖f̶͓͔͚͘̚ǧ̵͔̫̅ṡ̴̠̞̠̇7̸̥́̑͐ͅ!"}]

intents = discord.Intents.all()

reddit = praw.Reddit(client_id='s-PoBApuWL-Rmg',
                     client_secret='IonsVCxPhoB7lxmuMOlUXv0oo0KEuw',
                     user_agent='furry_irl')

intents.members = False

load_dotenv()
client = commands.Bot(command_prefix=['fs! ','fs!'], intents=Intents.all())

client.remove_command('help')

client.remove_command('lovetest')

with open('./furry_security/statements.txt', 'r+') as file:
    statements = json.load(file)
with open('./furry_security/responses.txt', 'r+') as file:
    responses = json.load(file)
current_statement = statements[random.randint(0, len(statements)-1)]

token = ""
#--------------------------------------------------------------Furry Security bot---------------------------------------------------------------------------


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Protecting the furs!'))
    print('Bot is online')


role = "------Member----"


@client.event
async def on_member_join(member):
    welcomes = [f'**{member.mention}** just got summoned in Le Furry Hideout',
                f'**{member.mention}** got here thorugh a Transfur!',
                f'Welcome to the best Furry Server **{member.mention}**!']

    ch = client.get_channel(838849651725565993)
    await ch.send(f'{random.choice(welcomes)}!')

@client.command()
async def ping(ctx):
    print('Ping was used')
    await ctx.send(f'Bot ping: {round(client.latency * 1000)}ms')

@client.command()
async def help(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(
        title='Commands for Furs :3 \n \nPrefix: fs! \n \nFun Commands: \nfun'
              ' \n \nReddit Commands(CURRENTLY UNAVAILABLE): \nreddit'
              ' \n \nInteraction: \ninteract \n \nMod commands: \nmod \n \nUseful commands: \nuseful'
              ' \n \nMusic Commands: \nmusic \n \nEconomy: \neco',
        color=discord.Color.green())
    await ctx.send(embed=embed)


@client.command()
async def fun(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(
        title='Fun Commands: \n \n8ball (Question) \nCoin \nDice \nLovetest (someone) \nGayrate \nsimprate \nfact',
        color=discord.Color.green())
    await ctx.send(embed=embed)

@client.command()
async def reddit(ctx):
    print('unv was used')
    embed = discord.Embed(
        title='CURRENTLY UNAVAILABLE',
        color=discord.Color.red())
    await ctx.send(embed=embed)

#@client.command()
#async def redcmd(ctx):
#    print('cmdhelp was used')
#    embed = discord.Embed(
#        title='Fun Commands: \n \nmeme (sends a r/memes meme) \nfurmeme (sends a r/furry meme) \nmeme_irl (sends a r/furry_irl meme)',
#        color=discord.Color.green())
#    await ctx.send(embed=embed)

@client.command()
async def interact(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(
        title='Interactive Commands: \n \nhug (someone) \nkiss (someone) \npat (someone)',
        color=discord.Color.green())
    await ctx.send(embed=embed)

@client.command()
async def mus(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(
        title='Music commands: \n \nplay (URL) \npause \nresume \nstop \nleave',
        color=discord.Color.green())
    await ctx.send(embed=embed)

@client.command()
async def eco(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(
        title='Economy commands: \n \nbalance \nbeg (beg for money) \nslots (amount of money to bet) \nwithdraw(w or wd also works) \ndeposit(d or dep also works) \ngive [user]',
        color=discord.Color.green())
    await ctx.send(embed=embed)

#------------------------------------------------------ECONOMY SYSTEM--------------------------------------------------------

@client.command(aliases=['bal'])
async def balance(ctx, member:discord.Member = None):

    if not member:
        member = ctx.author

    await open_account(member)

    user = member

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{member.name}'s balance",color = discord.Color.red())
    em.add_field(name = "Wallet",value = f"{wallet_amt}$")
    em.add_field(name = "Bank",value = f"{bank_amt}$")
    
    await ctx.send(embed = em)

@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(1, 41)

    if earnings == 0:
        await ctx.send(f"No luck today :(")
    else:
        await ctx.send(f"Someone gave you {earnings}$!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(180, 201, 2)

    await ctx.send(f"You made {earnings}$!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = round(error.retry_after, 0)
        convert = time.strftime("%M", time.gmtime(seconds))
        await ctx.send(f'You can work again in {convert} minutes.')

@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = round(error.retry_after, 0)
        convert = time.strftime("%M", time.gmtime(seconds))
        await ctx.send(f'You can beg again in {convert} minutes.')


async def open_account(user):
    
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["bag"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)

    return users

#withdraw
@client.command(aliases=['w','wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount to withdraw!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You don't have any money to withdraw!")
        return
    if amount<0:
        await ctx.send("Amount too low!")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"You withdrew {amount}$")

#deposit
@client.command(aliases=['d', 'dep'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount to deposit!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    print(amount, bal)
    if amount>bal[0]:
        await ctx.send("You don't have any money to deposit!")
        return
    if amount<0:
        await ctx.send("Amount too low!")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"You deposited {amount}$")

#give
@client.command()
async def give(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the amount you want to give!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You don't have any money in your bank!")
        return
    if amount<0:
        await ctx.send("Amount too low!")
        return

    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"You gave {amount}$ to {member}")

#slots
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter how much money you wanna bet!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much money!")
        return
    if amount<0:
        await ctx.send("Amount too low!")
        return

    final = []
    for i in range(3):
        a = random.choice([":red_circle:",":blue_circle:",":green_circle:",":yellow_circle:",":orange_circle:",":purple_circle:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author,2*amount)
        await ctx.send("You won!")
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("You lost...")

#update_bank
async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    print("Change:", change)
    print("Users:", users[str(user.id)][mode])

    if change == "":
        change = 0

    users[str(user.id)][mode] = int(users[str(user.id)][mode]) + int(change)

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"],users[str(user.id)]["bag"]]
    return bal

@client.command()
async def shop(ctx):
    em = discord.Embed(title ="Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name,value = f"\n{price}$ | {desc}", inline = "\n\n\nCommand use:\n\nTo buy something use **fs!buy [item_name]**,\nto check your inventory type **fs!bag**")

    await ctx.send(embed = em)

@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title = "Bag")

    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)

#buy_this
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*int(amount)

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<int(cost):
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    print("Cost:", cost)
    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

#----------------------------------------------------ECONOMY SYSTEM END------------------------------------------------------

#--------------------------------------------------------CHAT BOT----------------------------------------------------------------

# pulled from https://github.com/DiskKun/hello-bot/blob/master/discord-version/main.py on 31.03.2023

@client.command()
async def chat(message, *, args):
    global current_statement
    randomAssStringValue = "".join(args)
    randomAssStringValue = randomAssStringValue.strip()
    

    ## BOT CODE
    print(args)
    print(randomAssStringValue)
    usrinput = randomAssStringValue.lower()
    is_in_s = usrinput in statements
    if is_in_s == True:
        if usrinput in responses.keys():
            value = random.choice(responses[usrinput])
            await message.channel.send(value)
            current_statement = value
        else:
            current_statement = statements[random.randint(0, len(statements)-1)]
            await message.channel.send(current_statement)
    else:
        statements.append(usrinput)
        responses.setdefault(current_statement, [])
        if usrinput in responses[current_statement]:
            pass
        else:
            responses[current_statement].append(usrinput)
        current_statement = statements[random.randint(0, len(statements)-1)]
        await message.channel.send(current_statement)
    jstatements = json.dumps(statements)
    jresponses = json.dumps(responses)
    with open('./furry_security/statements.txt', 'w+') as file:
        file.write(jstatements)
    with open('./furry_security/responses.txt', 'w+') as file:
        file.write(jresponses)

#----------------------------------------------------CHAT BOT END------------------------------------------------------

@client.command()
@commands.has_permissions(kick_members=True)
async def modcmd(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(title='Mod Commands: \n \nKick (User) \nBan (User) \nClear (amount) \nUnban (User)',
                          color=discord.Color.green())
    await ctx.send(embed=embed)

@client.command()
async def usecmd(ctx):
    print('cmdhelp was used')
    embed = discord.Embed(title='Useful Commands: \n \nMath: \nPlus (num1) (num2) \nMinus (num1) (num2) \nMult (num1) (num2) \nDiv (num1) (num2)',
                          color=discord.Color.green())
    await ctx.send(embed=embed)


@client.command(aliases=['8ball', 'eightball'])
@commands.cooldown(rate=1, per=5)
async def _8ball(ctx, *, question):
    print('8ball was used')
    responses = ['It is certain',
                 'It is decidedly so',
                 'Without a doubt',
                 'Yes – definitely',
                 'You may rely on it',
                 'As I see it, yes',
                 'Most likely',
                 'Outlook good',
                 'Yes',
                 'Signs point to yes',
                 'Reply hazy, try again',
                 'Ask again later',
                 'Better not tell you now',
                 'Cannot predict now',
                 'Concentrate and ask again',
                 'Don’t count on it',
                 'My reply is no',
                 'My sources say no',
                 'Outlook not so good',
                 'Very doubtful']
    embed = discord.Embed(title=f'Question: {question}\nAnswer: {random.choice(responses)}',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.is_nsfw()
async def cocksize(ctx):
    print('cocksize was used')
    responses = ['8D',
                 '8=D',
                 '8==D',
                 '8===D',
                 '8====D',
                 '8=====D',
                 '8======D',
                 '8=======D',
                 '8========D',
                 '8=========D',
                 '8==========D',
                 '8===========D',
                 '8============D',
                 '8=============D',
                 '8==============D',
                 '8===============D',
                 '8================D',
                 '8=================D',
                 '8==================D',
                 '8===================D']
    embed = discord.Embed(title=f"{message.author}'s cock size:\n{random.choice(responses)}",
                          color=discord.Color.red())
    await ctx.send(embed=embed)

#Calculator
@client.command()
async def plus(ctx, num, num2):
    print('plus was used')
    ans = f'{float(num) + float(num2)}'

    await ctx.send(f'{ans}')

@client.command()
async def minus(ctx, num, num2):
    print('plus was used')
    ans = f'{float(num) - float(num2)}'

    await ctx.send(f'{ans}')

@client.command()
async def mult(ctx, num, num2):
    print('plus was used')
    ans = f'{float(num) * float(num2)}'

    await ctx.send(f'{ans}')

@client.command()
async def div(ctx, num, num2):
    print('plus was used')
    ans = f'{float(num) / float(num2)}'

    await ctx.send(f'{ans}')

@client.command(aliases=['lover8', 'lovetest', '<3test'])
@commands.cooldown(rate=1, per=5)
async def _lover8(ctx, *, question):
    author_name = ctx.message.author.name
    print('lovetest was used')
    prc1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
            57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
            84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

    await ctx.send(f'The love between {author_name} and {question} is {random.choice(prc1)}%')

@client.command(aliases=['gayr8', 'gayrate'])
@commands.cooldown(rate=1, per=5)
async def _gayr8(ctx):
    author_name = ctx.message.author.name
    print('gayrate was used')
    prc1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
            57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
            84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

    embed = discord.Embed(title=f'{author_name} is {random.choice(prc1)}% gay',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command(aliases=['simpr8', 'simprate'])
@commands.cooldown(rate=1, per=5)
async def _simpr8(ctx):
    author_name = ctx.message.author.name
    print('simprate was used')
    prc1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
            57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
            84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

    embed = discord.Embed(title=f'{author_name} is {random.choice(prc1)}% a simp',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(rate=1, per=5)
async def dice(ctx):
    print('Dice was used')
    dice = ['1',
            '2',
            '3',
            '4',
            '5',
            '6']
    embed = discord.Embed(title=f'You rolled a {random.choice(dice)}!',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(rate=1, per=5)
async def fact(ctx):
    print('Random fact was used')
    rndf = randfacts.get_fact()
    embed = discord.Embed(title=f'{rndf}',
                        color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(rate=1, per=5)
async def coin(ctx):
    print('Coin was used')
    rollcn = ['Heads',
              'Tails']
    embed = discord.Embed(title=f'Your coin landed on {random.choice(rollcn)}!',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(rate=1, per=5)
async def poll(ctx,question):
    channel = ctx.channel
    msg = await client.get_message(message_id)
    await msg.add_reaction(':white_check_mark:')
    await msg.add_reaction(':negative_squared_cross_mark:')

#---------------------------------------Music----------------------------------------

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@client.command()
async def play(ctx, url):
    global queue
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()

        embed = discord.Embed(title=f'Bot is playing {url}',
                            color=discord.Color.blue()
                            )

        await ctx.send(embed=embed)

@client.command()
async def ytvid(ctx, url):
    video = pafy.new(url)
    value = video.getbest()

    embed = discord.Embed(title=f'{url}',
                          color=discord.Color.blue()
                          )
    embed.video(url=str(value))

    await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')

@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

#-------------------------------------------------------------------------------

#---------------------------------------------------------IMG CMDS---------------------------------------------------------

@client.command()
async def e926(ctx ,tags: Optional[str]):

    headers = {
        'User-Agent': 'ZeMangoFur',
    }

    try:
        args = (" ".join(map(str,tags)))
    except:
        print("No tags present")

    if tags == None:
        image_url = f"https://e926.net/posts.json?limit=100/"
    else:
        image_url = f"https://e926.net/posts.json?limit=100&tags={tags}"

    async with request("GET", image_url,auth=BasicAuth('ZeMangoFur', 'gGdhCpLpgwGsJ7m8aCMiz8z1'), headers=headers) as response:
        #await ctx.send(f"API returned a {response.status} status")
        try:
            if response.status == 200:
                data = await response.json()
                count = len(data['posts'])
                r = random.randrange(0,count)
                randomVarName = data['posts'][r]['id']
                score = data['posts'][r]['score']['total']
                width = data['posts'][r]['file']['width']
                height = data['posts'][r]['file']['height']
                ext = data['posts'][r]['file']['ext']
                image_link = data['posts'][r]['file']['url']
        except:
            image_link = None
            await ctx.send(f'There was no post containing the tags: {tags}')
            # await ctx.send(f"There was no post containing the tags: {tags}")
            return

        embed = discord.Embed(title=f"{tags}", description=f'[Link](https://e926.net/posts/{randomVarName}/) | Score: {score} | Width: {width} | Height: {height}', colour=discord.Color.from_rgb(8,12,36))
        embed.set_footer(text="e926", icon_url="https://static.wikia.nocookie.net/logopedia/images/0/0b/Logo_transparent.svg/revision/latest/scale-to-width-down/512?cb=20181119223528")
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)

        if ext == "webm":
            await ctx.send(image_link)

#nsfw
@client.command()
@commands.is_nsfw()
async def e621(ctx ,tags: Optional[str]):

    headers = {
        'User-Agent': 'ZeMangoFur',
    }

    try:
        args = (" ".join(map(str,tags)))
    except:
        print("No tags present")

    if tags == None:
        image_url = f"https://e621.net/posts.json?limit=100/"
    else:
        image_url = f"https://e621.net/posts.json?limit=100&tags={tags}"

    async with request("GET", image_url,auth=BasicAuth('ZeMangoFur', 'gGdhCpLpgwGsJ7m8aCMiz8z1'), headers=headers) as response:
        #await ctx.send(f"API returned a {response.status} status")
        try:
            if response.status == 200:
                data = await response.json()
                count = len(data['posts'])
                r = random.randrange(0,count)
                randomVarName = data['posts'][r]['id']
                score = data['posts'][r]['score']['total']
                width = data['posts'][r]['file']['width']
                height = data['posts'][r]['file']['height']
                ext = data['posts'][r]['file']['ext']
                image_link = data['posts'][r]['file']['url']
        except:
            image_link = None
            await ctx.send(f'There was no post containing the tags: {tags}')
            # await ctx.send(f"There was no post containing the tags: {tags}")
            return

        embed = discord.Embed(title=f"{tags}", description=f'[Link](https://e621.net/posts/{randomVarName}/) | Score: {score} | Width: {width} | Height: {height}', colour=discord.Color.from_rgb(8,12,36))
        embed.set_footer(text="e621", icon_url="https://static.wikia.nocookie.net/logopedia/images/0/0b/Logo_transparent.svg/revision/latest/scale-to-width-down/512?cb=20181119223528")
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)

        if ext == "webm":
            await ctx.send(image_link)

#--------------------------------------------------------IMG CMDS END------------------------------------------------------

@client.command()
async def meme_irl(ctx):
    memes_submissions = reddit.subreddit('furry_irl').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    e = discord.Embed(title=f'Meme requested by {ctx.author}', description=f'**IF NSFW INCLUDED DELETE IMMEDIATELY!** \nDesc: {submission.title}', color=0x1F)
    e.set_image(url=submission.url)

    await ctx.send(embed=e)

@client.command()
async def furmeme(ctx):
    memes_submissions = reddit.subreddit('furry').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    e = discord.Embed(title=f'Meme requested by {ctx.author}', description=f'**IF NSFW INCLUDED DELETE IMMEDIATELY!** \nDesc: {submission.title}', color=0x1F)
    e.set_image(url=submission.url)

    await ctx.send(embed=e)

@client.command()
async def meme(ctx):
    meme_subreddit = await reddit.subreddit('memes')
    memes_submissions = meme_subreddit.hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    e = discord.Embed(title=f'Meme requested by {ctx.author}', description=f'**IF NSFW INCLUDED DELETE IMMEDIATELY!** \nDesc: {submission.title}', color=0x1F)
    e.set_image(url=submission.url)

    await ctx.send(embed=e)

#---------------------------------------Interaction----------------------------------------

@client.command()
async def hug(ctx, *, member):
    author_name = ctx.message.author.name
    path = random.choice(os.listdir('C:\\Users\\justi\\Desktop\\Lel\\Furry Security\\TESTING BOT\\hugs'))
    hugs = [f'**{author_name}** warmly cuddles {member}!',
            f"**{author_name}** hugs {member} like they're their boyfriend!",
            f'**{author_name}** Runs to {member} and cuddles them as hard as possible!',
            f'**{author_name}** wraps around {member} and hugs them!',
            f'**{author_name}** looks at {member} and just gives them the biggest hug ever!!!']

    await ctx.send(f'{random.choice(hugs)}')
    await ctx.send(file=discord.File("C:\\Users\\justi\\Desktop\\Lel\\Furry Security\\TESTING BOT\\hugs\\"+path))


@client.command()
async def kiss(ctx, *, member):
    author_name = ctx.message.author.name
    kiss = [f'**{author_name}** goes near {member} and kisses them!',
            f'**{author_name}** kisses {member}!',
            f'**{author_name}** runs to {member} and kisses them as hard as possible!',
            f'**{author_name}** pushes {member} against a wall and kisses them!',
            f'**{author_name}** looks at {member} and just gives them the biggest kiss ever!!!']

    await ctx.send(f'{random.choice(kiss)}')

@client.command()
async def pat(ctx, *, member):
    author_name = ctx.message.author.name
    pats = [f'**{author_name}** goes near {member} and pats em!',
            f'**{author_name}** pats {member}!',
            f'**{author_name}** gives {member} a magical pat!',
            f'**{author_name}** gave {member} a pat through the screen!']

    await ctx.send(f'{random.choice(pats)}')

#------------------------------------------------------------------------------------------

@client.event
async def on_command_error(ctx, error):
    raise error
    print('Command_Error or Cooldown')
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Command doesn't exist or is written wrong",
                              color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=5)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"This command is on cooldown, try again after {round(error.retry_after)}s",
                              color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Insufficient Permissions",
                              color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=5)
    if isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(title="Command only for NSFW Channels!",
                              color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=5)

@client.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, amount: int):
    print('Clear was used')
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Cleared {amount} Messages!', delete_after=5)


@clear.error
async def clear_error(ctx, error):
    print('Clear_Error')
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='Please specify an amount of messages to delete',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

client.run(token)
