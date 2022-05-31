import sys
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QTextEdit, QSplitter, QPushButton, \
                            QHBoxLayout, QVBoxLayout


class Client(QWidget):
    def __init__(self):
        super(Client, self).__init__()
        self.resize(500, 450)

        # 1. Создайте элемент управления и завершите макет интерфейса.
        # Код макета находится в функции layout_init().

        self.browser = QTextBrowser(self)
        self.edit = QTextEdit(self)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.browser)
        self.splitter.addWidget(self.edit)
        self.splitter.setSizes([350, 100])

        self.send_btn = QPushButton('Send', self)
        self.close_btn = QPushButton('Close', self)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        # 2. Создайте объект QTcpSocket и вызовите метод connectToHost()
        # для подключения к целевому хосту на указанном порту
        # (в это время будут выполнены три операции рукопожатия).
        # Если клиент и сервер успешно соединены, будет подан сигнал connected()

        self.sock = QTcpSocket(self)
        self.sock.connectToHost(QHostAddress.LocalHost, 9090)

        self.layout_init()
        self.signal_init()

    def layout_init(self):
        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.close_btn)
        self.h_layout.addWidget(self.send_btn)
        self.v_layout.addWidget(self.splitter)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    # 3. Выполните операции по подключению сигналов и слотов в функции signal_init().
    # Когда пользователь закончит ввод текста в поле для редактирования текста QTextEdit,
    # нажмите кнопку 'Send', чтобы отправить текст на сервер.
    # В функции слота write_data_slot() мы сначала получаем текст в поле для редактирования текста,
    # затем кодируем его и отправляем, используя метод write()
    # ( нет необходимости записывать адрес назначения и порт, потому что,
    # он был ранее указан с помощью метода connectToHost() )
    # После отправки мы очищаем поле для редактирования текста.

    def signal_init(self):
        self.send_btn.clicked.connect(self.write_data_slot)

        # 4. Когда пользователь нажимает кнопку закрытия,
        # вызывается метод close_slot(), чтобы закрыть сокет QTcpSocket,
        # и закрываем окно.
        self.close_btn.clicked.connect(self.close_slot)

        # Как упоминалось ранее, когда клиент и сервер успешно подключены,
        # будет подключен сигнал connected.
        # Мы подключаем этот сигнал к функции слота connected_slot().
        self.sock.connected.connect(self.connected_slot)

        # Сигнал readyRead испускается,
        # когда новые данные готовы для чтения.
        self.sock.readyRead.connect(self.read_data_slot)

    def write_data_slot(self):
        message = self.edit.toPlainText()
        self.browser.append('Client: {}'.format(message))
        datagram = message.encode()  # кодируем
        self.sock.write(datagram)    # отправляем
        self.edit.clear()            # очищаем поле для редактирования текста

    # В этой функции слота мы просто добавляем строку 'Connected! Ready to chat! :)' ,
    # чтобы напомнить пользователям, что они могут общаться.
    def connected_slot(self):
        message = 'Connected! Ready to chat! :)'
        self.browser.append(message)

    # Мы используем метод bytesAvailable(), чтобы определить, есть ли данные,
    # и если это так, мы вызываем метод read(), чтобы получить данные размера bytesAvailable().
    # Затем данные декодируются и отображаются на экране.
    def read_data_slot(self):
        while self.sock.bytesAvailable():
            datagram = self.sock.read(self.sock.bytesAvailable())
            message = datagram.decode()
            self.browser.append('Server: {}'.format(message))

    def close_slot(self):
        self.sock.close()                   # закрыть сокет QTcpSocket
        self.close()

    def closeEvent(self, event):
        self.sock.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Client()
    demo.show()
    sys.exit(app.exec_())