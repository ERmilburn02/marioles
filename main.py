import asyncio, json, aiohttp, time, datetime, random, inspect
import endpoints, messages, reactions, variables
keepConnection = True
variables.mRestart = datetime.datetime.now()
print("Mario Royale Bot")

async def start(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
                async for msg in ws:
                    data = json.loads(msg.data)
                    if data["op"] == 10:
                        asyncio.create_task(heartbeat(ws, data['d']['heartbeat_interval']))
                        await ws.send_json({"op":2,"d":{"token":open('token.txt').read(),
                        "properties":{},
                                "compress":False,
                                "large_threshold":250,
                                "presence":{
                                    "game":{
                                        "name":"Arpy do all the work",
                                        "type": 3
                                    }
                                }}})

                    if data['op'] == 0:


                        seq = data['s']


                        if data['t'] == 'READY':
                            sessionid = data['d']['session_id']
                            variables.aRestart = datetime.datetime.now()


                        elif data['t'] == "MESSAGE_CREATE" and 'bot' not in data['d']['author'] and 'webhook_id' not in data['d']['author']:
                            await messages.messagesMain(data)

                        
                        elif data['t'] == "MESSAGE_REACTION_ADD":
                            await reactions.reactionsMain(data)


                    if data['op'] == 6:
                        {
                            "token": open('token.txt').read,
                            "session_id": sessionid,
                            "seq": seq
                        }


                    elif data['op'] == 9:
                        await ws.send_json({"op":2,"d":{"token":open('token.txt').read(),
                        "properties":{},
                                "compress":False,
                                "large_threshold":250,
                                "presence":{
                                    "game":{
                                        "name": 'Arpy do all the work',
                                        "type": 3
                                    }
                                }}})



    except Exception as ex:
        messages.handle_exception(ex, inspect.currentframe().f_code.co_name)






####################################
###Ha, ha, ha, ha. Stayin' alive!###
async def heartbeat(ws, interval):
    while keepConnection:
        await asyncio.sleep(interval/1000)
        await ws.send_json({"op":1,"d": 0})
async def main():
    response = await endpoints.api_call("/gateway")
    await asyncio.shield(start(response["url"]))
####################################

while (True):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close
