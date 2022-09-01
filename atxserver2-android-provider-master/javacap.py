from airtest.core.android.android import ADB, Javacap
import asyncio
import websockets
from core.freeport import freeport
from threading import Thread
from core.utils import current_ip


class javaCapWS(object):
    def __init__(self, device_id):
        self.device_id = device_id
        adb = ADB()
        adb.serialno = self.device_id
        self.javacap = Javacap(adb)

    async def serverHands(self, websocket):
        while True:
            if websocket.state != 'State.CLOSING':
                frame = self.javacap.get_frame_from_stream()
                await websocket.send(frame)

    async def serverRun(self, websocket, path):
        await self.serverHands(websocket)


def start_javacap_server(device_id, loop, IP_ADDR, IP_PORT):
    asyncio.set_event_loop(loop)
    javacap_obj = javaCapWS(device_id)
    server = websockets.serve(javacap_obj.serverRun, IP_ADDR, IP_PORT)
    loop.run_until_complete(server)
    loop.run_forever()


def start_javacap_thread(device_id):
    IP_ADDR = current_ip()
    IP_PORT = freeport.get()

    loop = asyncio.new_event_loop()
    javacap_t = Thread(target=start_javacap_server, args=(device_id, loop, IP_ADDR, IP_PORT))
    javacap_t.setDaemon(True)
    javacap_t.start()
    return IP_ADDR + ':' + str(IP_PORT)


if __name__ == '__main__':
    import time

    print("======server main begin======")
    device_id = '275a69ec'
    print(start_javacap_thread(device_id))
    time.sleep(50)
