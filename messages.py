import asyncio, json, aiohttp, time, datetime, re, random, inspect
import endpoints, variables



version = "1.0.2.1"

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
        if data['d']['guild_id'] == '682024034418163819':
            reg = re.search(r'\A\,switch .+', data['d']['content'])
            characterList = {
                'player': '683364722749472859',
                'mario': '682111141844877323',
                'luigi': '682111395697000459',
                'peach': '682111445068283905',
                'toad': '682111230525440149',
                'waluigi': '682121852314845184',
                'wario': '682409568470695941'
            }
            if reg != None:
                m = data['d']['content'].split(" ", 1)[1:]
                if m[0].lower() in characterList:
                    valid = True
                else:
                    valid = False
            else:
                valid = False

            
            
            remRoles = []
            for elem in data['d']['member']['roles']:
                for i in characterList.values():
                    if elem == i:
                        remRoles.append(elem)

            for elem in remRoles:
                await endpoints.rem_role("682024034418163819", data['d']['author']['id'], elem)

            if valid == True:
                role = characterList[m[0].lower()]
                t = f"<@{data['d']['author']['id']}>, you have switched your character to **{m[0].lower()}**!"

            else:
                char, role = random.choice(list(characterList.items()))
                t = f"<@{data['d']['author']['id']}>, you let your fate decide, and became **{char}**!"

                
            await endpoints.add_role("682024034418163819", data['d']['author']['id'], role)
            await endpoints.message(data['d']['channel_id'], t)

    except Exception as ex:
        handle_exception(ex, inspect.currentframe().f_code.co_name)



commandList = {
    "general":{
        "switch": {
            "code": characterSelect,
            "help": {
                "name": ",switch [Player/Mario/Luigi/Peach/Toad/Yoshi/Waluigi/Wario]",
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