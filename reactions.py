import asyncio, json, aiohttp, time, datetime, os
import endpoints

async def reactionsMain(data):
    try:

        joineableRoles = {
            "luigi": {
                "role": "504992224782843913",
                "text": " as Luigi",
                "color": "2ECC71"
            },
            "mario": {
                "role": "504992282584285184",
                "text": " as Mario",
                "color": "E74C3C"
            },
            "toad": {
                "role": "504992129685258250",
                "text": " as Toad",
                "color": "eed69e"
            },
            "peach1": {
                "role": "504992332857344000",
                "text": " as Peach",
                "color": "fd96eb"
            },
            "👍": {
                "role": "503985047758700574",
                "text": "",
                "color": "6a9bff"
            }
        }

        if data['d']['message_id'] == '658101700996890645' and "504993967046393866" in data['d']['member']['roles']:#Join
            if "504992224782843913" not in data['d']['member']['roles'] and "504992282584285184" not in data['d']['member']['roles'] and "504992129685258250" not in data['d']['member']['roles'] and "504992332857344000" not in data['d']['member']['roles'] and "503985047758700574" not in data['d']['member']['roles']:
                await endpoints.rem_role(data['d']['guild_id'], data['d']['user_id'], "504993967046393866")
                await endpoints.add_role(data['d']['guild_id'], data['d']['user_id'], joineableRoles[data['d']['emoji']['name']]['role'])
                await endpoints.embed('591311098427473940', '', {
                    "title": f"{data['d']['member']['user']['username']}#{data['d']['member']['user']['discriminator']} has Joined!",
                    "description": f"<@{data['d']['member']['user']['id']}> has joined{joineableRoles[data['d']['emoji']['name']]['text']}!",
                    "color":int(f"{joineableRoles[data['d']['emoji']['name']]['color']}", 16),
                    "footer":{
                        "text": f"{data['d']['user_id']}"
                    }
                })

    except Exception as ex:
        print('Error:', ex)
        with open('log.log', 'a') as log:
            log.write(str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())) + f' [Crash Reactions]: {ex}\n')