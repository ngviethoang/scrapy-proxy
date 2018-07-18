# -*- coding: utf-8 -*-
""" Calculate proxies' run time and update to database """

import pymongo
from crawl_proxy.custom_settings import mongo_settings
import aiohttp
import asyncio
from datetime import datetime

mongo_uri = mongo_settings['URI']
mongo_db = mongo_settings['DATABASE']
collection_name = mongo_settings['PROXIES_COLLECTION']

client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]


# get newest proxies from database
def get_proxies(limit):
    find = {}  # run all proxies
    find = {'run_time': {'$ne': 100}}  # run unprocessed and good proxies only
    # find = {'run_time': None}  # only run unprocessed proxies

    proxies = db[collection_name].find(find).sort([('updated_at', -1)]).limit(limit)
    proxies = [proxy['proxy'] for proxy in proxies]

    return proxies


# update proxy's run time to database
def update_proxy(proxy, run_time):
    print('{} {}'.format(proxy, run_time))

    db[collection_name].update_one(filter={'proxy': proxy},
                                   update={'$set': {'run_time': run_time, 'updated_at': datetime.now()}})


# send request to get proxy's run time
async def fetch(session, proxy):
    start_time = datetime.now()

    try:
        async with session.get(url='https://www.amazon.com/', proxy=proxy):
            run_time = datetime.now() - start_time
            run_time = run_time.seconds

            update_proxy(proxy, run_time)

    except (aiohttp.client_exceptions.ClientError, asyncio.TimeoutError) as e:
        print('{} {}'.format(proxy, e))
        update_proxy(proxy, 100)


# Getter function with semaphore.
async def bound_fetch(sem, session, proxy):
    async with sem:
        await fetch(session, proxy)


# send all requests with proxies list
async def fetch_all(proxies):
    tasks = []

    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    conn = aiohttp.TCPConnector(
        limit=1000,
        use_dns_cache=False,
        ssl=False
    )

    async with aiohttp.ClientSession(connector=conn, conn_timeout=20) as session:
        for proxy in proxies:
            task = asyncio.ensure_future(bound_fetch(sem, session, proxy))
            tasks.append(task)  # create list of tasks

        await asyncio.gather(*tasks)  # gather task responses


if __name__ == '__main__':
    proxies = get_proxies(0)
    print(len(proxies))

    start_time = datetime.now()

    loop = asyncio.get_event_loop()  # event loop
    loop.set_debug(True)

    future = asyncio.ensure_future(fetch_all(proxies))  # tasks to do

    loop.run_until_complete(future)  # loop until done
    loop.close()

    run_time = datetime.now() - start_time
    print('Run time: {}'.format(run_time))
