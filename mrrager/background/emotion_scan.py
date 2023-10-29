import asyncio
import reflex as rx
from ..state import State
import asyncio
import threading
import cv2
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


async def webcam_loop():
    while True:
        try:
            _, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            # cv2.imshow("bruh", frame)

            encoded, buffer = cv2.imencode(".jpg", frame)
            rb = base64.b64encode(buffer)

            await asyncio.sleep(HUME_FPS)
            async with hume_client.connect(hume_config) as socket:
                res = await socket.send_bytes(rb)
                print(res)  # process return value
                return res

        except KeyboardInterrupt:
            break

    camera.release()
    cv2.destroyAllWindows()


class EmotionScan(State):
    emotions: str

    @rx.background
    async def update_emotions(self):
        while True:
            m = await webcam_loop()
            async with self:
                self.emotions = str(m)
            asyncio.sleep(1)
