import asyncio, json, aiohttp, time, datetime, re, random, inspect
import endpoints, variables



version = "1.0.0.1"

def replaceMultiple(mainString, toBeReplaces, newString=""):
    for elem in toBeReplaces :
        if elem in mainString :
            mainString = mainString.replace(elem, newString)
    
    return  mainString

async def Invalid(data):
    pass

def handle_exception(context, pos):
    '''pos = inspect.currentframe().f_code.co_name'''
    msg = context
    print(f"WARNING: {msg}")
    with open('log.log', 'a') as log:
        log.write(str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())) + f' [{pos} Crash]: {msg}\n')

def even(imput):
    if (imput % 2) == 0:
        return True
    else:
        return False

async def info(data):
    try:
        await endpoints.typing(data['d']['channel_id'])
        await endpoints.embed(data['d']['channel_id'], f"<@{data['d']['author']['id']}>", {
                "color": int('cc5506', 16), #Orange
                "timestamp": data['d']['timestamp'],
                "title": "Here's some information about me:",
                "fields":[
                    {
                        "name": "Creator:",
                        "value": "Chrisoman#8561",
                        "inline": True
                    },
                    {
                        "name": "Developer:",
                        "value": "Eliza 🏳⚧#0001",
                        "inline": True
                    },
                    {
                        "name": "Version:",
                        "value": f"{version}",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": f"Mario Royale Bot"
                }
            })
        await endpoints.del_message(data['d']['channel_id'], data['d']['id'])
    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)


async def status(data):
    try:
        if data['d']['author']['id'] == "676511901890510848":
            mDeltaTime = datetime.datetime.now() - variables.mRestart
            mDeltaTime = str(mDeltaTime).split('.')
            aDeltaTime = datetime.datetime.now() - variables.aRestart
            aDeltaTime = str(aDeltaTime).split('.')
            guilds = await endpoints.get_all_guilds()
            await endpoints.message(data['d']['channel_id'], f"{str(time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))}\nManual Uptime: {mDeltaTime[0]}\nAutomatic Uptime: {aDeltaTime[0]}\nServers: {len(guilds)}\n{version}")
    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)


async def link(data):
    try:
        await endpoints.embed(data['d']['channel_id'], f"<@{data['d']['author']['id']}>", {
            "title": "MRoyale Link",
            "color": int('FFA500', 16),
            "description": "[Click here](https://mroyale.cyuubi.xyz)"
        })
        await endpoints.del_message(data['d']['channel_id'], data['d']['id'])
    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)


async def characterSelect(data):
    try:
        if data['d']['guild_id'] == '672229426272010281':
            a_message = data['d']['content'].split(' ', 1)
            characterList = {
                'player': {
                    'id': '689284795595096202',
                    'name': 'player'
                },
                'infringio': {
                    'id': '689247676315074570',
                    'name': 'infringio'
                },
                'mario': {
                    'id': '689190614583083137',
                    'name': 'mario'
                },
                'luigi': {
                    'id': '689190704408559736',
                    'name': 'luigi'
                },
                'peach': {
                    'id': '689190834633048079',
                    'name': 'peach'
                },
                'toad': {
                    'id': '689191236522737740',
                    'name': 'toad'
                },
                'yoshi': {
                    'id': '689191571681312801',
                    'name': 'yoshi'
                },
                'waluigi': {
                    'id': '689192145378082862',
                    'name': 'waluigi'
                },
                'wario': {
                    'id': '689191896337219655',
                    'name': 'wario'
                }
            }
            if a_message[0] == ",switch" and a_message[1].lower() in characterList:

                remRole = ''
                if characterList['player']['id'] in data['d']['member']['roles']:
                    remRole = characterList['player']['id']
                elif characterList['infringio']['id'] in data['d']['member']['roles']:
                    remRole = characterList['infringio']['id']
                elif characterList['mario']['id'] in data['d']['member']['roles']:
                    remRole = characterList['mario']['id']
                elif characterList['luigi']['id'] in data['d']['member']['roles']:
                    remRole = characterList['luigi']['id']
                elif characterList['peach']['id'] in data['d']['member']['roles']:
                    remRole = characterList['peach']['id']
                elif characterList['toad']['id'] in data['d']['member']['roles']:
                    remRole = characterList['toad']['id']
                elif characterList['yoshi']['id'] in data['d']['member']['roles']:
                    remRole = characterList['yoshi']['id']
                elif characterList['waluigi']['id'] in data['d']['member']['roles']:
                    remRole = characterList['waluigi']['id']
                elif characterList['wario']['id'] in data['d']['member']['roles']:
                    remRole = characterList['wario']['id']
                

                await endpoints.rem_role("672229426272010281", data['d']['author']['id'], remRole)
                await endpoints.add_role("672229426272010281", data['d']['author']['id'], characterList[a_message[1].lower()]['id'])
                await endpoints.message(data['d']['channel_id'], f"<@{data['d']['author']['id']}>, you have switched your character to **{characterList[a_message[1].lower()]['name']}**!")
    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)




commandList = {
    "general":{
        "switch": {
            "code": characterSelect,
            "help": {
                "name": ",switch [Player/Infringio/Mario/Luigi/Peach/Toad/Yoshi/Waluigi/Wario]",
                "value": "Changes your character role"
            }
        },
        "info": {
            "code": info,
            "help": {
                "name": ",info",
                "value": "Displays information about the bot"
            }
        },
        "link": {
            "code": link,
            "help": {
                "name": ",link",
                "value": "Get the link for MRoyale"
            }
        }
    },
    "fun":{
    },
    "moderation":{
    },
    "utility":{
        "status": {
            "code": status
        },
    },
    "code":{
        ",switch": characterSelect,
        ",info": info,
        ",status": status,
        ",link": link
    }
}


async def messagesMain(data):
    try:


        if 'guild_id' not in data['d']: #Check if DM
            pass

        else: #If not DM
            message = data['d']['content'].split(" ")
            await commandList['code'].get(message[0], Invalid)(data)


    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)