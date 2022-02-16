from pybithumb import WebSocketManager
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

class Worker(QThread):
    def __init__(self):
        super().__init__()

    recv = pyqtSignal(str)
    def run(self):
        # WebSocketManger를 통해서 데이터를 받는 부분 구현
        wm = WebSocketManager("ticker", ["BTC_KRW"])
        while True:
            data = wm.get()
            self.recv.emit(data['content']['closePrice'])

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        label = QLabel("BTC",self)
        label.move(20,20)

        self.price = QTextEdit("",self)
        self.price.move(80,20)
        self.price.resize(100,25)

        button = QPushButton("Start", self)
        button.move(20,50)
        button.clicked.connect(self.click_btn)
        self.th = Worker()
        self.th.recv.connect(self.receive_msg)
    def click_btn(self):
        self.th.start()

    @pyqtSlot(str)
    def receive_msg(self,msg):
        self.price.setText(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()