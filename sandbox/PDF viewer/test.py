# ВАРИАНТ 1 (попроще) 
import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore

app = QtWidgets.QApplication(sys.argv)
web = QtWebEngineWidgets.QWebEngineView()
web.resize(900,500)
web.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
web.load(QtCore.QUrl("file:///C:/Users/konstantin/Desktop/1.pdf"))
web.show()

sys.exit(app.exec_())

# ВАРИАНТ 2 (поинтереснее)
# отдельно pip install PyQtWebEngine

##import sys
##from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
##
##PDFJS = 'file:///C:/Users/konstantin/Desktop/PDF viewer/web/viewer.html'
##PDF = 'file:///C:/Users/konstantin/Desktop/1.pdf'
##
##class Window(QtWebEngineWidgets.QWebEngineView):
##    def __init__(self):
##        super(Window, self).__init__()
##        self.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
##
##if __name__ == '__main__':
##
##    app = QtWidgets.QApplication(sys.argv)
##    window = Window()
##    window.setGeometry(600, 50, 800, 600)
##    window.show()
##    sys.exit(app.exec_())
