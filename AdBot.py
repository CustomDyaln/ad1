import discord
from discord.ext import commands
from discord.ext import tasks
from discord import Message
from discord import DMChannel
import json
import asyncio
import base64
import os
import requests
from requests.structures import CaseInsensitiveDict
import ctypes
from colorama import Fore, Back, Style
from colorama import init
init()

r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE



          
adbot = f"""

                                        {r}█████{w}╗ {r}██████{w}╗ {r}██████{w}╗  {r}██████{w}╗ {r}████████{w}╗
                                       {r}██{w}╔══{r}██{w}╗{r}██{w}╔══{r}██{w}╗{r}██{w}╔══{r}██{w}╗{r}██{w}╔═══{r}██{w}╗╚══{r}██{w}╔══╝
                                       {r}███████{w}║{r}██{w}║  {r}██{w}║{r}██████{w}╔╝{r}██{w}║   {r}██{w}║   {r}██{w}║   
                                       {r}██{w}╔══{r}██{w}║{r}██{w}║  {r}██{w}║{r}██{w}╔══{r}██{w}╗{r}██{w}║   {r}██{w}║   {r}██{w}║   
                                       {r}██{w}║  {r}██{w}║{r}██████{w}╔╝{r}██████{w}╔╝╚{r}██████{w}╔╝   {r}██{w}║   
                                       {w}╚═╝  ╚═╝╚═════╝ ╚═════╝  ╚═════╝    ╚═╝

      {Fore.CYAN}                       ╔═════════════════════════[{Style.RESET_ALL}AdBot{Fore.CYAN}]════════════════════════╗
                             ║ {Fore.MAGENTA}Version: {Style.RESET_ALL}1.1{Fore.CYAN}                                           ║
                             ║ {Fore.MAGENTA}Created By: {Style.RESET_ALL}Daddy Lazarus{Fore.CYAN}                              ║
      {Fore.CYAN}                       ╚════════════════════════════════════════════════════════╝
      
      
"""
ctypes.windll.kernel32.SetConsoleTitleW("Loading AdBot...")
with open('config.json', "rb") as infile:
    config = json.load(infile)
    token = config["userdata"].get('token')
    channelids = config["userdata"].get('channelids')
    hours = config["userdata"].get('hours')

if token == "null":
    os.system('cls')
    unset = True
    while unset == True:
        print(Fore.RED + "Error: " + Style.RESET_ALL + "No local userdata found!")
        token = input("Please enter your discord token: ")
        url = "https://canary.discord.com/api/v9/users/@me"

        headers = CaseInsensitiveDict()
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        headers["authorization"] = token

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            while unset == True:
                try:
                    hours = int(input("Hours: "))
                    oldmessagevalue = config["userdata"].get('message')
                    oldchannelidsvalue = config["userdata"].get('channelids')
                    update = {"userdata": {"token": token,"hours": hours,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                    config.update(update)
                    with open('config.json', "w") as jsfile:
                        json.dump(config, jsfile)
                        jsfile.close()
                    unset = False
                except:
                    print(Fore.RED + "Error: " + Style.RESET_ALL + "Must be integer value!")
        else:
            print(Fore.RED + "Error: " + Style.RESET_ALL + "Invalid token!")
else:
    pass


ABT = commands.Bot(command_prefix = "?", self_bot=True, loop=None)

# Auto DM Reply
def autoReply():
    check = requests.get('https://discord.com/api/v10/users/@me', headers={'Authorization': token})
    if check.status_code == 200:
        lol = json.loads(check.text)
        if lol['id'] != '0':
            a = requests.get('https://discord.com/api/v10/users/@me/channels', headers={'Authorization': token})
            b = json.loads(a.text)
            for i in b:
                try:
                    if i['type'] == int(1):
                        c = requests.get(f'https://discord.com/api/v10/channels/{i["id"]}/messages', headers={'Authorization': token})
                        d = json.loads(c.text)
                        if d[0]['author']['id'] != lol['id']:
                            requests.post(f'https://discord.com/api/v10/channels/{i["id"]}/messages', headers={'Authorization': token}, json={'content': config["userdata"].get('DmMessage')})                        
                            break
                except:
                    pass
def autoReplyLoop():
    while 1:
        autoReply()

# DM Deleter / Closer
def deleteDMs():
    a = requests.get('https://discord.com/api/v10/users/@me/channels', headers={'Authorization': token})
    b = json.loads(a.text)
    for i in b:
        try:
            if i['type'] == int(1):
                requests.delete(f'https://discord.com/api/v10/channels/{i["id"]}', headers={'Authorization': token})
                break
        except:
            pass

# Advertiser menu
def advertiser():
    while 1:clearConsole();choice=input(Fore.RED+"Advertiser:\n"+Fore.YELLOW+"1. Start advertiser\n2. Add channel\n3. Remove channel\n4. Change message\n5. Change delay\n6. Change DM Response\n7. Auto DM Response\n8. Leave\n");{'1':lambda:sendMessage(),'2':lambda:modifyChannels('add'),'3':lambda:modifyChannels('remove'),'4':lambda:changeMessage(),'5':lambda:changeDelay(),'6':lambda:changeDMResponse(),'7':lambda:(threading.Thread(target=autoReplyLoop).start(),print("Started Auto DM Responder")),'8':lambda:main()}.get(choice,lambda:print('Invalid choice'))();time.sleep(3)
def main():
    while 1:clearConsole();deleteDMs();choice=input(Fore.RED+"Home:\n"+Fore.YELLOW+"1. Advertiser\n2. Onliner\n3. Leave\n");{'1':advertiser,'2':onliner,'3':lambda:exit()}.get(choice,lambda:print('Invalid choice'))();time.sleep(3)


@ABT.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW("AdBot v1.1")
    os.system('cls')
    print(adbot + Style.RESET_ALL)
    print('Logged in as ' + Fore.RED + f'{ABT.user.name}#{ABT.user.discriminator}' + Style.RESET_ALL)
    advertise.start()
    main()
    advertiser()      

@tasks.loop(hours=int(hours))
async def advertise():
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        channelstosend = config["userdata"].get('channelids')
    if "null" in channelstosend:
        pass
    else:
        for i in channelstosend:
            try:
                decodedmsg = base64.b64decode(config["userdata"].get('message'))
                await ABT.get_channel(int(i)).send(decodedmsg.decode('utf-8'))
                print(f"{Fore.CYAN}[{Fore.MAGENTA}INFO{Fore.CYAN}]{Style.RESET_ALL} Successfully sent advertisment to channel id '{i}'!")
            except:
                print(f"{Fore.CYAN}[{Fore.MAGENTA}INFO{Fore.CYAN}]{Style.RESET_ALL} Could not send to channel id '{i}', removing from list...")
                with open('config.json', "rb") as infile:
                    config = json.load(infile)
                oldtokenvalue = config["userdata"].get('token')
                oldmessagevalue = config["userdata"].get('message')
                oldchannelidsvalue = config["userdata"].get('channelids')
                oldhoursvalue = config["userdata"].get('hours')
                oldchannelidsvalue.remove(i)
                update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                config.update(update)
                with open('config.json', "w") as jsfile:
                    json.dump(config, jsfile)
                    jsfile.close()

@ABT.command()
async def removechannel(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    oldchannelidsvalue.remove(id)
    update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()

@ABT.command()
async def addchannel(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    if oldchannelidsvalue == "null":
        update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": [id]}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    else:
        oldchannelidsvalue.append(id)
        update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()

@ABT.command()
async def setmsg(ctx, *, msg):
    await ctx.message.delete()
    encodedmsg = str(base64.b64encode(bytes(msg, 'utf-8')))[2:-1]
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": encodedmsg,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()


ABT.run(token, bot=False)
input()
