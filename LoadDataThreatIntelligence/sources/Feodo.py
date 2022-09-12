import asyncio
import json

import aiohttp
import pandas

url_botnet_c2_ip_blocklist = "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json"
url_botnet_c2_indicators_of_compromise = "https://feodotracker.abuse.ch/downloads/ipblocklist.json"


async def request_feodo(session, url):

    try:
        async with session.get(url) as response:
            return json.loads((await response.read()).decode('utf8'))

    except Exception as e:
        print(e)


async def structuring_data(session, url):
    data = [{"objects": [],
        "tags": {
        "name": "Botnet C2 IPs",
        "category": "Botnet",
        "metadata": {'relationship': 'descriptive'}
        }
        }]

    for ip in (await request_feodo(session, url)):
        name = ip['ip_address']
        del ip['ip_address']
        data[0]["objects"].append({
                "name": name,
                "type": "ip",
                "metadata": ip
            })
    print(len(data[0]['objects']))
    return json.dumps(data)


async def main():
    async with aiohttp.ClientSession() as session:
        print(await structuring_data(session, url_botnet_c2_indicators_of_compromise))

asyncio.get_event_loop_policy().get_event_loop().run_until_complete(main())
