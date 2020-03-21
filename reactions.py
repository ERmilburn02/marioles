import asyncio, json, aiohttp, time, datetime, os
import endpoints

async def reactionsMain(data):
    try:
        if data['d']['channel_id'] == "672245817440075786" and data['d']['emoji']['id'] == "681316576397754411":
            m = await endpoints.get_all_reacs(data['d']['channel_id'], data['d']['message_id'], "%3Acoindenied%3A681316576397754411")
            if len(m) > 9:
                await endpoints.del_message(data['d']['channel_id'], data['d']['message_id'])



    except Exception as ex:
        print('Error:', ex)
        with open('log.log', 'a') as log:
            log.write(str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())) + f' [Crash Reactions]: {ex}\n')