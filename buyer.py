from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from flask import Flask, jsonify, request
import json
import threading


class Ui_BuyerWindow(object):

    

    def setupUi(self, MainWindow):
        self.activated = 'pincode'
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1536, 864)
        MainWindow.setMinimumSize(QtCore.QSize(1536, 864))
        MainWindow.setMaximumSize(QtCore.QSize(1536, 864))
        MainWindow.setStyleSheet("background-color :#1c1c1c;")
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
                "border-radius:20;\n"
                "border: 3px solid #3a9fd9;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#3A9FD9\n"
                "}\n"
                "\n"
                "\n"
                "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/buyer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 129, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2{\n"
                "border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;\n"
                "}\n"
                "\n"
                "QPushButton#pushButton_2:hover{\n"
                "border-radius:20;\n"
                "border: 3px solid #3a9fd9;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#3A9FD9\n"
                "}\n"
                "\n"
                "\n"
                "")
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(214, 130, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_3{\n"
                "border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;\n"
                "}\n"
                "\n"
                "QPushButton#pushButton_3:hover{\n"
                "border-radius:20;\n"
                "border: 3px solid #3a9fd9;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#3A9FD9\n"
                "}\n"
                "\n"
                "\n"
                "")
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 130, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton#pushButton_4{\n"
                "border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;\n"
                "}\n"
                "\n"
                "QPushButton#pushButton_4:hover{\n"
                "border-radius:20;\n"
                "border: 3px solid #3a9fd9;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#3A9FD9\n"
                "}\n"
                "\n"
                "\n"
                "")
        self.pushButton_4.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(980, 140, 451, 611))
        self.scrollArea.setStyleSheet("background-color:#292929;\n"
"border-radius:25")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 451, 611))
        self.scrollAreaWidgetContents.setBaseSize(QtCore.QSize(300, 300))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(30, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 670, 561, 71))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton#pushButton_5{\n"
                "border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#0085ff;\n"
                "color:white;\n"
                "}\n"
                "\n"
                "QPushButton#pushButton_5:hover{\n"
                "border-radius:20;\n"
                "border: 3px solid #3a9fd9;\n"
                "border-color:#0085ffsu;\n"
                "background-color:#3A9FD9\n"
                "}\n"
                "\n"
                "\n"
                "")
        self.pushButton_5.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        # self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        # self.spinBox.setGeometry(QtCore.QRect(270, 628, 44, 26))
        # self.spinBox.setStyleSheet("color:white")
        # self.spinBox.setObjectName("spinBox")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(80, 630, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        # self.radioButton.setFont(font)
        # self.radioButton.setStyleSheet("color:white;")
        # self.radioButton.setObjectName("radioButton")
        # self.label_5 = QtWidgets.QLabel(self.centralwidget)
        # self.label_5.setGeometry(QtCore.QRect(318, 632, 66, 17))
        # font = QtGui.QFont()
        # font.setFamily("Google Sans")
        # self.label_5.setFont(font)
        # self.label_5.setStyleSheet("color:White;")
        # self.label_5.setObjectName("label_5")
        self.pincodes = QtWidgets.QFrame(self.centralwidget)
        self.pincodes.setGeometry(QtCore.QRect(40, 180, 821, 411))
        self.pincodes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pincodes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pincodes.setObjectName("pincodes")
        self.pincodes.setStyleSheet("background:transparent;")
        self.textEdit = QtWidgets.QTextEdit(self.pincodes)
        self.textEdit.setGeometry(QtCore.QRect(40, 90, 651, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;")
        self.textEdit.setObjectName("textEdit")
        self.label_6 = QtWidgets.QLabel(self.pincodes)
        self.label_6.setGeometry(QtCore.QRect(40, 50, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white")
        self.label_6.setObjectName("label_6")
        self.gps = QtWidgets.QFrame(self.centralwidget)
        self.gps.setGeometry(QtCore.QRect(60, 190, 821, 411))
        self.gps.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gps.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gps.setObjectName("gps")
        self.gps.setStyleSheet("background:transparent;")
        self.textEdit_2 = QtWidgets.QTextEdit(self.gps)
        self.textEdit_2.setGeometry(QtCore.QRect(40, 90, 651, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setStyleSheet("border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_7 = QtWidgets.QLabel(self.gps)
        self.label_7.setGeometry(QtCore.QRect(40, 50, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:white")
        self.label_7.setObjectName("label_7")
        self.textEdit_3 = QtWidgets.QTextEdit(self.gps)
        self.textEdit_3.setGeometry(QtCore.QRect(50, 210, 651, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setStyleSheet("border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_8 = QtWidgets.QLabel(self.gps)
        self.label_8.setGeometry(QtCore.QRect(50, 170, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:white")
        self.label_8.setObjectName("label_8")
        self.location = QtWidgets.QFrame(self.centralwidget)
        self.location.setGeometry(QtCore.QRect(40, 200, 821, 411))
        self.location.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.location.setFrameShadow(QtWidgets.QFrame.Raised)
        self.location.setObjectName("location")
        self.location.setStyleSheet("background:transparent;")
        self.textEdit_4 = QtWidgets.QTextEdit(self.location)
        self.textEdit_4.setGeometry(QtCore.QRect(40, 90, 651, 51))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_4.setFont(font)
        self.textEdit_4.setStyleSheet("border-radius:25;\n"
                "border: 3px solid #0085ff;\n"
                "border-color:#0085ffsu;\n"
                "background:transparent;\n"
                "color:white;")
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_9 = QtWidgets.QLabel(self.location)
        self.label_9.setGeometry(QtCore.QRect(40, 50, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Google Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:white")
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Team Creovate"))
        self.label_2.setText(_translate("MainWindow", "Team"))
        self.label_3.setText(_translate("MainWindow", "Creovate"))
        self.pushButton.setText(_translate("MainWindow", "    Buyer"))
        self.pushButton_2.setText(_translate("MainWindow", "Pincodes"))
        self.pushButton_2.clicked.connect(lambda :self.changeMode(self.pincodes,self.gps,self.location,'pincode'))
        self.pushButton_3.setText(_translate("MainWindow", "GPS"))
        self.pushButton_3.clicked.connect(lambda :self.changeMode(self.gps,self.pincodes,self.location,'gps'))
        self.pushButton_4.setText(_translate("MainWindow", "Location"))
        self.pushButton_4.clicked.connect(lambda: self.changeMode(self.location,self.gps,self.pincodes,'location'))
        self.pushButton_5.setText(_translate("MainWindow", "SEARCH"))
        self.pushButton_5.clicked.connect(lambda: self.SendReq(self.activated))
        # self.radioButton.setText(_translate("MainWindow", "Find all merchants within"))
        # self.label_5.setText(_translate("MainWindow", "kms."))
        self.label_6.setText(_translate("MainWindow", "Enter Pincode(s)"))
        self.label_7.setText(_translate("MainWindow", "Enter Latitude"))
        self.label_8.setText(_translate("MainWindow", "Enter Longitude"))
        self.label_9.setText(_translate("MainWindow", "Enter Location Name"))
        self.location.hide()
        self.gps.hide()

    def addUi(self,x):
        for i in reversed(range(self.verticalLayout_2.count())):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)
                
        for i in range(len(x)):
                self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
                self.frame.setMinimumSize(QtCore.QSize(360, 55))
                self.frame.setMaximumSize(QtCore.QSize(360, 55))
                self.frame.setStyleSheet("background-color:#262626")
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame_"+str(i))
                self.label_4 = QtWidgets.QLabel(self.frame)
                self.label_4.setGeometry(QtCore.QRect(40, 0, 271, 51))
                font = QtGui.QFont()
                font.setFamily("Google Sans")
                font.setBold(True)
                font.setWeight(75)
                self.label_4.setFont(font)
                self.label_4.setStyleSheet("color:white")
                self.label_4.setObjectName("label_4_"+str(i)) 
                self.label_4.setText(x[i])
                self.verticalLayout_2.addWidget(self.frame)

 
    def UpdateMerchants(self,data):
        for i in range(len(data)):
            self.addUi(data[i])



    def changeMode(self,active,nactive,nactive2,activated):
        self.activated = activated
        active.show()
        nactive.hide()
        nactive2.hide()

    def SendReq(self,mode):
        if mode=='pincode':
            rawTxt = self.textEdit.toPlainText()
            if ',' in rawTxt:
                pinList = [int(i) for i in rawTxt.split(",")] 
            else:
                pinList = [int(rawTxt)]
        elif mode=='gps':
            pinList = [float(self.textEdit_2.toPlainText()),float(self.textEdit_3.toPlainText())]
        elif mode=='location':
            pinList = [self.textEdit_4.toPlainText()]
        q = requests.post('http://34.0.5.92:4444/pincode',json={mode:pinList})
        doc = q.json()['Merchants']
        print(doc)
        if len(doc) == 0:
            self.addUi(['No Data Found'])
        else:
            self.addUi(doc)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_BuyerWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # threading.Thread(
    #     target=Fapp.run,
    #     kwargs=dict(debug=False,host='0.0.0.0',use_reloader=False,port=5555),
    #     daemon=True,
    # ).start()
    sys.exit(app.exec_())

