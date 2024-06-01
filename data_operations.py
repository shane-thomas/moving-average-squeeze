import aiohttp
from aiohttp import ClientResponse
import asyncio
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime, timedelta, date
from tqdm import tqdm
import constants as c
import os
import shutil


async def extracting(response: ClientResponse, counter: int) -> None:
    cwd = os.getcwd()
    data = await response.read()
    zipfile = ZipFile(BytesIO(data))
    filename = zipfile.namelist()[0]
    zipfile.extract(filename, f"{cwd}/{c.TWO_HUNDRED_DAYS_PATH}")
    path = f"{cwd}/{c.TWO_HUNDRED_DAYS_PATH}/{filename}"
    await rename(path)
    if counter < 5:
        zipfile.extract(filename, f"{cwd}/{c.FIVE_DAYS_PATH}")
        path = f"{cwd}/{c.FIVE_DAYS_PATH}/{filename}"
        await rename(path)
    if counter < 10:
        zipfile.extract(filename, f"{cwd}/{c.TEN_DAYS_PATH}")
        path = f"{cwd}/{c.TEN_DAYS_PATH}/{filename}"
        await rename(path)
    if counter < 20:
        zipfile.extract(filename, f"{cwd}/{c.TWENTY_DAYS_PATH}")
        path = f"{cwd}/{c.TWENTY_DAYS_PATH}/{filename}"
        await rename(path)
    if counter < 50:
        zipfile.extract(filename, f"{cwd}/{c.FIFTY_DAYS_PATH}")
        path = f"{cwd}/{c.FIFTY_DAYS_PATH}/{filename}"
        await rename(path)

async def rename(path: str) -> None:
    date_str = path.split('cm')[1][:-8]
    datetime_obj = datetime.strptime(date_str, "%d%b%Y")
    new_path = path.split(
        'cm')[0] + datetime_obj.strftime(c.DATE_FORMAT) + "-NSE-EQ.csv"
    try:
        os.rename(path, new_path)
    except FileExistsError:
        exit


async def get_files() -> None:
    print("Collecting data for the last 200 days")
    tasks = []
    counter = 0
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await (asyncio.gather(*tasks))
        for response in tqdm(responses, desc="Downloading files"):
            if response.status == 200 and counter != 200:
                await extracting(response, counter)
                counter += 1
    os.system('cls')


def get_tasks(session: aiohttp.ClientSession):
    tasks = []
    current_date = date.today()

    for i in range(365):
        if current_date.weekday() < 5:
            url = f"{c.URL}{current_date.strftime(
                '%Y')}/{current_date.strftime('%b').upper()}"
            date_string = current_date.strftime("%d%b%Y").upper()
            filename = f"cm{date_string}bhav.csv.zip"
            url = f"{url}/{filename}"
            tasks.append(session.get(url, ssl=False))
        current_date = current_date - timedelta(days=1)
    return tasks


def reload():
    cwd = os.getcwd()
    data_folder = os.path.join(cwd, "DATA")
    print(data_folder)
    if os.path.isdir(data_folder):
        shutil.rmtree(data_folder)
    print("Downloading new fresh set of files")
    asyncio.run(get_files())


if __name__ == "__main__":
    asyncio.run(get_files())
