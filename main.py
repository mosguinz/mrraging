import asyncio
import threading
import cv2
from operator import itemgetter
from hume import HumeStreamClient
from hume.models.config import FaceConfig

import base64
import dotenv

CONFIG = dotenv.dotenv_values()

# Hume
HUME_API_KEY = CONFIG["HUME_API_KEY"]
HUME_FPS = 1 / 3  # 3 fps
hume_config = [FaceConfig()]
hume_client = HumeStreamClient(HUME_API_KEY)

# CV webcam
camera = cv2.VideoCapture(0)


async def send_to_hume(rb: bytes):
    async with hume_client.connect(hume_config) as socket:
        print("Connected to Hume")
        res = await socket.send_bytes(rb)
        emotions = res['face']['predictions'][0]['emotions']
        sortedEmotions = sorted(emotions, key=itemgetter('score'), reverse=True)
        print("EMOTIONS: ", sortedEmotions[:5])  # process return value
        return res


async def webcam_loop():
    while True:
        try:
            _, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            cv2.imshow("bruh", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            encoded, buffer = cv2.imencode(".jpg", frame)
            rb = base64.b64encode(buffer)
            await send_to_hume(rb)
            # await asyncio.sleep(HUME_FPS)

        except KeyboardInterrupt:
            break

    camera.release()
    cv2.destroyAllWindows()


async def main():
    await webcam_loop()


asyncio.run(main())
