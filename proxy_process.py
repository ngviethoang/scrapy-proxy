# -*- coding: utf-8 -*-
""" Calculate proxies' run time and update to database """

import aiohttp
import asyncio
from datetime import datetime
from crawl_proxy.helper.db import get_mysql_connection

db = get_mysql_connection()

test_url = 'https://www.teepublic.com/'


# get newest proxies from database
def get_proxies(limit=None):
    query = """
        SELECT ip FROM proxies
        WHERE response_time != 100 OR response_time IS NULL
    """

    if limit is not None:
        query += "LIMIT {}".format(limit)

    with db.cursor() as cursor:
        cursor.execute(query)

        proxies = cursor.fetchall()
        proxies = [p[0] for p in proxies]

    return proxies


# update proxy's run time to database
def update_proxy(proxy, response_time):
    print('{} {}'.format(proxy, response_time))

    with db.cursor() as cursor:
        cursor.execute("""
            UPDATE proxies 
            SET response_time = %s, updated_at = %s
            WHERE ip = %s
        """, (response_time, datetime.now(), proxy))

        db.commit()


# send request to get proxy's run time
async def fetch(session, proxy):
    start_time = datetime.now()

    try:
        async with session.get(url=test_url, proxy=proxy) as response:
            response_time = 100

            if response.status == 200:
                content = bytearray()
                while True:
                    chunk = await response.content.read(100)
                    if not chunk:
                        break
                    content += chunk
                content = content.decode('utf-8')

                if 'ROBOTS' not in content:
                    response_time = datetime.now() - start_time
                    response_time = response_time.microseconds / 1000000
                else:
                    print('captcha detected :(')

            update_proxy(proxy, response_time)

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
    sem = asyncio.Semaphore(100)

    conn = aiohttp.TCPConnector(
        limit=1000,
        use_dns_cache=False,
        ssl=False
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }

    async with aiohttp.ClientSession(connector=conn, conn_timeout=20, headers=headers) as session:
        for proxy in proxies:
            task = asyncio.ensure_future(bound_fetch(sem, session, proxy))
            tasks.append(task)  # create list of tasks

        await asyncio.gather(*tasks)  # gather task responses


if __name__ == '__main__':
    proxies = get_proxies()
    print(len(proxies))

    start_time = datetime.now()

    loop = asyncio.get_event_loop()  # event loop
    loop.set_debug(True)

    future = asyncio.ensure_future(fetch_all(proxies))  # tasks to do

    loop.run_until_complete(future)  # loop until done
    loop.close()
