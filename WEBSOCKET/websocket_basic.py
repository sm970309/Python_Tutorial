import websockets
import asyncio
import json
async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri,ping_interval = None) as websocket:
        # 연결 완료 상태 표시
        greeting = await websocket.recv()
        print(greeting)

        subscribe_fmt = {
            "type":"ticker",
            "symbols":["BTC_KRW"],
            "tickTypes":["30M"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)

async def main():
    print('main start')
    await bithumb_ws_client()
    print('main end')
asyncio.run(main())