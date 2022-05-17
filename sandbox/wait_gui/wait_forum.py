import sys
from PySide2 import QtWidgets, QtCore


class Worker(QtCore.QThread):
    delay: int = 0
    ticked: QtCore.SignalInstance = QtCore.Signal(int)

    def __init__(self, parent: QtCore.QObject = None) -> None:
        QtCore.QThread.__init__(self, parent)

    def run(self) -> None:
        for second in range(self.delay):
            self.ticked.emit(second)
            self.sleep(1)


class ProgressBar(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        QtWidgets.QWidget.__init__(self, parent)

        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setMinimumWidth(50)
        self.spinBox.setSuffix(" с")

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setValue(0)

        self.worker = Worker(self)
        self.worker.started.connect(self.workerStarted)
        self.worker.ticked.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.workerFinished)

        self.pushButton = QtWidgets.QPushButton("Start", self)
        self.pushButton.clicked.connect(self.pushButtonClicked)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.pushButton)

    def pushButtonClicked(self) -> None:
        delay: int = self.spinBox.value()
        self.progressBar.setMaximum(delay - 1)
        self.worker.delay = delay
        self.worker.start()

    def workerStarted(self) -> None:
        self.pushButton.setDisabled(True)

    def workerFinished(self) -> None:
        self.pushButton.setEnabled(True)


class Example(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        QtWidgets.QWidget.__init__(self, parent)

        self.progressBar1 = ProgressBar(self)
        self.progressBar2 = ProgressBar(self)
        self.progressBar3 = ProgressBar(self)
        self.progressBar4 = ProgressBar(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.progressBar1)
        layout.addWidget(self.progressBar2)
        layout.addWidget(self.progressBar3)
        layout.addWidget(self.progressBar4)


app = QtWidgets.QApplication(sys.argv)
main = Example()
main.show()
sys.exit(app.exec_())