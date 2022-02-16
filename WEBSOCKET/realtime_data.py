import multiprocessing as mp
import websockets
import asyncio
import json
import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# 비동기 방식으로 웹소켓을 받아옴
async def bithumb_ws_client(q):
    uri = "wss://pubwss.bithumb.com/pub/ws"

    # bithumb의 websocket에 연결
    async with websockets.connect(uri,ping_interval=None) as websocket:
        subscribe_fmt = {
            "type":"ticker",
            "symbols":["BTC_KRW"],
            "tickTypes":["1H"]
        }
        # 지정한 형식을 json형태로 변환 후 bithumb에 전달
        subscribe_data = json.dumps(subscribe_fmt)
        # await를 사용하여 비동기함수 처리
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            # websocket 데이터 받아온 후 q(queue)에 집어넣음
            q.put(data)

# producer의 메인 Thread
async def main(q):
    await bithumb_ws_client(q)

def producer(q):
    asyncio.run(main(q))

# 데이터를 가져오는 Thread
class Consumer(QThread):
    poped = pyqtSignal(dict)

    def __init__(self,q):
        super().__init__()
        self.q = q
    def run(self):
        while True:
            # queue에 데이터가 들어올 때 마다 signal을 보냄
            if not self.q.empty():
                data=q.get()
                self.poped.emit(data)

class MyWindow(QMainWindow):
    def __init__(self,q):
        super().__init__()
        self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('Bithumb')

        # 전달받은 queue로 signal객체(thread) 생성
        self.consumer = Consumer(q)
        # signal을 slot에 연결
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        # widget
        self.label = QLabel("bitcoin: ",self)
        self.label.move(10,10)

        self.line_edit = QLineEdit(" ",self)
        self.line_edit.resize(150,30)
        self.line_edit.move(100,10)

        

    # signal을 받으면 해당 slot을 실행
    @pyqtSlot(dict)
    def print_data(self,data):
        content = data.get('content')
        if content is not None:
            current_price = int(content.get('closePrice'))
            # 아래의 format은 1,000 단위마다 , 를 찍는 method
            self.line_edit.setText(format(current_price,",d"))

        now = datetime.datetime.now().strftime("%Y-%m-%d-%p %I:%m:%S")
        self.statusBar().showMessage(str(now))

# 메인 프로세스(MyWindow) -> 서브 프로세스(Producer)
# 프로세스간에 queue를 사용하여 데이터를 주고받음
if __name__ == "__main__":
    # producer 프로세스를 spawn함
    q = mp.Queue()
    # args -> 전달할 인자(튜플 형태로 전달), daemon = True -> 부모프로세스가 종료될때 daemon도 같이 종료
    p = mp.Process(name="Producer",target=producer,args=(q,),daemon=True)
    p.start()

    app = QApplication(sys.argv)
    # 위에서 생성된 queue를 메인 프로세스에 넘겨줌
    mywindow = MyWindow(q)
    mywindow.show()
    app.exec_()