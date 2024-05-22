from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QRunnable,QThreadPool,QProcess,QObject, pyqtSignal
import requests
import json
from src.map import MapWindow

class Worker(QRunnable):
    def __init__(self, file):
        super().__init__()
        self.filename = file

    def run(self):
        config = json.load(open("src/config.json",'r'))
        print(self.filename)
        files = {'file': open(self.filename[0], 'rb')}
        print('starting upload')
        response = requests.post(config['SellerCSV'], files=files)
        print('upload finished')
        print(response)



class Communicator(QObject):
    coordinates_signal = pyqtSignal(int) 

class Ui_MerchantWindow(object):
    
    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1536, 864)
        MainWindow.setMinimumSize(QtCore.QSize(1536, 864))
        MainWindow.setMaximumSize(QtCore.QSize(1536, 864))
        MainWindow.setStyleSheet("background-color :#e8e8e8;\n"
"border-radius:25")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Assets/logo2.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1340, 800, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:#3f3f3f;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1406, 800, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:#4285F4;")
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
"color:#3f3f3f;\n"
"}\n"
"\n"
"QPushButton#pushButton:hover{\n"
"border-radius:25;\n"
"border: 3px solid #3a9fd9;\n"
"border-color:#0085ffsu;\n"
"background-color:#558be5\n"
"}\n"
"\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/shop2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(400, 100, 731, 301))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 40, 681, 231))
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2{\n"
"border-radius:25;\n"
"border: 3px solid #4285f4;\n"
"border-color:#0085ffsu;\n"
"background-color:#e8e8e8;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton#pushButton_2:hover{\n"
"background-color:#e1e1e1;\n"
"}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(290, 70, 121, 81))
        self.label_4.setStyleSheet("background:transparent;")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("Assets/upload2.png"))
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
"color:#3f3f3f")
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
"color:#858585")
        self.label_6.setObjectName("label_6")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(510, 150, 501, 91))
        self.frame_2.setStyleSheet("background-color:#e2e2e2")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(60, 15, 61, 61))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setPixmap(QtGui.QPixmap("Assets/csv-256.png"))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(150, 26, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:#3f3f3f;")
        self.label_8.setObjectName("label_8")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 260, 501, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_3{\n"
"border-radius:15;\n"
"border-color:#5bc4ff;\n"
"background-color:#4285F4;\n"
"color:#1c1c1c;\n"
"}\n"
"\n"
"QPushButton#pushButton_3:hover {\n"
"border-radius:15;\n"
"border-color:#5bc4ff;\n"
"background-color:#75A9FF;\n"
"color:#1c1c1c;\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setEnabled(True)
        self.frame_3.setGeometry(QtCore.QRect(330, 410, 821, 431))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(100, 20, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background:transparent;\n"
"color:#626262")
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit.setGeometry(QtCore.QRect(90, 70, 661, 31))
        self.lineEdit.setStyleSheet("border-radius:25;\n"
"border-color:#0085ffsu;\n"
"background-color:#e8e8e8;\n"
"color:black;")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_4.setGeometry(QtCore.QRect(80, 60, 681, 51))
        self.pushButton_4.setStyleSheet("QPushButton#pushButton_4{\n"
"border-radius:15;\n"
"border: 3px solid #4285f4;\n"
"border-color:#4285f4;\n"
"background-color:#e8e8e8;\n"
"color:white;\n"
"}\n"
"\n"
"")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(410, -10, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background:transparent;\n"
"color:#6c6c6c")
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(100, 120, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background:transparent;\n"
"color:#626262")
        self.label_13.setObjectName("label_13")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 170, 601, 31))
        self.lineEdit_3.setStyleSheet("border-radius:25;\n"
"border-color:#0085ffsu;\n"
"background-color:#e8e8e8;\n"
"color:black;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_6.setGeometry(QtCore.QRect(80, 160, 621, 51))
        self.pushButton_6.setStyleSheet("QPushButton#pushButton_6{\n"
"border-radius:15;\n"
"border: 3px solid #3cfcd9;\n"
"border-color:#4285f4;\n"
"background-color:#e8e8e8;\n"
"color:white;\n"
"}\n"
"\n"
"")
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(620, 120, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background:transparent;\n"
"color:#E41515;")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(100, 200, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background:transparent;\n"
"color:#626262")
        self.label_15.setObjectName("label_15")
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_9.setGeometry(QtCore.QRect(80, 270, 681, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet("QPushButton#pushButton_9{\n"
"border-radius:15;\n"
"border-color:#5bc4ff;\n"
"background-color:#4285F4;\n"
"color:#1c1c1c;\n"
"}\n"
"\n"
"QPushButton#pushButton_9:hover {\n"
"border-radius:15;\n"
"border-color:#5bc4ff;\n"
"background-color:#75A9FF;\n"
"color:#1c1c1c;\n"
"}")
        self.pushButton_9.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_5.setGeometry(QtCore.QRect(710, 160, 51, 51))
        self.pushButton_5.setStyleSheet("QPushButton#pushButton_5{\n"
"border-radius:15;\n"
"border: 3px solid #3cfcd9;\n"
"border-color:#4285f4;\n"
"background-color:#e8e8e8;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton#pushButton_5:hover{\n"
"border-radius:15;\n"
"border: 3px solid #3cfcd9;\n"
"border-color:#4285f4;\n"
"background-color:#bcbcbc;\n"
"color:white;\n"
"}\n"
"")
        self.pushButton_5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Assets/marker.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_9.raise_()
        self.pushButton_4.raise_()
        self.label_10.raise_()
        self.label_13.raise_()
        self.pushButton_6.raise_()
        self.lineEdit.raise_()
        self.lineEdit_3.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.pushButton_9.raise_()
        self.pushButton_5.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.pushButton.raise_()
        self.frame_2.raise_()
        self.pushButton_3.raise_()
        self.frame.raise_()
        self.frame_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.threadpool = QThreadPool()
        self.process = QProcess()

        self.communicator = Communicator()
        self.communicator.coordinates_signal.connect(self.update_coordinates)

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
         self.label_9.setText(_translate("MainWindow", "Enter Merchant Name"))
         self.label_10.setText(_translate("MainWindow", "OR"))
         self.label_13.setText(_translate("MainWindow", "Enter Pincode Area"))
         self.label_14.setText(_translate("MainWindow", "")) #invalid
         self.label_15.setText(_translate("MainWindow", "Enter multiple pincodes separated by commas e.g., 110001,500001,201301"))
         self.pushButton_9.setText(_translate("MainWindow", "SUBMIT"))
         self.pushButton_9.clicked.connect(lambda: self.sendJSON(self.lineEdit.text(),self.lineEdit_3.text()))
         self.pushButton_2.clicked.connect(lambda: self.openFile())
         self.pushButton_5.clicked.connect(lambda: self.open_map_view())


   

        

    def openFile(self):
        # self.filename = QFileDialog.getOpenFileName(filter="CSV Files (*.csv)")
        self.filename = QFileDialog.getOpenFileName(filter="CSV Files (*.csv)")

        if self.filename[0] != '' and self.filename[1] != '':
            self.frame.hide()
            self.frame_3.hide()
            self.label_8.setText('{}'.format(self.filename[0].split('/')[-1]))


    def StartWork(self):
        worker = Worker(self.filename)
        self.threadpool.start(worker)

    def sendJSON(self,merch,pinc):
        config = json.load(open("src/config.json",'r'))
        url = config['SellerJSON']
        payload = {
        "merchant_name": merch,
        "pincodes": pinc
        }

        headers = {
        'Content-Type': 'application/json'
        }

        try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                        print("Request was successful.")
                        print("Response:", response.json())
                else:
                        print(f"Failed to send request. Status code: {response.status_code}")
                        print("Response:", response.text)
        except Exception as e:
                print(f"An error occurred: {e}")


    def update_coordinates(self,x):
       print('started',x)
       if len(str(x)) == 6:
           oldtxt = self.lineEdit_3.text()
           if len(oldtxt) == 0:
                self.lineEdit_3.setText(str(x)+',')
           elif oldtxt[-1]==',':
               self.lineEdit_3.setText(oldtxt+str(x)+',')
                
       
       else:
           print("Pincode not found")

    def open_map_view(self):
        self.map_window = MapWindow()
        self.map_window.bridge.coordinates_received.connect(self.communicator.coordinates_signal.emit)
        self.map_window.show()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MerchantWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
