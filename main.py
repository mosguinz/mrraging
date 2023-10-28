import asyncio

from hume import HumeStreamClient
from hume.models.config import BurstConfig
from hume.models.config import ProsodyConfig


async def main():
    client = HumeStreamClient("<your-api-key>")
    configs = [BurstConfig(), ProsodyConfig()]
    async with client.connect(configs) as socket:
        result = await socket.send_file("<your-audio-filepath>")
        print(result)


asyncio.run(main())