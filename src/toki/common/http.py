import asyncio
from aiohttp import ClientSession
from typing import List

MAX_SIM_CONNS = 50


async def fetch(url, session: ClientSession):
    """
    Fetch the response from URL

    :param string url:
    :param session:
    :return:
    """
    async with session.get(url) as response:
        items = await response.json()
        return {
            "items": items,
            "url": url
        }


async def bound_fetch(sem: asyncio.Semaphore, url: str, session: ClientSession):
    """
    Ensure working with SEMAPHORE a bunch of tasks

    :param asyncio.Semaphore sem:
    :param str url:
    :param ClientSession session:
    :return:
    """
    async with sem:
        return await fetch(url, session)


async def fetch_all(url_list: List[str]):
    """
    create async scrapper with possibility to download data for batch of url

    :param url_list:
    :return:
    """
    tasks = []
    async with ClientSession() as session:
        sem = asyncio.Semaphore(MAX_SIM_CONNS)
        for url in url_list:
            # task = asyncio.create_task(bound_fetch(sem, url, session))
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)
