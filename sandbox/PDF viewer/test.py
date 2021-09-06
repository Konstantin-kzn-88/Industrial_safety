# # ВАРИАНТ 1 (попроще)
# import sys
# from PySide2 import QtWidgets, QtWebEngineWidgets, QtCore
#
# app = QtWidgets.QApplication(sys.argv)
# web = QtWebEngineWidgets.QWebEngineView()
# web.resize(900,500)
# web.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
# web.load(QtCore.QUrl("file:///C:/python_project/industrial_safety/sandbox/PDF viewer/test_BLOB.pdf"))
# web.show()
#
# sys.exit(app.exec_())

# ВАРИАНТ 2 (поинтереснее)
# отдельно pip install PyQtWebEngine

# import sys
# from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets
#
# PDFJS = 'file:///C:/python_project/industrial_safety/sandbox/PDF viewer/web/viewer.html'
# PDF = 'file:///C:/python_project/industrial_safety/sandbox/PDF viewer/test_BLOB.pdf'
#
# class Window(QtWebEngineWidgets.QWebEngineView):
#    def __init__(self):
#        super(Window, self).__init__()
#        self.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
#
# if __name__ == '__main__':
#
#    app = QtWidgets.QApplication(sys.argv)
#    window = Window()
#    window.setGeometry(600, 50, 800, 600)
#    window.show()
#    sys.exit(app.exec_())


import qpageview

from PySide2 import QtWidgets
a = QtWidgets.QApplication([])

v = qpageview.View()
v.show()
v.loadPdf("C:/python_project/industrial_safety/sandbox/PDF viewer/test_BLOB.pdf")