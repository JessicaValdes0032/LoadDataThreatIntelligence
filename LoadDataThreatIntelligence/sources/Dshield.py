import ipaddress
import re
import json
import pandas

link_dshield_30d = "https://iplists.firehol.org/files/dshield_30d.netset"
ip_expresion = "^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"


async def request_dshield(session):
    try:
        ips_list = []

        async with session.get(link_dshield_30d) as response:
            text = (await response.read()).decode("utf-8").strip()

            for line in text.split('\n'):
                if line.startswith('#'):
                    continue
                for ip in ipaddress.IPv4Network(line):
                    ips_list.append(str(ip))

            return ips_list

    except Exception as e:
        print(e)


async def structuring_data(session):
    data = [{"tags": {
        "name": "IPs list",
        "category": "",
        "metadata": {'relationship': 'descriptive'}}
        , "objects": [
        ],
        "name": ''}]

    for ip in (await request_dshield(session)):
        data[0]["objects"].append({
                "name": ip,
                "type": "ip",
                "metadata": {}
            })

    return json.dumps(data)


# def sending_to_api(session):
#     async with session.post(, data:await structuring_data(session))
