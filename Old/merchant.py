from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QRunnable,QThreadPool
import requests

class Worker(QRunnable):
    def __init__(self, file):
        super().__init__()
        self.filename = file

    def run(self):
        print(self.filename)
        files = {'file': open(self.filename[0], 'rb')}
        print('starting upload')
        response = requests.post('http://34.0.7.203:5000/upload', files=files)
        print('upload finished')
        print(response)



class Ui_MerchantWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1536, 864)
        MainWindow.setMinimumSize(QtCore.QSize(1536, 864))
        MainWindow.setMaximumSize(QtCore.QSize(1536, 864))
        MainWindow.setStyleSheet("background-color :#1c1c1c;\n"
"border-radius:25")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Assets/logo.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1340, 800, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1406, 800, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:#5bc4ff;")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 20, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton#pushButton{\n"
"border-radius:25;\n"
"border: 3px solid #0085ff;\n"
"border-color:#0085ffsu;\n"
"background:transparent;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton#pushButton:hover{\n"
"border-radius:25;\n"
"border: 3px solid #3a9fd9;\n"
"border-color:#0085ffsu;\n"
"background-color:#3A9FD9\n"
"}\n"
"\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/shop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(440, 170, 731, 301))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 40, 681, 231))
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2{\n"
"border-radius:25;\n"
"border: 3px solid #3cfcd9;\n"
"border-color:#0085ffsu;\n"
"background-color:#282828;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton#pushButton_2:hover{\n"
"background-color:#525252;\n"
"}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.openFile())
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(290, 70, 121, 81))
        self.label_4.setStyleSheet("background:transparent;")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("Assets/upload.png"))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(250, 170, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background:transparent;\n"
"color:#c2fff4")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(260, 200, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background:transparent;\n"
"color:#c2fff4")
        self.label_6.setObjectName("label_6")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(550, 220, 501, 91))
        self.frame_2.setStyleSheet("background-color:#292929;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(40, 10, 61, 71))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("Assets/csv.png"))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(150, 26, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:white")
        self.label_8.setObjectName("label_8")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(557, 334, 491, 61))
        
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_3{\n"
"background-color:#58E017;color:#29660c;border-radius:25;\n"
"}\n"
"\n"
"QPushButton#pushButton_3:hover{\n"
"background-color:#84e955\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.StartWork())
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.pushButton.raise_()
        self.frame_2.raise_()
        self.pushButton_3.raise_()
        self.frame.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.threadpool = QThreadPool()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Team"))
        self.label_3.setText(_translate("MainWindow", "Creovate"))
        self.pushButton.setText(_translate("MainWindow", "     Merchant"))
        self.label_5.setText(_translate("MainWindow", "Upload Data File"))
        self.label_6.setText(_translate("MainWindow", "only .csv file supported"))
        self.label_8.setText(_translate("MainWindow", "FILENAMEXYZ.CSV"))
        self.pushButton_3.setText(_translate("MainWindow", "UPLOAD"))
        

    def openFile(self):
        # self.filename = QFileDialog.getOpenFileName(filter="Text files (*.txt);;JSON files (*.json);;CSV Files (*.csv)")
        self.filename = QFileDialog.getOpenFileName(filter="CSV Files (*.csv)")

        if self.filename[0] != '' and self.filename[1] != '':
            self.frame.hide()
            self.label_8.setText('{}'.format(self.filename[0].split('/')[-1]))


    def StartWork(self):
        worker = Worker(self.filename)
        self.threadpool.start(worker)

#     def SendFile(self):
#         print(self.filename)
#         files = {'file': open(self.filename[0], 'rb')}
#         response = requests.post('http://34.0.7.203:5000/upload', files=files)
#         print(response)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MerchantWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
