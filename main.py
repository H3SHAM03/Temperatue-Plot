from MainWindow import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Temperature Real-time Plot')
    window.setWindowIcon(QtGui.QIcon('icon.png'))
    window.show()
    sys.exit(app.exec_())