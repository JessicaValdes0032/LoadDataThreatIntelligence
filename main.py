import asyncio
import os.path
from datetime import datetime
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from LoadDataThreatIntelligence.database import database
from datetime import datetime

from LoadDataThreatIntelligence.sources import Dshield


async def main():
    async with aiohttp.ClientSession() as session:
        print(await Dshield.structuring_data(session))

scheduler = AsyncIOScheduler()

# Schedule to run the task on every third Friday of February, March, April, November, and December at 2 a.m., 3 a.m.,
# 4 a.m., and 5 a.m.:

scheduler.add_job(main, 'cron', month='2-4,11-12', day='3rd fri', hour='2-5', next_run_time=datetime.now())

scheduler.start()
asyncio.get_event_loop_policy().get_event_loop().run_forever()


