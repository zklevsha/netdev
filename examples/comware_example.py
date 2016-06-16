import asyncio
import logging

import yaml

import netdev

config_path = 'config.yaml'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


async def task(param):
    hp = netdev.connect(**param)
    await hp.connect()
    out = await hp.send_command('display ver')
    print(out)


async def run():
    config = yaml.load(open(config_path, 'r'))
    devices = yaml.load(open(config['device_credentials'], 'r'))
    params = [p for p in devices if p['device_type'] == 'hp_comware']
    tasks = []
    for param in params:
        tasks.append(task(param))
    await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())