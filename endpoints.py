import asyncio, json, aiohttp, variables
token = open('token.txt').read()
async def api_call(path, method="GET", reason = '', **kwargs):
    defaults = {"headers":{"Authorization": f"Bot {token}", "Content-Type": "application/json", "X-Audit-Log-Reason": f"{reason}"}}
    kwargs = dict(defaults, **kwargs)
    async with aiohttp.ClientSession() as session:
        response = await session.request(method, "https://discordapp.com/api"+path, **kwargs)
        try:
            return await response.json()
        except:
            return response.reason

async def typing(channel):
    return await api_gate(f"/channels/{channel}/typing", "POST")

async def message(channel, content, url=""):
    return await api_gate(f"/channels/{channel}/messages", "POST", json={"content": content, "image":{"url": url}})

async def del_message(channel, message):
    return await api_gate(f"/channels/{channel}/messages/{message}", "DELETE")

async def fetch_message(channel, around):
    return await api_gate(f"/channels/{channel}/messages/{around}", "GET")

async def fetch_messages(channel, message, limit=2, which="before"):
    '''when = "before" | "around" | "after" message ID'''
    return await api_gate(f"/channels/{channel}/messages", "GET", params={'limit': limit, which: message})

async def fetch_server(guild):
    return await api_gate(f"/guilds/{guild}", "GET")

async def add_role(guild, user, role):
    return await api_gate(f"/guilds/{guild}/members/{user}/roles/{role}", "PUT")

async def rem_role(guild, user, role):
    return await api_gate(f"/guilds/{guild}/members/{user}/roles/{role}", "DELETE")

async def embed(channel, content, embed):
    return await api_gate(f"/channels/{channel}/messages", "POST", json={"content": content, "embed": embed})

async def add_reaction(channel, message, emoji):
    return await api_gate(f"/channels/{channel}/messages/{message}/reactions/{emoji}/@me", 'PUT')

async def dm_message(recepient_id):
    return await api_gate(f"/users/@me/channels", "POST", json={"recipient_id": recepient_id})

async def kick_user(guild, user, reason):
    return await api_gate(f"/guilds/{guild}/members/{user}", "DELETE", f"{reason}")

async def ban_user(guild, user, reason):
    return await api_gate(f"/guilds/{guild}/bans/{user}?reason={reason}", "PUT", f"{reason}")

async def fetch_channel(channel):
    return await api_gate(f"/channels/{channel}", "GET")

async def fetch_user(guild, user):
    return await api_gate(f"/guilds/{guild}/members/{user}", "GET")

async def get_all_guilds():
    return await api_gate(f"/users/@me/guilds", "GET")

async def api_gate(path, method="GET", reason = '', **kwargs):
    if variables.lock is False:
        k = await api_call(path, method, reason, **kwargs)
        if 'retry_after' in k:
            variables.lock = True
            await asyncio.sleep(k["retry_after"]/1000)
            variables.lock = False
            return await api_gate(path, method, reason, **kwargs)
        else:
            return k
    else:
        await asyncio.sleep(1)
        return api_gate(path, method, reason, **kwargs)