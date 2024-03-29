from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from logic.data import Data
from logic.control import Control
import time
import json
from glob import glob

class Ui_Form(object):
    def __init__(self, Form):
        self.form = Form
        self.form.setObjectName("form")
        self.form.resize(800, 380)
        self.form.setStyleSheet("background-color: rgb(236, 236, 236);\n")
        self.state = 0 #0: home_screen, 1: create, 2: calibrate, 3: select
        self.user_screen = 1
        self.dat = Data()
        self.dat.clean_queue()
        self.ctr = Control()
        self.trash = True
        self.init= [0,0,0,0,0] #All screen aren't called
        self.state_machine(4)
    
    #region stylesheets
    def slider_formatters(self):
        return """
        QSlider::groove:horizontal {
        border: 1px solid #bbb;
        background: white;
        height: 20px;
        border-radius: 4px;
        }

        QSlider::sub-page:horizontal {
        background: #E09825;
        border: 1px solid #777;
        height: 20px;
        border-radius: 4px;
        }

        QSlider::add-page:horizontal {
        background: #fff;
        border: 1px solid #777;
        height: 20px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fff, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 4px;
        }

        QSlider::sub-page:horizontal:disabled {
        background: #bbb;
        border-color: #999;
        }

        QSlider::add-page:horizontal:disabled {
        background: #eee;
        border-color: #999;
        }

        QSlider::handle:horizontal:disabled {
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        }"""
    
    def buttonStyle(self, selected):
        if selected:
            return """
            QPushButton {
                color: #aa0000;
                font-weight: bold;
                border: 1px solid rgb(236, 236, 236);
                border-radius: 3px;
                width: 30px;
                height: 30px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(236, 236, 236), stop: 1 rgb(236, 236, 236));
            }
            QPushButton:hover {
                color: #fff;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(179, 176, 176), stop: 1 rgb(179, 176, 176));
            }
            QPushButton:pressed {
                color: #fff;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E09825, stop: 1 #E09825);
            }
            """
        else:
            return """
            QPushButton {
                color: black;
                border: 1px solid rgb(236, 236, 236);
                border-radius: 3px;
                width: 30px;
                height: 30px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(236, 236, 236), stop: 1 rgb(236, 236, 236));
            }
            QPushButton:hover {
                color: #fff;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(179, 176, 176), stop: 1 rgb(179, 176, 176));
            }
            QPushButton:pressed {
                color: #fff;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E09825, stop: 1 #E09825);
            }
            """
    
    def buttonNavStyle(self):
        return """
        QPushButton{
            height: 50px;
            background-color: #241a16;
            color: #fff;
        }
        QPushButton:hover {
            color: #fff;
            background-color: #0c0807;
        }
        QPushButton:pressed {
            color: #fff;
            background-color: #333;
        }"""
    
    def ButtonImageStyle(self):
        return """
        QPushButton{
            background-color: rgb(236, 236, 236);
        }
        QPushButton:hover {
            background-color: rgb(236, 236, 236);
        }
        QPushButton:pressed {
            background-color: rgb(236, 236, 236);
        }
        QPushButton:released {
            background-color: rgb(236, 236, 236);
        }
        """

    #endregion stylesheets
    
    #region home_screen
    def main(self): 
        self.pushButton = QtWidgets.QPushButton(self.form)
        self.pushButton.setGeometry(QtCore.QRect(100, 180, 150, 60))
        self.pushButton.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 25px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "border-image: url(assets/img2.png)")
        self.pushButton.setText("Crear")
        self.pushButton.clicked.connect(lambda: self.state_machine(1))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.form)
        self.pushButton_4.setGeometry(QtCore.QRect(720, 20, 41, 31))
        self.pushButton_4.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 10px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.form)
        self.pushButton_5.setGeometry(QtCore.QRect(300, 180, 150, 60))
        self.pushButton_5.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 25px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "border-image: url(assets/img1.png)")
        self.pushButton_5.setText("Calibrar")
        self.pushButton_5.clicked.connect(lambda: self.state_machine(2))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.form)
        self.pushButton_6.setGeometry(QtCore.QRect(500, 180, 150, 60))
        self.pushButton_6.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 25px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "border-image: url(assets/img0.png)")
        self.pushButton_6.setText("Seleccionar")
        self.pushButton_6.clicked.connect(lambda: self.state_machine(3))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label = QtWidgets.QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 74))
        self.label.setStyleSheet("font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: bold;\n"
        "font-size: 36px;\n"
        "line-height: 42px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "background-color: #E09825;")
        self.label.setObjectName("label")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.form)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 310, 65, 65))
        self.pushButton_3.setStyleSheet("border-image: url(:/back/assets/back.png);\n"
        "border-radius:30px\n"
        "")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setIcon(QIcon('assets/back.png'))
        self.pushButton_3.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_3.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.pushButton_3.clicked.connect(lambda: self.state_machine(4))
        
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle(_translate("self.form", "Mixology"))
        self.pushButton_4.setText(_translate("self.form", "X"))
        self.pushButton_4.clicked.connect(lambda: self.form.close())
        self.label.setText(_translate("self.form", "    MIXOLOGY"))

    #endregion home_screen

    #region create
    def create_form(self):
        self.form.setObjectName("crt_Form")
        self.form.resize(800, 380)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form.sizePolicy().hasHeightForWidth())
        self.form.setSizePolicy(sizePolicy)
        self.form.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.crt_label_2 = QtWidgets.QLabel(self.form)
        self.crt_label_2.setGeometry(QtCore.QRect(0, 0, 800, 74))
        self.crt_label_2.setStyleSheet("font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: bold;\n"
        "font-size: 36px;\n"
        "line-height: 42px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "background-color: #E09825;")
        self.crt_label_2.setObjectName("crt_label_2")
        self.crt_pushButton_7 = QtWidgets.QPushButton(self.form)
        self.crt_pushButton_7.setGeometry(QtCore.QRect(720, 20, 41, 31))
        self.crt_pushButton_7.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 10px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;")
        self.crt_pushButton_7.setObjectName("crt_pushButton_7")
        self.crt_pushButton_7.clicked.connect(lambda: sys.exit(0))
        self.crt_label_12 = QtWidgets.QLabel(self.form)
        self.crt_label_12.setGeometry(QtCore.QRect(320, 330, 67, 17))
        self.crt_label_12.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.crt_label_12.setObjectName("crt_label_12")
        
        self.crt_label_13 = QtWidgets.QLabel(self.form)
        self.crt_label_13.setGeometry(QtCore.QRect(290, 33, 67, 18))
        self.crt_label_13.setStyleSheet("color: #fff;background-color: #E09825;font-size: 16px;")
        self.crt_label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.crt_label_13.setObjectName("crt_label_13")
        
        self.crt_pushButton = QtWidgets.QPushButton(self.form)
        self.crt_pushButton.setGeometry(QtCore.QRect(10, 310, 65, 65))
        self.crt_pushButton.setStyleSheet("border-image: url(:/back/assets/back.png);\n"
        "border-radius:30px\n"
        "")
        self.crt_pushButton.setText("")
        self.crt_pushButton.setObjectName("crt_pushButton")
        self.crt_pushButton.setIcon(QIcon('assets/back.png'))
        self.crt_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.crt_pushButton.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.crt_pushButton.clicked.connect(lambda: self.state_machine(0))
        self.crt_pushButton_2 = QtWidgets.QPushButton(self.form)
        self.crt_pushButton_2.setGeometry(QtCore.QRect(720, 310, 65, 65))
        self.crt_pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "border-image: url(:/check/assets/check2.png);\n"
        "border-radius:30px\n"
        "")
        self.crt_pushButton_2.setText("")
        self.crt_pushButton_2.setObjectName("crt_pushButton_2")
        self.crt_pushButton_2.setIcon(QIcon('assets/check2.png'))
        self.crt_pushButton_2.setIconSize(QtCore.QSize(50, 50))
        self.crt_pushButton_2.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.crt_pushButton_2.clicked.connect(self.crt_save)
        self.crt_lineEdit = QtWidgets.QLineEdit(self.form)
        self.crt_lineEdit.setGeometry(QtCore.QRect(360, 30, 170, 25))
        self.crt_lineEdit.setStyleSheet("border-radius: 10px;\n"
        "")
        self.crt_lineEdit.setObjectName("crt_lineEdit")
        self.crt_textEdit = QtWidgets.QTextEdit(self.form)
        self.crt_textEdit.setGeometry(QtCore.QRect(300, 30, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.crt_textEdit.setFont(font)
        self.crt_textEdit.setStyleSheet("background-color: #E09825;\n"
        "color: #FFFFFF;")
        self.crt_textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.crt_textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.crt_textEdit.setLineWidth(1)
        self.crt_textEdit.setObjectName("crt_textEdit")
        self.crt_horizontalSlider_11 = QtWidgets.QSlider(self.form)
        self.crt_horizontalSlider_11.setGeometry(QtCore.QRect(400, 330, 80, 16))
        self.crt_horizontalSlider_11.setMaximum(1)
        self.crt_horizontalSlider_11.setSliderPosition(0)
        self.crt_horizontalSlider_11.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_11.setObjectName("crt_horizontalSlider_11")
        self.crt_scrollArea = QtWidgets.QScrollArea(self.form)
        self.crt_scrollArea.setGeometry(QtCore.QRect(30, 110, 350, 200))
        self.crt_scrollArea.setWidgetResizable(True)
        self.crt_scrollArea.setObjectName("crt_scrollArea")
        self.crt_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.crt_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 334, 442))
        self.crt_scrollAreaWidgetContents.setObjectName("crt_scrollAreaWidgetContents")
        self.crt_formLayout = QtWidgets.QFormLayout(self.crt_scrollAreaWidgetContents)
        self.crt_formLayout.setObjectName("crt_formLayout")
        self.crt_label = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label.setFont(font)
        self.crt_label.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label.setObjectName("crt_label")
        self.crt_formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.crt_label)
        self.crt_horizontalSlider = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)

        self.crt_horizontalSlider.setFont(font)
        self.crt_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider.setObjectName("crt_horizontalSlider")
        
        self.crt_formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider)
        self.crt_label_3 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_3.setFont(font)
        self.crt_label_3.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_3.setObjectName("crt_label_3")
        self.crt_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.crt_label_3)
        self.crt_horizontalSlider_2 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_2.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_2.setObjectName("crt_horizontalSlider_2")
        self.crt_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_2)
        self.crt_label_4 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_4.setFont(font)
        self.crt_label_4.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_4.setObjectName("crt_label_4")
        self.crt_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.crt_label_4)
        self.crt_horizontalSlider_3 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_3.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_3.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_3.setObjectName("crt_horizontalSlider_3")
        self.crt_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_3)
        self.crt_label_6 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_6.setFont(font)
        self.crt_label_6.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_6.setObjectName("crt_label_6")
        self.crt_formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.crt_label_6)
        self.crt_horizontalSlider_4 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_4.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_4.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_4.setObjectName("crt_horizontalSlider_4")
        self.crt_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_4)
        self.crt_label_7 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_7.setFont(font)
        self.crt_label_7.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_7.setObjectName("crt_label_7")
        self.crt_formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.crt_label_7)
        self.crt_horizontalSlider_5 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_5.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_5.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_5.setObjectName("crt_horizontalSlider_5")
        self.crt_formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_5)
        self.crt_label_8 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_8.setFont(font)
        self.crt_label_8.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_8.setObjectName("crt_label_8")
        self.crt_formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.crt_label_8)
        self.crt_horizontalSlider_6 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_6.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_6.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_6.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_6.setObjectName("crt_horizontalSlider_6")
        self.crt_formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_6)
        self.crt_label_9 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_9.setFont(font)
        self.crt_label_9.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_9.setObjectName("crt_label_9")
        self.crt_formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.crt_label_9)
        self.crt_horizontalSlider_7 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_7.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_7.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_7.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_7.setObjectName("crt_horizontalSlider_7")
        self.crt_formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_7)
        self.crt_label_11 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_11.setFont(font)
        self.crt_label_11.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_11.setObjectName("crt_label_11")
        
        
        self.crt_formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.crt_label_11)
        self.crt_horizontalSlider_8 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_8.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_8.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_8.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_8.setObjectName("crt_horizontalSlider_8")
        self.crt_formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_8)
        self.crt_label_10 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_10.setFont(font)
        self.crt_label_10.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_10.setObjectName("crt_label_10")
        self.crt_formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.crt_label_10)
        self.crt_label_5 = QtWidgets.QLabel(self.crt_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crt_label_5.setFont(font)
        self.crt_label_5.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.crt_label_5.setObjectName("crt_label_5")
        self.crt_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.crt_label_5)
        self.crt_horizontalSlider_9 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_9.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_9.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_9.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_9.setObjectName("crt_horizontalSlider_9")
        self.crt_formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_9)
        self.crt_horizontalSlider_10 = QtWidgets.QSlider(self.crt_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crt_horizontalSlider_10.sizePolicy().hasHeightForWidth())
        self.crt_horizontalSlider_10.setSizePolicy(sizePolicy)
        self.crt_horizontalSlider_10.setOrientation(QtCore.Qt.Horizontal)
        self.crt_horizontalSlider_10.setObjectName("crt_horizontalSlider_10")
        self.crt_horizontalSlider_10.setValue(0)
        self.crt_formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_10)

        #region Slider formatter

        self.crt_horizontalSlider.setMaximum(500)
        self.crt_horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider.setTickInterval(50)
        self.crt_horizontalSlider.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_2.setMaximum(500)
        self.crt_horizontalSlider_2.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_2.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_2.setTickInterval(50)
        self.crt_horizontalSlider_2.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_3.setMaximum(500)
        self.crt_horizontalSlider_3.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_3.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_3.setTickInterval(50)
        self.crt_horizontalSlider_3.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_4.setMaximum(500)
        self.crt_horizontalSlider_4.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_4.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_4.setTickInterval(50)
        self.crt_horizontalSlider_4.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_5.setMaximum(500)
        self.crt_horizontalSlider_5.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_5.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_5.setTickInterval(50)
        self.crt_horizontalSlider_5.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_6.setMaximum(500)
        self.crt_horizontalSlider_6.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_6.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_6.setTickInterval(50)
        self.crt_horizontalSlider_6.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_7.setMaximum(500)
        self.crt_horizontalSlider_7.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_7.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_7.setTickInterval(50)
        self.crt_horizontalSlider_7.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_8.setMaximum(500)
        self.crt_horizontalSlider_8.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_8.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_8.setTickInterval(50)
        self.crt_horizontalSlider_8.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_9.setMaximum(500)
        self.crt_horizontalSlider_9.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_9.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_9.setTickInterval(50)
        self.crt_horizontalSlider_9.setStyleSheet(self.slider_formatters())


        self.crt_horizontalSlider_10.setMaximum(500)
        self.crt_horizontalSlider_10.setTickPosition(QSlider.TicksBelow)
        self.crt_horizontalSlider_10.valueChanged.connect(self.crt_update_val)
        self.crt_horizontalSlider_10.setTickInterval(50)
        self.crt_horizontalSlider_10.setStyleSheet(self.slider_formatters())
        #endregion Slider formatter

        self.crt_formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.crt_horizontalSlider_9)
        self.crt_scrollArea.setWidget(self.crt_scrollAreaWidgetContents)
        self.crt_scrollArea_2 = QtWidgets.QScrollArea(self.form)
        self.crt_scrollArea_2.setGeometry(QtCore.QRect(390, 110, 350, 200))
        self.crt_scrollArea_2.setWidgetResizable(True)
        self.crt_scrollArea_2.setObjectName("crt_scrollArea_2")
        self.crt_scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.crt_scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 348, 198))
        self.crt_scrollAreaWidgetContents_2.setObjectName("crt_scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.crt_scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("crt_verticalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox.setObjectName("crt_checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox_2.setObjectName("crt_checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox_3.setObjectName("crt_checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox_4.setObjectName("crt_checkBox_4")
        self.verticalLayout.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox_5.setObjectName("crt_checkBox_5")
        self.verticalLayout.addWidget(self.checkBox_5)
        self.checkBox_6 = QtWidgets.QCheckBox(self.crt_scrollAreaWidgetContents_2)
        self.checkBox_6.setObjectName("crt_checkBox_6")
        self.verticalLayout.addWidget(self.checkBox_6)
        self.crt_scrollArea_2.setWidget(self.crt_scrollAreaWidgetContents_2)
        self.crt_scrollArea_2.raise_()
        self.crt_scrollArea.raise_()
        self.crt_label_2.raise_()
        self.crt_pushButton_7.raise_()
        self.crt_label_12.raise_()
        self.crt_pushButton.raise_()
        self.crt_pushButton_2.raise_()
        self.crt_textEdit.raise_()
        self.crt_lineEdit.raise_()
        self.crt_horizontalSlider_11.raise_()
        self.crt_label_13.raise_()

        self.crt_retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)

    def crt_retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle(_translate("self.form", "Mixology"))
        self.crt_label_2.setText(_translate("self.form", "    CREAR"))
        self.crt_pushButton_7.setText(_translate("self.form", "X"))
        self.crt_label_13.setText(_translate("self.form", "Nombre"))
        self.crt_label_12.setText(_translate("self.form", "Mezclar"))
        self.crt_textEdit.setHtml(_translate("self.form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"))
        self.crt_label.setText(_translate("self.form", self.dat.bottles['1'][0])+("\t\t"if len(self.dat.bottles['1'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider.value())+" ml")
        self.crt_label_3.setText(_translate("self.form", self.dat.bottles['2'][0])+("\t\t"if len(self.dat.bottles['2'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_2.value())+" ml")
        self.crt_label_4.setText(_translate("self.form", self.dat.bottles['3'][0])+("\t\t"if len(self.dat.bottles['3'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_3.value())+" ml")
        self.crt_label_5.setText(_translate("self.form", self.dat.bottles['4'][0])+("\t\t"if len(self.dat.bottles['4'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_4.value())+" ml")
        self.crt_label_6.setText(_translate("self.form", self.dat.bottles['5'][0])+("\t\t"if len(self.dat.bottles['5'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_5.value())+" ml")
        self.crt_label_7.setText(_translate("self.form", self.dat.bottles['6'][0])+("\t\t"if len(self.dat.bottles['6'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_6.value())+" ml")
        self.crt_label_8.setText(_translate("self.form", self.dat.bottles['7'][0])+("\t\t"if len(self.dat.bottles['7'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_7.value())+" ml")
        self.crt_label_9.setText(_translate("self.form", self.dat.bottles['8'][0])+("\t\t"if len(self.dat.bottles['8'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_8.value())+" ml")
        self.crt_label_10.setText(_translate("self.form", self.dat.bottles['9'][0])+("\t\t"if len(self.dat.bottles['9'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_9.value())+" ml")
        self.crt_label_11.setText(_translate("self.form", self.dat.bottles['10'][0])+("\t\t"if len(self.dat.bottles['10'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_10.value())+" ml")
        
        self.checkBox.setText(_translate("self.form", self.dat.boxes["1"]))
        self.checkBox_2.setText(_translate("self.form", self.dat.boxes["2"]))
        self.checkBox_3.setText(_translate("self.form", self.dat.boxes["3"]))
        self.checkBox_4.setText(_translate("self.form", self.dat.boxes["4"]))
        self.checkBox_5.setText(_translate("self.form", self.dat.boxes["5"]))
        self.checkBox_6.setText(_translate("self.form", self.dat.boxes["6"]))
    
    def crt_update_val(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle("Mixology")                
        self.crt_horizontalSlider.setValue(int(self.crt_horizontalSlider.value()/50)*50)
        self.crt_horizontalSlider_2.setValue(int(self.crt_horizontalSlider_2.value()/50)*50)
        self.crt_horizontalSlider_3.setValue(int(self.crt_horizontalSlider_3.value()/50)*50)
        self.crt_horizontalSlider_4.setValue(int(self.crt_horizontalSlider_4.value()/50)*50)
        self.crt_horizontalSlider_5.setValue(int(self.crt_horizontalSlider_5.value()/50)*50)
        self.crt_horizontalSlider_6.setValue(int(self.crt_horizontalSlider_6.value()/50)*50)
        self.crt_horizontalSlider_7.setValue(int(self.crt_horizontalSlider_7.value()/50)*50)
        self.crt_horizontalSlider_8.setValue(int(self.crt_horizontalSlider_8.value()/50)*50)
        self.crt_horizontalSlider_9.setValue(int(self.crt_horizontalSlider_9.value()/50)*50)
        self.crt_horizontalSlider_10.setValue(int(self.crt_horizontalSlider_10.value()/50)*50)
        self.crt_label.setText(_translate("self.form", self.dat.bottles['1'][0])+("\t\t"if len(self.dat.bottles['1'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider.value())+" ml")
        self.crt_label_3.setText(_translate("self.form", self.dat.bottles['2'][0])+("\t\t"if len(self.dat.bottles['2'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_2.value())+" ml")
        self.crt_label_4.setText(_translate("self.form", self.dat.bottles['3'][0])+("\t\t"if len(self.dat.bottles['3'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_3.value())+" ml")
        self.crt_label_5.setText(_translate("self.form", self.dat.bottles['4'][0])+("\t\t"if len(self.dat.bottles['4'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_4.value())+" ml")
        self.crt_label_6.setText(_translate("self.form", self.dat.bottles['5'][0])+("\t\t"if len(self.dat.bottles['5'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_5.value())+" ml")
        self.crt_label_7.setText(_translate("self.form", self.dat.bottles['6'][0])+("\t\t"if len(self.dat.bottles['6'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_6.value())+" ml")
        self.crt_label_8.setText(_translate("self.form", self.dat.bottles['7'][0])+("\t\t"if len(self.dat.bottles['7'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_7.value())+" ml")
        self.crt_label_9.setText(_translate("self.form", self.dat.bottles['8'][0])+("\t\t"if len(self.dat.bottles['8'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_8.value())+" ml")
        self.crt_label_10.setText(_translate("self.form", self.dat.bottles['9'][0])+("\t\t"if len(self.dat.bottles['9'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_9.value())+" ml")
        self.crt_label_11.setText(_translate("self.form", self.dat.bottles['10'][0])+("\t\t"if len(self.dat.bottles['10'][0])<8 else "\t")+"\n"+str(self.crt_horizontalSlider_10.value())+" ml")

    def crt_save(self):
        name = (self.crt_lineEdit.text().title())
        ingredients = ((
              (str(self.dat.bottles['1'][0])+"," if self.crt_horizontalSlider.value() > 0 else "")+
              (str(self.dat.bottles['2'][0])+"," if self.crt_horizontalSlider_2.value() > 0 else "")+
              (str(self.dat.bottles['3'][0])+"," if self.crt_horizontalSlider_3.value() > 0 else "")+
              (str(self.dat.bottles['4'][0])+"," if self.crt_horizontalSlider_4.value() > 0 else "")+
              (str(self.dat.bottles['5'][0])+"," if self.crt_horizontalSlider_5.value() > 0 else "")+
              (str(self.dat.bottles['6'][0])+"," if self.crt_horizontalSlider_6.value() > 0 else "")+
              (str(self.dat.bottles['7'][0])+"," if self.crt_horizontalSlider_7.value() > 0 else "")+
              (str(self.dat.bottles['8'][0])+"," if self.crt_horizontalSlider_8.value() > 0 else "")+
              (str(self.dat.bottles['9'][0])+"," if self.crt_horizontalSlider_9.value() > 0 else "")+
              (str(self.dat.bottles['10'][0])+"," if self.crt_horizontalSlider_10.value() > 0 else "")
        )[:-1])
        volume = ((
              (str(self.crt_horizontalSlider.value())+"," if self.crt_horizontalSlider.value() > 0 else "")+
              (str(self.crt_horizontalSlider_2.value())+"," if self.crt_horizontalSlider_2.value() > 0 else "")+
              (str(self.crt_horizontalSlider_3.value())+"," if self.crt_horizontalSlider_3.value() > 0 else "")+
              (str(self.crt_horizontalSlider_4.value())+"," if self.crt_horizontalSlider_4.value() > 0 else "")+
              (str(self.crt_horizontalSlider_5.value())+"," if self.crt_horizontalSlider_5.value() > 0 else "")+
              (str(self.crt_horizontalSlider_6.value())+"," if self.crt_horizontalSlider_6.value() > 0 else "")+
              (str(self.crt_horizontalSlider_7.value())+"," if self.crt_horizontalSlider_7.value() > 0 else "")+
              (str(self.crt_horizontalSlider_8.value())+"," if self.crt_horizontalSlider_8.value() > 0 else "")+
              (str(self.crt_horizontalSlider_9.value())+"," if self.crt_horizontalSlider_9.value() > 0 else "")+
              (str(self.crt_horizontalSlider_10.value())+"," if self.crt_horizontalSlider_10.value() > 0 else "")
        )[:-1])
        boxes = ((
              (str(self.dat.boxes['1'])+"," if self.checkBox.isChecked() else "")+
              (str(self.dat.boxes['2'])+"," if self.checkBox_2.isChecked() else "")+
              (str(self.dat.boxes['3'])+"," if self.checkBox_3.isChecked() else "")+
              (str(self.dat.boxes['4'])+"," if self.checkBox_4.isChecked() else "")+
              (str(self.dat.boxes['5'])+"," if self.checkBox_5.isChecked() else "")+
              (str(self.dat.boxes['6'])+"," if self.checkBox_6.isChecked() else "")
        )[:-1])
        boxes = boxes if len(boxes) > 0 else " "
        mix = ((False, True)[self.crt_horizontalSlider_11.value()])

        # Validators
        if sum((self.crt_horizontalSlider.value(), self.crt_horizontalSlider_2.value(), self.crt_horizontalSlider_3.value(), self.crt_horizontalSlider_4.value(), self.crt_horizontalSlider_5.value(), self.crt_horizontalSlider_6.value(), self.crt_horizontalSlider_7.value(), self.crt_horizontalSlider_8.value(), self.crt_horizontalSlider_9.value(), self.crt_horizontalSlider_10.value())) > 500:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Máximo: 500 ml")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()
        elif (not len(name)):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Falta nombre en la bebida")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()
        elif len(self.dat.df.ID) == 9:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No hay más espacio para bebidas")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.dat.add_recipe(name,ingredients,volume,boxes,mix)
            self.dat.__init__()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Tu receta fue guardada")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Guardado")
            msg.exec_()
            self.crt_lineEdit.setText("")
            self.crt_label.setText(self.dat.bottles['1'][0]+("\t\t"if len(self.dat.bottles['1'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_3.setText(self.dat.bottles['2'][0]+("\t\t"if len(self.dat.bottles['2'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_4.setText(self.dat.bottles['3'][0]+("\t\t"if len(self.dat.bottles['3'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_5.setText(self.dat.bottles['10'][0]+("\t\t"if len(self.dat.bottles['4'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_6.setText(self.dat.bottles['4'][0]+("\t\t"if len(self.dat.bottles['5'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_7.setText(self.dat.bottles['5'][0]+("\t\t"if len(self.dat.bottles['6'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_8.setText(self.dat.bottles['6'][0]+("\t\t"if len(self.dat.bottles['7'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_9.setText(self.dat.bottles['7'][0]+("\t\t"if len(self.dat.bottles['8'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_11.setText(self.dat.bottles['8'][0]+("\t\t"if len(self.dat.bottles['9'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_label_10.setText(self.dat.bottles['9'][0]+("\t\t"if len(self.dat.bottles['10'][0])<8 else "\t")+"\n"+"0 ml")
            self.crt_horizontalSlider.setValue(0)
            self.crt_horizontalSlider_2.setValue(0)
            self.crt_horizontalSlider_3.setValue(0)
            self.crt_horizontalSlider_4.setValue(0)
            self.crt_horizontalSlider_5.setValue(0)
            self.crt_horizontalSlider_6.setValue(0)
            self.crt_horizontalSlider_7.setValue(0)
            self.crt_horizontalSlider_8.setValue(0)
            self.crt_horizontalSlider_9.setValue(0)
            self.crt_horizontalSlider_10.setValue(0)
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)

    #endregion create
    
    #region calibrate
    def calibrate_form(self):
        self.form.setObjectName("cal_form")
        self.form.resize(800, 380)
        self.cal_pushButton_7 = QtWidgets.QPushButton(self.form)
        self.cal_pushButton_7.setGeometry(QtCore.QRect(720, 20, 41, 31))
        self.cal_pushButton_7.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 10px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;")
        self.cal_pushButton_7.setObjectName("cal_pushButton_7")
        self.cal_pushButton_7.clicked.connect(lambda: sys.exit(0))
        self.cal_label_2 = QtWidgets.QLabel(self.form)
        self.cal_label_2.setGeometry(QtCore.QRect(0, 0, 800, 74))
        self.cal_label_2.setStyleSheet("font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: bold;\n"
        "font-size: 36px;\n"
        "line-height: 42px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "background-color: #E09825;")
        self.cal_label_2.setObjectName("cal_label_2")
        self.cal_pushButton_10 = QtWidgets.QPushButton(self.form)
        self.cal_pushButton_10.setGeometry(QtCore.QRect(10, 310, 65, 65))
        self.cal_pushButton_10.setStyleSheet("\n"
        "border-image: url(:/back/assets/back.png);\n"
        "border-radius:30px")
        self.cal_pushButton_10.setText("")
        self.cal_pushButton_10.setObjectName("cal_pushButton_10")
        self.cal_pushButton_10.setIcon(QIcon('assets/back.png'))
        self.cal_pushButton_10.setIconSize(QtCore.QSize(50, 50))
        self.cal_pushButton_10.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.cal_pushButton_10.clicked.connect(lambda: self.state_machine(0))
        self.cal_pushButton_11 = QtWidgets.QPushButton(self.form)
        self.cal_pushButton_11.setGeometry(QtCore.QRect(720, 310, 65, 65))
        self.cal_pushButton_11.setStyleSheet("\n"
        "border-image: url(:/check/assets/check2.png);\n"
        "border-radius:30px\n"
        "")
        self.cal_pushButton_11.setText("")
        self.cal_pushButton_11.setObjectName("cal_pushButton_11")
        self.cal_pushButton_11.setIcon(QIcon('assets/check2.png'))
        self.cal_pushButton_11.setIconSize(QtCore.QSize(50, 50))
        self.cal_pushButton_11.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.cal_pushButton_11.clicked.connect(self.cal_save)

        #region Scroll 1
        self.cal_scrollArea = QtWidgets.QScrollArea(self.form)
        self.cal_scrollArea.setGeometry(QtCore.QRect(30, 80, 550, 200))
        self.cal_scrollArea.setWidgetResizable(True)
        self.cal_scrollArea.setObjectName("cal_scrollArea")
        self.cal_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.cal_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 534, 472))
        self.cal_scrollAreaWidgetContents.setObjectName("cal_scrollAreaWidgetContents")
        self.cal_gridLayout = QtWidgets.QGridLayout(self.cal_scrollAreaWidgetContents)
        self.cal_gridLayout.setObjectName("cal_gridLayout")
        self.cal_lineEdit_12 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_12.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_12.setObjectName("cal_lineEdit_12")
        self.cal_lineEdit_12.setText(self.dat.bottles["1"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_12, 0, 2, 1, 1)

        
        self.cal_lineEdit_15 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_15.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_15.setObjectName("cal_lineEdit_15")
        self.cal_lineEdit_15.setText(self.dat.bottles["2"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_15, 1, 2, 1, 1)

        
        self.cal_horizontalSlider = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider.setObjectName("cal_horizontalSlider")
        self.cal_horizontalSlider.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider, 0, 3, 1, 1)

        self.cal_lineEdit_10 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_10.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_10.setObjectName("cal_lineEdit_10")
        self.cal_lineEdit_10.setText(self.dat.bottles["3"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_10, 2, 2, 1, 1)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_horizontalSlider.sizePolicy().hasHeightForWidth())

        self.cal_horizontalSlider_2 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_2.setSizePolicy(sizePolicy)
        self.cal_horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_2.setObjectName("cal_horizontalSlider_2")
        self.cal_horizontalSlider_2.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_2, 1, 3, 1, 1)

        self.cal_horizontalSlider_3 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_3.setObjectName("cal_horizontalSlider_3")
        self.cal_horizontalSlider_3.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_3, 2, 3, 1, 1)

        self.cal_horizontalSlider_4 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_4.setObjectName("cal_horizontalSlider_4")
        self.cal_horizontalSlider_4.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_4, 3, 3, 1, 1)

        self.cal_label_22 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_22.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_22.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_22.setText("Item---1")
        self.cal_label_22.setObjectName("cal_label_22")
        self.cal_gridLayout.addWidget(self.cal_label_22, 0, 4, 1, 1)

        self.cal_horizontalSlider_5 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_5.setObjectName("cal_horizontalSlider_5")
        self.cal_horizontalSlider_5.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_5, 4, 3, 1, 1)

        self.cal_lineEdit_13 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_13.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_13.setObjectName("cal_lineEdit_13")
        self.cal_lineEdit_13.setText(self.dat.bottles["4"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_13, 3, 2, 1, 1)
        
        self.cal_label_26 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_26.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_26.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_26.setText("Item---2")
        self.cal_label_26.setObjectName("cal_label_26")
        self.cal_gridLayout.addWidget(self.cal_label_26, 1, 4, 1, 1)

        self.cal_horizontalSlider_6 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_6.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_6.setObjectName("cal_horizontalSlider_6")
        self.cal_horizontalSlider_6.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_6, 5, 3, 1, 1)

        self.cal_label_18 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_label_18.sizePolicy().hasHeightForWidth())
        self.cal_label_18.setSizePolicy(sizePolicy)
        self.cal_label_18.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_18.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_18.setText("Item---3")
        self.cal_label_18.setObjectName("cal_label_18")
        self.cal_gridLayout.addWidget(self.cal_label_18, 2, 4, 1, 1)

        self.cal_lineEdit_11 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_11.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_11.setObjectName("cal_lineEdit_11")
        self.cal_lineEdit_11.setText(self.dat.bottles["5"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_11, 4, 2, 1, 1)

        
        self.cal_label_19 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_19.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_19.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_19.setText("Item---4")
        self.cal_label_19.setObjectName("cal_label_19")
        self.cal_gridLayout.addWidget(self.cal_label_19, 3, 4, 1, 1)

        self.cal_lineEdit_14 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_14.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_14.setObjectName("cal_lineEdit_14")
        self.cal_lineEdit_14.setText(self.dat.bottles["6"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_14, 5, 2, 1, 1)

        
        self.cal_horizontalSlider_7 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_7.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_7.setObjectName("cal_horizontalSlider_7")
        self.cal_horizontalSlider_7.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_7, 6, 3, 1, 1)

        self.cal_horizontalSlider_8 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_8.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_8.setObjectName("cal_horizontalSlider_8")
        self.cal_horizontalSlider_8.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_8, 7, 3, 1, 1)

        self.cal_horizontalSlider_9 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_9.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_9.setObjectName("cal_horizontalSlider_9")
        self.cal_horizontalSlider_9.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_9, 8, 3, 1, 1)

        self.cal_label_21 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_21.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_21.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_21.setText("Item---5")
        self.cal_label_21.setObjectName("cal_label_21")
        self.cal_gridLayout.addWidget(self.cal_label_21, 4, 4, 1, 1)

        self.cal_lineEdit_9 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_9.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_9.setObjectName("cal_lineEdit_9")
        self.cal_lineEdit_9.setText(self.dat.bottles["7"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_9, 6, 2, 1, 1)

        
        self.cal_label_20 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_20.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_20.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_20.setText("Item---6")
        self.cal_label_20.setObjectName("cal_label_20")
        self.cal_gridLayout.addWidget(self.cal_label_20, 5, 4, 1, 1)

        self.cal_label_24 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_24.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_24.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_24.setText("Item---7")
        self.cal_label_24.setObjectName("cal_label_24")
        self.cal_gridLayout.addWidget(self.cal_label_24, 6, 4, 1, 1)

        self.cal_lineEdit_7 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.cal_lineEdit_7.sizePolicy().hasHeightForWidth())
        self.cal_lineEdit_7.setSizePolicy(sizePolicy)
        self.cal_lineEdit_7.setMinimumSize(QtCore.QSize(30, 40))
        self.cal_lineEdit_7.setObjectName("cal_lineEdit_7")
        self.cal_lineEdit_7.setText(self.dat.bottles["8"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_7, 7, 2, 1, 1)

        
        self.cal_label_23 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_23.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_23.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_23.setText("Item---8")
        self.cal_label_23.setObjectName("cal_label_23")
        self.cal_gridLayout.addWidget(self.cal_label_23, 7, 4, 1, 1)

        self.cal_lineEdit_8 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_8.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_8.setObjectName("cal_lineEdit_8")
        self.cal_lineEdit_8.setText(self.dat.bottles["9"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_8, 8, 2, 1, 1)

        
        self.cal_label_25 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_25.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_25.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_25.setText("Item---9")
        self.cal_label_25.setObjectName("cal_label_25")
        self.cal_gridLayout.addWidget(self.cal_label_25, 8, 4, 1, 1)

        self.cal_lineEdit_16 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents)
        self.cal_lineEdit_16.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_lineEdit_16.setObjectName("cal_lineEdit_16")
        self.cal_lineEdit_16.setText(self.dat.bottles["10"][0])
        self.cal_gridLayout.addWidget(self.cal_lineEdit_16, 9, 2, 1, 1)

        
        self.cal_horizontalSlider_10 = QtWidgets.QSlider(self.cal_scrollAreaWidgetContents)
        self.cal_horizontalSlider_10.setOrientation(QtCore.Qt.Horizontal)
        self.cal_horizontalSlider_10.setObjectName("cal_horizontalSlider_10")
        self.cal_horizontalSlider_10.setStyleSheet(self.slider_formatters())
        self.cal_gridLayout.addWidget(self.cal_horizontalSlider_10, 9, 3, 1, 1)

        self.cal_label_27 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents)
        self.cal_label_27.setMinimumSize(QtCore.QSize(0, 40))
        self.cal_label_27.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.cal_label_27.setText("Item---10")
        self.cal_label_27.setObjectName("cal_label_27")
        self.cal_gridLayout.addWidget(self.cal_label_27, 9, 4, 1, 1)

        self.cal_scrollArea.setWidget(self.cal_scrollAreaWidgetContents)

        #endregion Scroll 1
        
        #region Slider formatter
        self.cal_horizontalSlider.setMaximum(3000)
        self.cal_horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider.setTickInterval(100)


        self.cal_horizontalSlider_2.setMaximum(3000)
        self.cal_horizontalSlider_2.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_2.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_2.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_2.setTickInterval(100)


        self.cal_horizontalSlider_3.setMaximum(3000)
        self.cal_horizontalSlider_3.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_3.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_3.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_3.setTickInterval(100)


        self.cal_horizontalSlider_4.setMaximum(3000)
        self.cal_horizontalSlider_4.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_4.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_4.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_4.setTickInterval(100)


        self.cal_horizontalSlider_5.setMaximum(3000)
        self.cal_horizontalSlider_5.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_5.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_5.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_5.setTickInterval(100)


        self.cal_horizontalSlider_6.setMaximum(3000)
        self.cal_horizontalSlider_6.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_6.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_6.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_6.setTickInterval(100)


        self.cal_horizontalSlider_7.setMaximum(3000)
        self.cal_horizontalSlider_7.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_7.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_7.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_7.setTickInterval(100)


        self.cal_horizontalSlider_8.setMaximum(3000)
        self.cal_horizontalSlider_8.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_8.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_8.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_8.setTickInterval(100)


        self.cal_horizontalSlider_9.setMaximum(3000)
        self.cal_horizontalSlider_9.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_9.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_9.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_9.setTickInterval(100)


        self.cal_horizontalSlider_10.setMaximum(3000)
        self.cal_horizontalSlider_10.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_10.valueChanged.connect(self.cal_update_val)
        self.cal_horizontalSlider_10.setTickPosition(QSlider.TicksBelow)
        self.cal_horizontalSlider_10.setTickInterval(100)
        #endregion Slider formatter

        #region Scroll 2
        self.cal_scrollArea_2 = QtWidgets.QScrollArea(self.form)
        self.cal_scrollArea_2.setGeometry(QtCore.QRect(600, 80, 162, 200))
        self.cal_scrollArea_2.setWidgetResizable(True)
        self.cal_scrollArea_2.setObjectName("cal_scrollArea_2")
        self.cal_scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.cal_scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 146, 336))
        self.cal_scrollAreaWidgetContents_2.setObjectName("cal_scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.cal_scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("cal_verticalLayout")
        self.cal_label_12 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_12.setObjectName("cal_label_12")
        self.verticalLayout.addWidget(self.cal_label_12)
        self.cal_lineEdit = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit.setObjectName("cal_lineEdit")
        self.cal_lineEdit.setText(self.dat.boxes['1'])

        self.verticalLayout.addWidget(self.cal_lineEdit)
        self.cal_label_13 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_13.setObjectName("cal_label_13")
        self.verticalLayout.addWidget(self.cal_label_13)
        self.cal_lineEdit_2 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit_2.setObjectName("cal_lineEdit_2")
        self.cal_lineEdit_2.setText(self.dat.boxes['2'])
        
        self.verticalLayout.addWidget(self.cal_lineEdit_2)
        self.cal_label_14 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_14.setObjectName("cal_label_14")
        self.verticalLayout.addWidget(self.cal_label_14)
        self.cal_lineEdit_3 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit_3.setObjectName("cal_lineEdit_3")
        self.cal_lineEdit_3.setText(self.dat.boxes['3'])
        
        self.verticalLayout.addWidget(self.cal_lineEdit_3)
        self.cal_label_15 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_15.setObjectName("cal_label_15")
        self.verticalLayout.addWidget(self.cal_label_15)
        self.cal_lineEdit_4 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit_4.setObjectName("cal_lineEdit_4")
        self.cal_lineEdit_4.setText(self.dat.boxes['4'])
        
        self.verticalLayout.addWidget(self.cal_lineEdit_4)
        self.cal_label_16 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_16.setObjectName("cal_label_16")
        self.verticalLayout.addWidget(self.cal_label_16)
        self.cal_lineEdit_5 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit_5.setObjectName("cal_lineEdit_5")
        self.cal_lineEdit_5.setText(self.dat.boxes['5'])
        
        self.verticalLayout.addWidget(self.cal_lineEdit_5)
        self.cal_label_17 = QtWidgets.QLabel(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_17.setObjectName("cal_label_17")
        self.verticalLayout.addWidget(self.cal_label_17)
        self.cal_lineEdit_6 = QtWidgets.QLineEdit(self.cal_scrollAreaWidgetContents_2)
        self.cal_lineEdit_6.setObjectName("cal_lineEdit_6")
        self.cal_lineEdit_6.setText(self.dat.boxes['6'])
        
        self.verticalLayout.addWidget(self.cal_lineEdit_6)
        self.cal_scrollArea_2.setWidget(self.cal_scrollAreaWidgetContents_2)
        self.cal_label_2.raise_()
        self.cal_pushButton_7.raise_()
        self.cal_pushButton_11.raise_()
        self.cal_pushButton_10.raise_()
        self.cal_scrollArea.raise_()
        self.cal_scrollArea_2.raise_()
        #endregion Scroll 2

        self.cal_retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)

    def cal_update_val(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle("Mixology")

        self.cal_horizontalSlider.setValue(int(self.cal_horizontalSlider.value()/100)*100)
        self.cal_horizontalSlider_2.setValue(int(self.cal_horizontalSlider_2.value()/100)*100)
        self.cal_horizontalSlider_3.setValue(int(self.cal_horizontalSlider_3.value()/100)*100)
        self.cal_horizontalSlider_4.setValue(int(self.cal_horizontalSlider_4.value()/100)*100)
        self.cal_horizontalSlider_5.setValue(int(self.cal_horizontalSlider_5.value()/100)*100)
        self.cal_horizontalSlider_6.setValue(int(self.cal_horizontalSlider_6.value()/100)*100)
        self.cal_horizontalSlider_7.setValue(int(self.cal_horizontalSlider_7.value()/100)*100)
        self.cal_horizontalSlider_8.setValue(int(self.cal_horizontalSlider_8.value()/100)*100)
        self.cal_horizontalSlider_9.setValue(int(self.cal_horizontalSlider_9.value()/100)*100)
        self.cal_horizontalSlider_10.setValue(int(self.cal_horizontalSlider_10.value()/100)*100)

        self.cal_label_22.setText(str(self.cal_horizontalSlider.value())+" ml")
        self.cal_label_26.setText(str(self.cal_horizontalSlider_2.value())+" ml")
        self.cal_label_18.setText(str(self.cal_horizontalSlider_3.value())+" ml")
        self.cal_label_19.setText(str(self.cal_horizontalSlider_4.value())+" ml")
        self.cal_label_21.setText(str(self.cal_horizontalSlider_5.value())+" ml")
        self.cal_label_20.setText(str(self.cal_horizontalSlider_6.value())+" ml")
        self.cal_label_24.setText(str(self.cal_horizontalSlider_7.value())+" ml")
        self.cal_label_23.setText(str(self.cal_horizontalSlider_8.value())+" ml")
        self.cal_label_25.setText(str(self.cal_horizontalSlider_9.value())+" ml")
        self.cal_label_27.setText(str(self.cal_horizontalSlider_10.value())+" ml")

    def cal_retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle(_translate("self.form", "Mixology"))
        self.cal_pushButton_7.setText(_translate("self.form", "X"))
        self.cal_label_2.setText(_translate("self.form", "    CALIBRAR"))
        self.cal_label_12.setText(_translate("self.form", "Cajón 1"))
        self.cal_label_13.setText(_translate("self.form", "Cajón 2"))
        self.cal_label_14.setText(_translate("self.form", "Cajón 3"))
        self.cal_label_15.setText(_translate("self.form", "Cajón 4"))
        self.cal_label_16.setText(_translate("self.form", "Cajón 5"))
        self.cal_label_17.setText(_translate("self.form", "Cajón 6"))
        self.cal_label_22.setText(str(self.dat.bottles["1"][1])+" ml")
        self.cal_label_26.setText(str(self.dat.bottles["2"][1])+" ml")
        self.cal_label_18.setText(str(self.dat.bottles["3"][1])+" ml")
        self.cal_label_19.setText(str(self.dat.bottles["4"][1])+" ml")
        self.cal_label_21.setText(str(self.dat.bottles["5"][1])+" ml")
        self.cal_label_20.setText(str(self.dat.bottles["6"][1])+" ml")
        self.cal_label_24.setText(str(self.dat.bottles["7"][1])+" ml")
        self.cal_label_23.setText(str(self.dat.bottles["8"][1])+" ml")
        self.cal_label_25.setText(str(self.dat.bottles["9"][1])+" ml")
        self.cal_label_27.setText(str(self.dat.bottles["10"][1])+" ml")
        self.cal_horizontalSlider.setValue(int(self.dat.bottles["1"][1]))
        self.cal_horizontalSlider_2.setValue(int(self.dat.bottles["2"][1]))
        self.cal_horizontalSlider_3.setValue(int(self.dat.bottles["3"][1]))
        self.cal_horizontalSlider_4.setValue(int(self.dat.bottles["4"][1]))
        self.cal_horizontalSlider_5.setValue(int(self.dat.bottles["5"][1]))
        self.cal_horizontalSlider_6.setValue(int(self.dat.bottles["6"][1]))
        self.cal_horizontalSlider_7.setValue(int(self.dat.bottles["7"][1]))
        self.cal_horizontalSlider_8.setValue(int(self.dat.bottles["8"][1]))
        self.cal_horizontalSlider_9.setValue(int(self.dat.bottles["9"][1]))
        self.cal_horizontalSlider_10.setValue(int(self.dat.bottles["10"][1]))
        
    def cal_change_validator(self, num, name, value):
        if self.dat.bottles[str(num)][0] != name and value == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Por qué estás colocando una botella vacía?\nIngresa el contenido de "+name)
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()
            return False
        return True

    def cal_save(self):
        validator = True
        for x,y,z in zip(range(1,10),(self.cal_lineEdit_12.text(),self.cal_lineEdit_15.text(),self.cal_lineEdit_10.text(),self.cal_lineEdit_13.text(),self.cal_lineEdit_11.text(),self.cal_lineEdit_14.text(),self.cal_lineEdit_9.text(),self.cal_lineEdit_7.text(),self.cal_lineEdit_8.text(),self.cal_lineEdit_16.text()),(self.cal_horizontalSlider.value(),self.cal_horizontalSlider_2.value(),self.cal_horizontalSlider_3.value(),self.cal_horizontalSlider_4.value(),self.cal_horizontalSlider_5.value(),self.cal_horizontalSlider_6.value(),self.cal_horizontalSlider_7.value(),self.cal_horizontalSlider_8.value(),self.cal_horizontalSlider_9.value(),self.cal_horizontalSlider_10.value())):
            if not self.cal_change_validator(x,y,z):
                validator = False
                break
        if validator:
            changes = not((self.cal_lineEdit_12.text() == self.dat.bottles["1"][0])and(self.cal_lineEdit_15.text() == self.dat.bottles["2"][0])and(self.cal_lineEdit_10.text() == self.dat.bottles["3"][0])and(self.cal_lineEdit_13.text() == self.dat.bottles["4"][0])and(self.cal_lineEdit_11.text() == self.dat.bottles["5"][0])and(self.cal_lineEdit_14.text() == self.dat.bottles["6"][0])and(self.cal_lineEdit_9.text() == self.dat.bottles["7"][0])and(self.cal_lineEdit_7.text() == self.dat.bottles["8"][0])and(self.cal_lineEdit_8.text() == self.dat.bottles["9"][0])and(self.cal_lineEdit_16.text() == self.dat.bottles["10"][0]))
            bot = []
            bot.append(1 if self.cal_lineEdit_12.text() != self.dat.bottles["1"][0] else "NONE")
            bot.append(2 if self.cal_lineEdit_15.text() != self.dat.bottles["2"][0] else "NONE")
            bot.append(3 if self.cal_lineEdit_10.text() != self.dat.bottles["3"][0] else "NONE")
            bot.append(4 if self.cal_lineEdit_13.text() != self.dat.bottles["4"][0] else "NONE")
            bot.append(5 if self.cal_lineEdit_11.text() != self.dat.bottles["5"][0] else "NONE")
            bot.append(6 if self.cal_lineEdit_14.text() != self.dat.bottles["6"][0] else "NONE")
            bot.append(7 if self.cal_lineEdit_9.text() != self.dat.bottles["7"][0] else "NONE")
            bot.append(8 if self.cal_lineEdit_7.text() != self.dat.bottles["8"][0] else "NONE")
            bot.append(9 if self.cal_lineEdit_8.text() != self.dat.bottles["9"][0] else "NONE")
            bot.append(10 if self.cal_lineEdit_16.text() != self.dat.bottles["10"][0] else "NONE")
            
            try:
                while True:
                    bot.remove("NONE")
            except ValueError:
                pass
            
            self.dat.__init__()
            self.dat.change_bottle(1,self.cal_lineEdit_12.text().title(),self.cal_horizontalSlider.value())
            self.dat.change_bottle(2,self.cal_lineEdit_15.text().title(),self.cal_horizontalSlider_2.value())
            self.dat.change_bottle(3,self.cal_lineEdit_10.text().title(),self.cal_horizontalSlider_3.value())
            self.dat.change_bottle(4,self.cal_lineEdit_13.text().title(),self.cal_horizontalSlider_4.value())
            self.dat.change_bottle(5,self.cal_lineEdit_11.text().title(),self.cal_horizontalSlider_5.value())
            self.dat.change_bottle(6,self.cal_lineEdit_14.text().title(),self.cal_horizontalSlider_6.value())
            self.dat.change_bottle(7,self.cal_lineEdit_9.text().title(),self.cal_horizontalSlider_7.value())
            self.dat.change_bottle(8,self.cal_lineEdit_7.text().title(),self.cal_horizontalSlider_8.value())
            self.dat.change_bottle(9,self.cal_lineEdit_8.text().title(),self.cal_horizontalSlider_9.value())
            self.dat.change_bottle(10,self.cal_lineEdit_16.text().title(),self.cal_horizontalSlider_10.value())
            self.dat.change_box(1,self.cal_lineEdit.text().title())
            self.dat.change_box(2,self.cal_lineEdit_2.text().title())
            self.dat.change_box(3,self.cal_lineEdit_3.text().title())
            self.dat.change_box(4,self.cal_lineEdit_4.text().title())
            self.dat.change_box(5,self.cal_lineEdit_5.text().title())
            self.dat.change_box(6,self.cal_lineEdit_6.text().title())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Información actualizada")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Completado")
            msg.exec_()
            
            if changes:
                self.dat.__init__()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Para calibrar las bombas se servirá un poco del contenido de las botellas,\npor favor, coloca un recipiente")
                # msg.setInformativeText('More information')
                msg.setWindowTitle("Cambio de botella")
                msg.exec_()
                [self.dat.change_bottle(x,y,z) for x,y,z in zip([w+1 for w in bot],[self.dat.bottles[str(w+1)][0] for w in bot],[self.dat.bottles[str(w+1)][1]-100 for w in bot])]
                self.ctr.pump_control(bot, [100 for _ in bot], [0.035 for _ in bot])
                
    #endregion calibrate

    #region select    
    def select_form(self):
        self.form.setObjectName("Form")
        self.form.resize(800, 380)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.form.setFont(font)
        self.sel_pushButton_8 = QtWidgets.QPushButton(self.form)
        self.sel_pushButton_8.setGeometry(QtCore.QRect(730, 30, 41, 31))
        self.sel_pushButton_8.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 10px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;")
        self.sel_pushButton_8.setObjectName("pushButton_8")
        self.sel_label_18 = QtWidgets.QLabel(self.form)
        self.sel_label_18.setGeometry(QtCore.QRect(0, 0, 800, 74))
        self.sel_label_18.setStyleSheet("font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: bold;\n"
        "font-size: 36px;\n"
        "line-height: 42px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "background-color: #E09825;")
        self.sel_label_18.setObjectName("label_18")
        self.sel_pushButton_9 = QtWidgets.QPushButton(self.form)
        self.sel_pushButton_9.setGeometry(QtCore.QRect(720, 20, 41, 31))
        self.sel_pushButton_9.setStyleSheet("background: #AA0000;\n"
        "border: 0.5px solid rgba(255, 255, 255, 0.48);\n"
        "border-radius: 10px;\n"
        "\n"
        "font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: normal;\n"
        "font-size: 18px;\n"
        "line-height: 28px;\n"
        "\n"
        "color: #FFFFFF;") 
        self.sel_pushButton_9.setObjectName("pushButton_9")
        self.sel_pushButton_9.clicked.connect(lambda: sys.exit(0))
        self.sel_pushButton = QtWidgets.QPushButton(self.form)
        self.sel_pushButton.setGeometry(QtCore.QRect(10, 310, 65, 65))
        self.sel_pushButton.setStyleSheet("border-image: url(:/back/assets/back.png);\n"
        "\n"
        "border-radius:30px")
        self.sel_pushButton.setText("")
        self.sel_pushButton.setIcon(QIcon('assets/back.png'))
        self.sel_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.sel_pushButton.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.sel_pushButton.setObjectName("pushButton")
        self.sel_pushButton.clicked.connect(lambda: self.state_machine(0))
        self.sel_scrollArea = QtWidgets.QScrollArea(self.form)
        self.sel_scrollArea.setGeometry(QtCore.QRect(70, 80, 651, 200))
        self.sel_scrollArea.setWidgetResizable(True)
        self.sel_scrollArea.setObjectName("scrollArea")
        self.sel_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.sel_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -228, 635, 426))
        self.sel_scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.sel_gridLayout = QtWidgets.QGridLayout(self.sel_scrollAreaWidgetContents)
        self.sel_gridLayout.setObjectName("gridLayout")
        self.sel_label_7 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_7.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_7.setFont(font)
        self.sel_label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_7.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;")
        self.sel_label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_7.setObjectName("label_7")
        self.sel_gridLayout.addWidget(self.sel_label_7, 0, 3, 1, 1)
        self.sel_label_16 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_16.setFont(font)
        self.sel_label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_16.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;")
        self.sel_label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_16.setObjectName("label_16")
        self.sel_gridLayout.addWidget(self.sel_label_16, 1, 3, 1, 1)
        self.sel_label_36 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_36.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_36.setFont(font)
        self.sel_label_36.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n"
        "\n"
        "\n"
        "\n"
        "")
        self.sel_label_36.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_36.setObjectName("label_36")
        self.sel_gridLayout.addWidget(self.sel_label_36, 0, 1, 1, 1)
        self.sel_label_32 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_32.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_32.setFont(font)
        self.sel_label_32.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;\n"
        "\n"
        "\n"
        "")
        self.sel_label_32.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_32.setObjectName("label_32")
        self.sel_gridLayout.addWidget(self.sel_label_32, 1, 1, 1, 1)
        self.sel_label_33 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_33.setFont(font)
        self.sel_label_33.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_33.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;")
        self.sel_label_33.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_33.setObjectName("label_33")
        self.sel_gridLayout.addWidget(self.sel_label_33, 2, 3, 1, 1)
        self.sel_label_22 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_22.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_22.setFont(font)
        self.sel_label_22.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n"
        "\n"
        "\n"
        "")
        self.sel_label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_22.setObjectName("label_22")
        self.sel_gridLayout.addWidget(self.sel_label_22, 2, 1, 1, 1)
        self.sel_label_23 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_23.setFont(font)
        self.sel_label_23.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_23.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;")
        self.sel_label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_23.setObjectName("label_23")
        self.sel_gridLayout.addWidget(self.sel_label_23, 3, 3, 1, 1)
        self.sel_label_40 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_40.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_40.setFont(font)
        self.sel_label_40.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;\n"
        "\n"
        "\n"
        "")
        self.sel_label_40.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_40.setObjectName("label_40")
        self.sel_gridLayout.addWidget(self.sel_label_40, 3, 1, 1, 1)
        self.sel_label_31 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_31.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_31.setFont(font)
        self.sel_label_31.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n"
        "\n"
        "\n"
        "")
        self.sel_label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_31.setObjectName("label_31")
        self.sel_gridLayout.addWidget(self.sel_label_31, 4, 1, 1, 1)
        self.sel_label_28 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_28.setFont(font)
        self.sel_label_28.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_28.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;")
        self.sel_label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_28.setObjectName("label_28")
        self.sel_gridLayout.addWidget(self.sel_label_28, 4, 3, 1, 1)
        self.sel_label_24 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_24.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_24.setFont(font)
        self.sel_label_24.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;\n"
        "\n"
        "\n"
        "")
        self.sel_label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_24.setObjectName("label_24")
        self.sel_gridLayout.addWidget(self.sel_label_24, 5, 1, 1, 1)
        self.sel_label_19 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_19.setFont(font)
        self.sel_label_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_19.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;")
        self.sel_label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_19.setObjectName("label_19")
        self.sel_gridLayout.addWidget(self.sel_label_19, 5, 3, 1, 1)
        self.sel_label_38 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_38.setFont(font)
        self.sel_label_38.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_38.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;")
        self.sel_label_38.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_38.setObjectName("label_38")
        self.sel_gridLayout.addWidget(self.sel_label_38, 6, 3, 1, 1)
        self.sel_label_37 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_37.setFont(font)
        self.sel_label_37.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_37.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n")
        self.sel_label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_37.setObjectName("label_37")
        self.sel_gridLayout.addWidget(self.sel_label_37, 7, 3, 1, 1)
        self.sel_label_20 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_20.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_20.setFont(font)
        self.sel_label_20.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n"
        "\n"
        "\n"
        "")
        self.sel_label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_20.setObjectName("label_20")
        self.sel_gridLayout.addWidget(self.sel_label_20, 6, 1, 1, 1)
        self.sel_label_30 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_30.setFont(font)
        self.sel_label_30.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sel_label_30.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;")
        self.sel_label_30.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_30.setObjectName("label_30")
        self.sel_gridLayout.addWidget(self.sel_label_30, 8, 3, 1, 1)
        self.sel_label_25 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_25.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_25.setFont(font)
        self.sel_label_25.setStyleSheet("background-color: rgb(186, 189, 182);\n"
        "color: #000000;\n"
        "\n"
        "\n"
        "")
        self.sel_label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_25.setObjectName("label_25")
        self.sel_gridLayout.addWidget(self.sel_label_25, 7, 1, 1, 1)
        self.sel_label_41 = QtWidgets.QLabel(self.sel_scrollAreaWidgetContents)
        self.sel_label_41.setMinimumSize(QtCore.QSize(0, 40))
        self.sel_label_41.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sel_label_41.setBaseSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_label_41.setFont(font)
        self.sel_label_41.setStyleSheet("background-color: rgb(136, 138, 133);\n"
        "color: #FFFFFF;\n"
        "\n"
        "\n"
        "")
        self.sel_label_41.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_label_41.setObjectName("label_41")
        self.sel_gridLayout.addWidget(self.sel_label_41, 8, 1, 1, 1)
        self.sel_pushButton_3 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_3.setObjectName("pushButton_3")
        self.sel_pushButton_3.clicked.connect(lambda: self.sel_add_to_queue(1,[self.sel_pushButton_3,self.sel_label_36,self.sel_label_7]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_3, 0, 0, 1, 1)
        self.sel_pushButton_4 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_4.setObjectName("pushButton_4")
        self.sel_pushButton_4.clicked.connect(lambda: self.sel_add_to_queue(2,[self.sel_pushButton_4,self.sel_label_32,self.sel_label_16]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_4, 1, 0, 1, 1)
        self.sel_pushButton_5 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_5.setObjectName("pushButton_5")
        self.sel_pushButton_5.clicked.connect(lambda: self.sel_add_to_queue(3,[self.sel_pushButton_5,self.sel_label_22,self.sel_label_33]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_5, 2, 0, 1, 1)
        self.sel_pushButton_6 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_6.setObjectName("pushButton_6")
        self.sel_pushButton_6.clicked.connect(lambda: self.sel_add_to_queue(4,[self.sel_pushButton_6,self.sel_label_40,self.sel_label_23]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_6, 3, 0, 1, 1)
        self.sel_pushButton_7 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_7.setObjectName("pushButton_7")
        self.sel_pushButton_7.clicked.connect(lambda: self.sel_add_to_queue(5,[self.sel_pushButton_7,self.sel_label_31,self.sel_label_28]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_7, 4, 0, 1, 1)
        self.sel_pushButton_10 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_10.setObjectName("pushButton_10")
        self.sel_pushButton_10.clicked.connect(lambda: self.sel_add_to_queue(6,[self.sel_pushButton_10,self.sel_label_24,self.sel_label_19]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_10, 5, 0, 1, 1)
        self.sel_pushButton_11 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_11.setObjectName("pushButton_11")
        self.sel_pushButton_11.clicked.connect(lambda: self.sel_add_to_queue(7,[self.sel_pushButton_11,self.sel_label_20,self.sel_label_38]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_11, 6, 0, 1, 1)
        self.sel_pushButton_12 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_12.setObjectName("pushButton_12")
        self.sel_pushButton_12.clicked.connect(lambda: self.sel_add_to_queue(8,[self.sel_pushButton_12,self.sel_label_25,self.sel_label_37]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_12, 7, 0, 1, 1)
        self.sel_pushButton_13 = QtWidgets.QPushButton(self.sel_scrollAreaWidgetContents)
        self.sel_pushButton_13.setObjectName("pushButton_13")
        self.sel_pushButton_13.clicked.connect(lambda: self.sel_add_to_queue(9,[self.sel_pushButton_13,self.sel_label_41,self.sel_label_30]))

        self.sel_gridLayout.addWidget(self.sel_pushButton_13, 8, 0, 1, 1)
        self.sel_scrollArea.setWidget(self.sel_scrollAreaWidgetContents)

        self.sel_pushButton_16 = QtWidgets.QPushButton(self.form)
        self.sel_pushButton_16.setText("Show queue")
        self.sel_pushButton_16.clicked.connect(self.sel_show_queue)
        self.sel_pushButton_16.setGeometry(QtCore.QRect(410, 300, 100, 65))
        self.sel_pushButton_16.setObjectName("pushButton_16")
        
        self.sel_retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)

    def sel_retranslateUi(self):
        self.dat.__init__()
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle(_translate("self.form", "Mixology"))
        self.sel_pushButton_8.setText(_translate("self.form", "X"))
        self.sel_label_18.setText(_translate("self.form", "    SELECCIONAR"))
        self.sel_pushButton_9.setText(_translate("self.form", "X"))
        try:
            self.sel_label_36.setText(_translate("self.form", self.dat.df.Name[0]))
            self.sel_label_36.setVisible(True)
            self.sel_label_7.setText(_translate("self.form", self.dat.df.Ingredients[0]+","+self.dat.df.Boxes[0] if len(self.dat.df.Boxes[0])>1 else self.dat.df.Ingredients[0]))
            self.sel_label_7.setVisible(True)
            self.sel_pushButton_3.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_3.setVisible(True)
        except Exception as e:
            self.sel_label_36.setVisible(False)
            self.sel_label_7.setVisible(False)
            self.sel_pushButton_3.setVisible(False)
        try:
            self.sel_label_32.setText(_translate("self.form", self.dat.df.Name[1]))
            self.sel_label_32.setVisible(True)
            self.sel_label_16.setText(_translate("self.form", self.dat.df.Ingredients[1]+","+self.dat.df.Boxes[1] if len(self.dat.df.Boxes[1])>1 else self.dat.df.Ingredients[1]))
            self.sel_label_16.setVisible(True)
            self.sel_pushButton_4.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_4.setVisible(True)
        except Exception as e:
            self.sel_label_32.setVisible(False)
            self.sel_label_16.setVisible(False)
            self.sel_pushButton_4.setVisible(False)
        try:
            self.sel_label_22.setText(_translate("self.form", self.dat.df.Name[2]))
            self.sel_label_22.setVisible(True)
            self.sel_label_33.setText(_translate("self.form", self.dat.df.Ingredients[2]+","+self.dat.df.Boxes[2] if len(self.dat.df.Boxes[2])>1 else self.dat.df.Ingredients[2]))
            self.sel_label_33.setVisible(True)
            self.sel_pushButton_5.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_5.setVisible(True)
        except Exception as e:
            self.sel_label_22.setVisible(False)
            self.sel_label_33.setVisible(False)
            self.sel_pushButton_5.setVisible(False)
        try:
            self.sel_label_40.setText(_translate("self.form", self.dat.df.Name[3]))
            self.sel_label_40.setVisible(True)
            self.sel_label_23.setText(_translate("self.form", self.dat.df.Ingredients[3]+","+self.dat.df.Boxes[3] if len(self.dat.df.Boxes[3])>1 else self.dat.df.Ingredients[3]))
            self.sel_label_23.setVisible(True)
            self.sel_pushButton_6.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_6.setVisible(True)
        except Exception as e:
            self.sel_label_40.setVisible(False)
            self.sel_label_23.setVisible(False)
            self.sel_pushButton_6.setVisible(False)
        try:
            self.sel_label_31.setText(_translate("self.form", self.dat.df.Name[4]))
            self.sel_label_31.setVisible(True)
            self.sel_label_28.setText(_translate("self.form", self.dat.df.Ingredients[4]+","+self.dat.df.Boxes[4] if len(self.dat.df.Boxes[4])>1 else self.dat.df.Ingredients[4]))
            self.sel_label_28.setVisible(True)
            self.sel_pushButton_7.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_7.setVisible(True)
        except Exception as e:
            self.sel_label_31.setVisible(False)
            self.sel_label_28.setVisible(False)
            self.sel_pushButton_7.setVisible(False)
        try:
            self.sel_label_24.setText(_translate("self.form", self.dat.df.Name[5]))
            self.sel_label_24.setVisible(True)
            self.sel_label_19.setText(_translate("self.form", self.dat.df.Ingredients[5]+","+self.dat.df.Boxes[5] if len(self.dat.df.Boxes[5])>1 else self.dat.df.Ingredients[5]))
            self.sel_label_19.setVisible(True)
            self.sel_pushButton_10.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_10.setVisible(True)
        except Exception as e:
            self.sel_label_24.setVisible(False)
            self.sel_label_19.setVisible(False)
            self.sel_pushButton_10.setVisible(False)
        try:
            self.sel_label_20.setText(_translate("self.form", self.dat.df.Name[6]))
            self.sel_label_20.setVisible(True)
            self.sel_label_38.setText(_translate("self.form", self.dat.df.Ingredients[6]+","+self.dat.df.Boxes[6] if len(self.dat.df.Boxes[6])>1 else self.dat.df.Ingredients[6]))
            self.sel_label_38.setVisible(True)
            self.sel_pushButton_11.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_11.setVisible(True)
        except Exception as e:
            self.sel_label_20.setVisible(False)
            self.sel_label_38.setVisible(False)
            self.sel_pushButton_11.setVisible(False)
        try:
            self.sel_label_25.setText(_translate("self.form", self.dat.df.Name[7]))
            self.sel_label_25.setVisible(True)
            self.sel_label_37.setText(_translate("self.form", self.dat.df.Ingredients[7]+","+self.dat.df.Boxes[7] if len(self.dat.df.Boxes[7])>1 else self.dat.df.Ingredients[7]))
            self.sel_label_37.setVisible(True)
            self.sel_pushButton_12.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_12.setVisible(True)
        except Exception as e:
            self.sel_label_25.setVisible(False)
            self.sel_label_37.setVisible(False)
            self.sel_pushButton_12.setVisible(False)
        try:
            self.sel_label_41.setText(_translate("self.form", self.dat.df.Name[8]))
            self.sel_label_41.setVisible(True)
            self.sel_label_30.setText(_translate("self.form", self.dat.df.Ingredients[8]+","+self.dat.df.Boxes[8] if len(self.dat.df.Boxes[8])>1 else self.dat.df.Ingredients[8]))
            self.sel_label_30.setVisible(True)
            self.sel_pushButton_13.setText(_translate("self.form", "Eliminar"))
            self.sel_pushButton_13.setVisible(True)
        except Exception as e:
            self.sel_label_41.setVisible(False)
            self.sel_label_30.setVisible(False)
            self.sel_pushButton_13.setVisible(False)

    def sel_add_to_queue(self, id, functions):
        if self.trash:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("¿Estás seguro que quieres eliminar esta receta?")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Panel de confirmación")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msg.exec_()
            if (ret == QMessageBox.Yes):
                self.dat.clean_queue()
                self.dat.remove_recipe(id)
                [x.setVisible(False) for x in functions]
                self.dat.__init__()
                self.sel_retranslateUi()
        else:
            message, verification = self.dat.verify(id)
            if verification:
                self.dat.add_to_queue(id)
                self.dat.__init__()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("- "+str(("\n- ").join([self.dat.df.Name[list(self.dat.df.ID).index(x)] for x in self.dat.queue.values()])))
                # msg.setInformativeText('More information')
                msg.setWindowTitle("Cola Actual")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(message)
                # msg.setInformativeText('More information')
                msg.setWindowTitle("Completado")
                msg.exec_()
        self.usr_retranslateUi()
            
    def sel_show_queue(self):
        if bool(self.dat.queue):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("- "+str(("\n- ").join([self.dat.df.Name[list(self.dat.df.ID).index(x)] for x in self.dat.queue.values()])))
            msg.setInformativeText('\n\n\n¿Quieres eliminar la cola?')
            msg.setWindowTitle("Cola Actual")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msg.exec_()
            if (ret == QMessageBox.Yes):
                self.sel_clear_queue()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cola vacía")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Cola Actual")
            msg.exec_()

    def sel_clear_queue(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("¿Seguro que quieres borrar la cola?")
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Panel de confirmación")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        if (ret == QMessageBox.Yes):
            self.dat.clean_queue()
            self.dat.__init__()
        else:
            self.sel_show_queue()

    def sel_prepare(self):
        pause = False
        if bool(self.dat.queue):
            
            for i,j in enumerate(self.dat.queue.values(),1):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setText("¿Colocaste un vaso para servir?")
                # msg.setInformativeText('More information')
                msg.setWindowTitle("Ya casi comenzamos...")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                ret = msg.exec_()
                if (ret == QMessageBox.Yes):
                    message, verification = self.dat.verify(j)
                    self.dat.__init__()
                    if(verification):
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(message)
                        msg.setStyleSheet("background-color: #FFFFFF;")
                        # msg.setInformativeText('More information')
                        msg.setWindowTitle("En proceso...")
                        msg.show()
                        time.sleep(2)
                        self.prepare_drink(j-1)
                        msg.close()

                        self.dat.autocalibration(j)
                        self.dat.__init__()
                        
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("¡Tu bebida "+self.dat.df.Name[j-1]+" está lista!")
                        # msg.setInformativeText('More information')
                        msg.setWindowTitle("Completado")
                        msg.exec_()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText(message)
                        # msg.setInformativeText('More information')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        pause = True
                        self.dat.pause_queue(i)
                        break
                else:
                    pause = True
                    self.dat.pause_queue(i)
                    break
            if not pause:
                self.dat.clean_queue()
            self.dat.__init__()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Debes añadir la bebida a la cola\ncon el signo de \"+\"")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("No hay bebidas en cola")
            ret = msg.exec_()

    def prepare_drink(self,id):
        indexes, ingredients = list(self.dat.bottles.keys()),[w[0] for w in self.dat.bottles.values()]
        try:
            selected = [int(y) for y in [indexes[ingredients.index(x)] for x in self.dat.df.Ingredients[id].split(',')]]
        except:
            selected = indexes[ingredients.index(self.dat.df[id])]
        
        try:
            seconds = [int(x) for x in self.dat.df.Volume[id].split(',')]
        except:
            seconds = int(self.dat.df.Volume[id])
            
        
        calibration = [0.035 for _ in selected]
        self.ctr.pump_control(selected, seconds, calibration)
        if self.dat.df.Boxes[id] != " ":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            if ',' in str(self.dat.df.Boxes[id]):
                msg.setText("Añade a tu bebida:\n-"+'\n-'.join(self.dat.df.Boxes[id].split(',')))
            else:
                msg.setText("Añade a tu bebida:\n-"+str(self.dat.df.Boxes[id]))
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Añadidos sugeridos")
            ret = msg.exec_()
        
        if self.dat.df.Mix[id]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Coloca tu vaso en la mezcladora")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Mezcla tu bebida")
            ret = msg.exec_()
    #endregion select    
        
    #region user
    
    def user_form(self):
        self.form.setObjectName("self.form")
        self.form.resize(800, 380)
        self.form.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.form.setStyleSheet("background-color: rgb(236, 236, 236);\n"
        "")
        self.usr_label = QtWidgets.QLabel(self.form)
        self.usr_label.setGeometry(QtCore.QRect(0, 0, 800, 74))
        self.usr_label.setStyleSheet("font-family: Roboto;\n"
        "font-style: normal;\n"
        "font-weight: bold;\n"
        "font-size: 36px;\n"
        "line-height: 42px;\n"
        "\n"
        "color: #FFFFFF;\n"
        "background-color: #E09825;")
        self.usr_label.setObjectName("usr_label")
        self.usr_pushButton = QtWidgets.QPushButton(self.form)
        self.usr_pushButton.setGeometry(QtCore.QRect(735, 10, 50, 50))
        self.usr_pushButton.setObjectName("usr_pushButton")
        self.usr_pushButton.setIcon(QIcon('assets/settings.png'))
        self.usr_pushButton.setIconSize(QtCore.QSize(40, 40))
        self.usr_pushButton.clicked.connect(lambda: self.getpassword())
        self.usr_pushButton_2 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_2.setGeometry(QtCore.QRect(650, 310-20, 65, 65))
        self.usr_pushButton_2.setObjectName("usr_pushButton_2")
        self.usr_pushButton_2.setIcon(QIcon('assets/add.png'))
        self.usr_pushButton_2.setIconSize(QtCore.QSize(50, 50))
        self.usr_pushButton_2.clicked.connect(lambda: self.sel_add_to_queue(self.user_screen,[self.usr_pushButton_16,self.usr_pushButton_16]))
        
        self.usr_pushButton_18 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_18.setGeometry(QtCore.QRect(80, 310-20, 65, 65))
        self.usr_pushButton_18.setObjectName("usr_pushButton_2")
        self.usr_pushButton_18.setIcon(QIcon('assets/undo.png'))
        self.usr_pushButton_18.setIconSize(QtCore.QSize(50, 50))
        self.usr_pushButton_18.clicked.connect(lambda: self.usr_undo())
        
        self.usr_horizontalLayoutWidget = QtWidgets.QWidget(self.form)
        self.usr_horizontalLayoutWidget.setGeometry(QtCore.QRect(150, 340-20, 500, 50))
        self.usr_horizontalLayoutWidget.setObjectName("usr_horizontalLayoutWidget")
        self.usr_horizontalLayout = QtWidgets.QHBoxLayout(self.usr_horizontalLayoutWidget)
        self.usr_horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.usr_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.usr_horizontalLayout.setSpacing(15)
        self.usr_horizontalLayout.setObjectName("usr_horizontalLayout")
        
        #region button menu
        self.usr_pushButton_6 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_6.setObjectName("usr_pushButton_6")
        self.usr_pushButton_6.clicked.connect(lambda: self.usr_change_recipe(1))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_6)
        self.usr_pushButton_7 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_7.setObjectName("usr_pushButton_7")
        self.usr_pushButton_7.clicked.connect(lambda: self.usr_change_recipe(2))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_7)
        self.usr_pushButton_8 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_8.setObjectName("usr_pushButton_8")
        self.usr_pushButton_8.clicked.connect(lambda: self.usr_change_recipe(3))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_8)
        self.usr_pushButton_9 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_9.setObjectName("usr_pushButton_9")
        self.usr_pushButton_9.clicked.connect(lambda: self.usr_change_recipe(4))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_9)
        self.usr_pushButton_10 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_10.setObjectName("usr_pushButton_10")
        self.usr_pushButton_10.clicked.connect(lambda: self.usr_change_recipe(5))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_10)
        self.usr_pushButton_11 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_11.setObjectName("usr_pushButton_11")
        self.usr_pushButton_11.clicked.connect(lambda: self.usr_change_recipe(6))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_11)
        self.usr_pushButton_12 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_12.setObjectName("usr_pushButton_12")
        self.usr_pushButton_12.clicked.connect(lambda: self.usr_change_recipe(7))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_12)
        self.usr_pushButton_13 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_13.setObjectName("usr_pushButton_13")
        self.usr_pushButton_13.clicked.connect(lambda: self.usr_change_recipe(8))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_13)
        self.usr_pushButton_14 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_14.setObjectName("usr_pushButton_14")
        self.usr_pushButton_14.clicked.connect(lambda: self.usr_change_recipe(9))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_14)
        self.usr_pushButton_15 = QtWidgets.QPushButton(self.usr_horizontalLayoutWidget)
        self.usr_pushButton_15.setObjectName("usr_pushButton_15")
        self.usr_pushButton_15.clicked.connect(lambda: self.usr_change_recipe(10))
        self.usr_horizontalLayout.addWidget(self.usr_pushButton_15)
        #endregion button menu
        
        self.usr_label_2 = QtWidgets.QLabel(self.form)
        self.usr_label_2.setGeometry(QtCore.QRect(10, 110-10, 150, 30))
        self.usr_label_2.setObjectName("usr_label_2")
        self.usr_label_2.setStyleSheet("border-top-left-radius: 5px;"
                                   "border-top-right-radius: 20px;"
                                   "border: 1px solid black;")

        self.usr_label_3 = QtWidgets.QLabel(self.form)
        self.usr_label_3.setGeometry(QtCore.QRect(10, 140-10, 150, 130))
        self.usr_label_3.setObjectName("usr_label_3")
        self.usr_label_3.setStyleSheet("border-bottom-left-radius: 20px;"
                                   "border-bottom-right-radius: 5px;"
                                   "border: 1px solid black;")

        self.usr_label_4 = QtWidgets.QLabel(self.form)
        self.usr_label_4.setGeometry(QtCore.QRect(641, 110-10, 150, 30))
        self.usr_label_4.setObjectName("usr_label_4")
        self.usr_label_4.setStyleSheet("border-top-left-radius: 5px;"
                                   "border-top-right-radius: 20px;"
                                   "border: 1px solid black;")

        self.usr_label_5 = QtWidgets.QLabel(self.form)
        self.usr_label_5.setGeometry(QtCore.QRect(641, 140-10, 150, 130))
        self.usr_label_5.setObjectName("usr_label_5")
        self.usr_label_5.setStyleSheet("border-bottom-left-radius: 20px;"
                                   "border-bottom-right-radius: 5px;"
                                   "border: 1px solid black;")

        self.usr_pushButton_3 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_3.setGeometry(QtCore.QRect(720, 310-20, 65, 65))
        self.usr_pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "border-radius:30px\n"
        "")
        self.usr_pushButton_3.setText("")
        self.usr_pushButton_3.setObjectName("crt_pushButton_2")
        self.usr_pushButton_3.setIcon(QIcon('assets/play.png'))
        self.usr_pushButton_3.setIconSize(QtCore.QSize(50, 50))
        self.usr_pushButton_3.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.usr_pushButton_3.clicked.connect(self.sel_prepare)
        
        self.usr_pushButton_17 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_17.setGeometry(QtCore.QRect(10, 310-20, 65, 65))
        self.usr_pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "border-radius:30px\n"
        "")
        self.usr_pushButton_17.setText("")
        self.usr_pushButton_17.setObjectName("crt_pushButton_2")
        self.usr_pushButton_17.setIcon(QIcon('assets/checklist.png'))
        self.usr_pushButton_17.setIconSize(QtCore.QSize(50, 50))
        self.usr_pushButton_17.setStyleSheet("border-radius:30px\noverflow:hidden;")
        self.usr_pushButton_17.clicked.connect(self.sel_show_queue)
        
        self.usr_pushButton_4 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_4.setGeometry(QtCore.QRect(165, 90-10, 30, 230))
        self.usr_pushButton_4.setObjectName("usr_pushButton_4")
        self.usr_pushButton_4.setStyleSheet(self.buttonNavStyle())
        self.usr_pushButton_4.clicked.connect(lambda: self.usr_change_recipe("-"))
        
        self.usr_pushButton_5 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_5.setGeometry(QtCore.QRect(605, 90-10, 30, 230))
        self.usr_pushButton_5.setObjectName("usr_pushButton_5")
        self.usr_pushButton_5.setStyleSheet(self.buttonNavStyle())
        self.usr_pushButton_5.clicked.connect(lambda: self.usr_change_recipe("+"))
        
        
        self.usr_label_6 = QtWidgets.QLabel(self.form)
        self.usr_label_6.setGeometry(QtCore.QRect(195, 290-10, 205, 30))
        self.usr_label_6.setStyleSheet("background-color: rgba(0,0,0,0.5);"
                                   "color: #fff;"
                                   "padding-left: 15px;"
                                   "border-top-right-radius: 20px;")
        self.usr_label_6.setObjectName("usr_label_6")
        
        self.usr_label_7 = QtWidgets.QLabel(self.form)
        self.usr_label_7.setGeometry(QtCore.QRect(0, 360, 800, 20))
        self.usr_label_7.setStyleSheet("background-color: black;"
                                   "color: #fff;"
                                   "padding-left: 15px;"
                                   "font-size: 14px;")
        self.usr_label_7.setObjectName("usr_label_7")
        self.usr_label_7.setText("Para añadir la bebida a la cola presione el signo de \"+\"")
        
        
        
        self.usr_pushButton_16 = QtWidgets.QPushButton(self.form)
        self.usr_pushButton_16.setGeometry(QtCore.QRect(195, 90-10, 410, 230))
        self.usr_pushButton_16.setObjectName("usr_pushButton_16")
        self.usr_pushButton_16.raise_()
        self.usr_label.raise_()
        self.usr_pushButton.raise_()
        self.usr_pushButton_2.raise_()
        self.usr_horizontalLayoutWidget.raise_()
        self.usr_label_2.raise_()
        self.usr_label_3.raise_()
        self.usr_label_4.raise_()
        self.usr_label_5.raise_()
        self.usr_pushButton_3.raise_()
        self.usr_pushButton_4.raise_()
        self.usr_pushButton_5.raise_()
        self.usr_label_6.raise_()

        self.usr_retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)


    def usr_undo(self):
        self.dat.queue.popitem()
        jsonFile = open("data/queue.json", "w")
        jsonFile.write(json.dumps(self.dat.queue, indent=4, sort_keys=True))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Se ha removido el último elemento de la cola")
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Cola actualizada")
        msg.exec_()
        self.usr_retranslateUi()

    
    def usr_retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.form.setWindowTitle(_translate("self.form", "Mixology"))
        self.usr_label.setText(_translate("self.form", "    MIXOLOGY"))
        self.usr_pushButton_6.setText(_translate("self.form", "1"))
        self.usr_pushButton_6.setVisible(len(self.dat.df.ID)>0)
        self.usr_pushButton_7.setText(_translate("self.form", "2"))
        self.usr_pushButton_7.setVisible(len(self.dat.df.ID)>1)
        self.usr_pushButton_8.setText(_translate("self.form", "3"))
        self.usr_pushButton_8.setVisible(len(self.dat.df.ID)>2)
        self.usr_pushButton_9.setText(_translate("self.form", "4"))
        self.usr_pushButton_9.setVisible(len(self.dat.df.ID)>3)
        self.usr_pushButton_10.setText(_translate("self.form", "5"))
        self.usr_pushButton_10.setVisible(len(self.dat.df.ID)>4)
        self.usr_pushButton_11.setText(_translate("self.form", "6"))
        self.usr_pushButton_11.setVisible(len(self.dat.df.ID)>5)
        self.usr_pushButton_12.setText(_translate("self.form", "7"))
        self.usr_pushButton_12.setVisible(len(self.dat.df.ID)>6)
        self.usr_pushButton_13.setText(_translate("self.form", "8"))
        self.usr_pushButton_13.setVisible(len(self.dat.df.ID)>7)
        self.usr_pushButton_14.setText(_translate("self.form", "9"))
        self.usr_pushButton_14.setVisible(len(self.dat.df.ID)>8)
        self.usr_pushButton_15.setText(_translate("self.form", "10"))
        self.usr_pushButton_15.setVisible(len(self.dat.df.ID)>9)
        self.usr_label_2.setText(_translate("self.form", "Líquidos"))
        self.usr_label_3.setText("-"+"\n-".join(self.dat.df.Ingredients[self.user_screen-1].split(',')))
        self.usr_label_4.setText(_translate("self.form", "Sólidos"))
        self.usr_label_5.setText("-"+"\n-".join(self.dat.df.Boxes[self.user_screen-1].split(',')))
        self.usr_pushButton_4.setText("<" if self.user_screen>1 else "")
        self.usr_pushButton_4.setEnabled(self.user_screen>1)
        self.usr_pushButton_5.setText(">" if self.user_screen<len(self.dat.df.ID) else "")
        self.usr_pushButton_5.setEnabled(self.user_screen<len(self.dat.df.ID))
        self.usr_label_6.setText(self.dat.df.Name[self.user_screen-1])
        
        self.usr_pushButton_6.setStyleSheet(self.buttonStyle(self.user_screen == 1))
        self.usr_pushButton_7.setStyleSheet(self.buttonStyle(self.user_screen == 2))
        self.usr_pushButton_8.setStyleSheet(self.buttonStyle(self.user_screen == 3))
        self.usr_pushButton_9.setStyleSheet(self.buttonStyle(self.user_screen == 4))
        self.usr_pushButton_10.setStyleSheet(self.buttonStyle(self.user_screen == 5))
        self.usr_pushButton_11.setStyleSheet(self.buttonStyle(self.user_screen == 6))
        self.usr_pushButton_12.setStyleSheet(self.buttonStyle(self.user_screen == 7))
        self.usr_pushButton_13.setStyleSheet(self.buttonStyle(self.user_screen == 8))
        self.usr_pushButton_14.setStyleSheet(self.buttonStyle(self.user_screen == 9))
        self.usr_pushButton_15.setStyleSheet(self.buttonStyle(self.user_screen == 10))

        
        if self.dat.df.Name[self.user_screen-1]+'.jpg' in [x.replace("images/","") for x in glob("images/*")]:
            self.usr_pushButton_16.setIcon(QIcon('images/'+self.dat.df.Name[self.user_screen-1]+'.jpg'))
        else:
            self.usr_pushButton_16.setIcon(QIcon('images/Logo.jpg'))
        self.usr_pushButton_16.setIconSize(QtCore.QSize(410, 230))
        self.usr_pushButton_16.setStyleSheet(self.ButtonImageStyle())
        self.usr_pushButton_18.setVisible(bool(self.dat.queue))
        

    def usr_change_recipe(self, sign):
        if sign == "+":
            self.user_screen +=1
        elif sign == "-":
            self.user_screen -=1
        else:
            self.user_screen = sign
        self.usr_retranslateUi()
            
    def getpassword(self):
        f = open('.pass.bin', 'rb')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Seguro que quieres entrar al modo administrador?")
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Panel de confirmación")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        if ret == QMessageBox.Yes:
            s = ""
            text, ok = QInputDialog.getText(None, "Admin", "Contraseña", QLineEdit.Password)
            if ok and text:
                for line in f:
                    s = line.decode()
                if s == text:
                    self.state_machine(0)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Contraseña incorrecta")
                    # msg.setInformativeText('More information')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                f.close()
    #endregion user
    
    def state_machine(self,state):
        self.dat.__init__()
        self.state = state
        self.trash = self.state == 3
        if self.state == 0 and self.init[0] == 0:
            self.main()
            self.init[0] = 1
        
        if self.state == 1 and self.init[1] == 0:
            self.create_form()
            self.init[1] = 1
        elif self.state == 1:
            self.crt_retranslateUi()
        
        if self.state == 2 and self.init[2] == 0:
            self.calibrate_form()
            self.init[2] = 1
        elif self.state == 2:
            self.cal_retranslateUi()
        
        if self.state == 3 and self.init[3] == 0:
            self.select_form()
            self.init[3] = 1
        elif self.state == 3:
            self.sel_retranslateUi()
        
        if self.state == 4 and self.init[3] == 0:
            self.user_form()
            self.init[4] = 1
        elif self.state == 4:
            self.usr_retranslateUi()

        #region visible
        #region main
        try:
            self.pushButton.setVisible(self.state == 0)
            self.pushButton_3 .setVisible(self.state == 0)
            self.pushButton_4 .setVisible(self.state == 0)
            self.pushButton_5.setVisible(self.state == 0)
            self.pushButton_6.setVisible(self.state == 0)
            self.label.setVisible(self.state == 0)
        except:
            pass
        #endregion main
        #region create
        try:
            self.crt_label_2.setVisible(self.state == 1)
            self.crt_pushButton_7.setVisible(self.state == 1)
            self.crt_label_12.setVisible(self.state == 1)
            self.crt_pushButton.setVisible(self.state == 1)
            self.crt_pushButton_2.setVisible(self.state == 1)
            self.crt_lineEdit.setVisible(self.state == 1)
            self.crt_textEdit.setVisible(self.state == 1)
            self.crt_horizontalSlider_11.setVisible(self.state == 1)
            self.crt_scrollArea.setVisible(self.state == 1)
            self.crt_scrollAreaWidgetContents.setVisible(self.state == 1)
            self.crt_label.setVisible(self.state == 1)
            self.crt_horizontalSlider.setVisible(self.state == 1)
            self.crt_label_3.setVisible(self.state == 1)
            self.crt_horizontalSlider_2.setVisible(self.state == 1)
            self.crt_label_4.setVisible(self.state == 1)
            self.crt_horizontalSlider_3.setVisible(self.state == 1)
            self.crt_label_6.setVisible(self.state == 1)
            self.crt_horizontalSlider_4.setVisible(self.state == 1)
            self.crt_label_7.setVisible(self.state == 1)
            self.crt_horizontalSlider_5.setVisible(self.state == 1)
            self.crt_label_8.setVisible(self.state == 1)
            self.crt_horizontalSlider_6.setVisible(self.state == 1)
            self.crt_label_9.setVisible(self.state == 1)
            self.crt_horizontalSlider_7.setVisible(self.state == 1)
            self.crt_label_11.setVisible(self.state == 1)
            self.crt_label_13.setVisible(self.state == 1)
            self.crt_horizontalSlider_8.setVisible(self.state == 1)
            self.crt_label_10.setVisible(self.state == 1)
            self.crt_label_5.setVisible(self.state == 1)
            self.crt_horizontalSlider_9.setVisible(self.state == 1)
            self.crt_horizontalSlider_10.setVisible(self.state == 1)
            self.crt_scrollArea_2.setVisible(self.state == 1)
            self.crt_scrollAreaWidgetContents_2.setVisible(self.state == 1)
            self.crt_verticalLayout.setVisible(self.state == 1)
            self.crt_checkBox.setVisible(self.state == 1)
            self.crt_checkBox_2.setVisible(self.state == 1)
            self.crt_checkBox_3.setVisible(self.state == 1)
            self.crt_checkBox_4.setVisible(self.state == 1)
            self.crt_checkBox_5.setVisible(self.state == 1)
            self.crt_checkBox_6.setVisible(self.state == 1)
        except:
            pass
        #endregion create
        #region calibrate
        try:
            self.cal_pushButton_7.setVisible(self.state == 2)
            self.cal_label_2.setVisible(self.state == 2)
            self.cal_pushButton_10.setVisible(self.state == 2)
            self.cal_pushButton_11.setVisible(self.state == 2)
            self.cal_scrollArea.setVisible(self.state == 2)
            self.cal_scrollAreaWidgetContents.setVisible(self.state == 2)
            self.cal_lineEdit_12.setVisible(self.state == 2)
            self.cal_lineEdit_15.setVisible(self.state == 2)
            self.cal_horizontalSlider.setVisible(self.state == 2)
            self.cal_lineEdit_10.setVisible(self.state == 2)
            self.cal_horizontalSlider_2.setVisible(self.state == 2)
            self.cal_horizontalSlider_3.setVisible(self.state == 2)
            self.cal_horizontalSlider_4.setVisible(self.state == 2)
            self.cal_label_22.setVisible(self.state == 2)
            self.cal_horizontalSlider_5.setVisible(self.state == 2)
            self.cal_lineEdit_13.setVisible(self.state == 2)
            self.cal_label_26.setVisible(self.state == 2)
            self.cal_horizontalSlider_6.setVisible(self.state == 2)
            self.cal_label_18.setVisible(self.state == 2)
            self.cal_lineEdit_11.setVisible(self.state == 2)
            self.cal_label_19.setVisible(self.state == 2)
            self.cal_lineEdit_14.setVisible(self.state == 2)
            self.cal_horizontalSlider_7.setVisible(self.state == 2)
            self.cal_horizontalSlider_8.setVisible(self.state == 2)
            self.cal_horizontalSlider_9.setVisible(self.state == 2)
            self.cal_label_21.setVisible(self.state == 2)
            self.cal_lineEdit_9.setVisible(self.state == 2)
            self.cal_label_20.setVisible(self.state == 2)
            self.cal_label_24.setVisible(self.state == 2)
            self.cal_lineEdit_7.setVisible(self.state == 2)
            self.cal_label_23.setVisible(self.state == 2)
            self.cal_lineEdit_8.setVisible(self.state == 2)
            self.cal_label_25.setVisible(self.state == 2)
            self.cal_lineEdit_16.setVisible(self.state == 2)
            self.cal_horizontalSlider_10.setVisible(self.state == 2)
            self.cal_label_27.setVisible(self.state == 2)
            self.cal_scrollArea_2.setVisible(self.state == 2)
            self.cal_scrollAreaWidgetContents_2.setVisible(self.state == 2)
            self.cal_verticalLayout.setVisible(self.state == 2)
            self.cal_label_12.setVisible(self.state == 2)
            self.cal_lineEdit.setVisible(self.state == 2)
            self.cal_label_13.setVisible(self.state == 2)
            self.cal_lineEdit_2.setVisible(self.state == 2)
            self.cal_label_14.setVisible(self.state == 2)
            self.cal_lineEdit_3.setVisible(self.state == 2)
            self.cal_label_15.setVisible(self.state == 2)
            self.cal_lineEdit_4.setVisible(self.state == 2)
            self.cal_label_16.setVisible(self.state == 2)
            self.cal_lineEdit_5.setVisible(self.state == 2)
            self.cal_label_17.setVisible(self.state == 2)
            self.cal_lineEdit_6.setVisible(self.state == 2)
        except:
            pass
        #endregion calibrate
        #region select
        try:
            self.sel_pushButton_8.setVisible(self.state == 3)
            self.sel_label_18.setVisible(self.state == 3)
            self.sel_pushButton_9.setVisible(self.state == 3)
            self.sel_pushButton.setVisible(self.state == 3)
            self.sel_scrollArea.setVisible(self.state == 3)
            self.sel_scrollAreaWidgetContents.setVisible(self.state == 3)
            
            self.sel_label_36.setVisible(self.state == 3 and len(self.dat.df.ID)>0)
            self.sel_label_7.setVisible(self.state == 3) and len(self.dat.df.ID)>0
            self.sel_pushButton_3.setVisible(self.state == 3 and len(self.dat.df.ID)>0)
            
            self.sel_label_32.setVisible(self.state == 3 and len(self.dat.df.ID)>1)
            self.sel_label_16.setVisible(self.state == 3 and len(self.dat.df.ID)>1)
            self.sel_pushButton_4.setVisible(self.state == 3 and len(self.dat.df.ID)>1)
            
            self.sel_label_33.setVisible(self.state == 3 and len(self.dat.df.ID)>2)
            self.sel_label_22.setVisible(self.state == 3 and len(self.dat.df.ID)>2)
            self.sel_pushButton_5.setVisible(self.state == 3 and len(self.dat.df.ID)>2)
            
            self.sel_label_23.setVisible(self.state == 3 and len(self.dat.df.ID)>3)
            self.sel_label_40.setVisible(self.state == 3 and len(self.dat.df.ID)>3)
            self.sel_pushButton_6.setVisible(self.state == 3 and len(self.dat.df.ID)>3)
            
            self.sel_label_31.setVisible(self.state == 3 and len(self.dat.df.ID)>4)
            self.sel_label_28.setVisible(self.state == 3 and len(self.dat.df.ID)>4)
            self.sel_pushButton_7.setVisible(self.state == 3 and len(self.dat.df.ID)>4)
            
            self.sel_label_24.setVisible(self.state == 3 and len(self.dat.df.ID)>5)
            self.sel_label_19.setVisible(self.state == 3 and len(self.dat.df.ID)>5)
            self.sel_pushButton_10.setVisible(self.state == 3 and len(self.dat.df.ID)>5)
            
            self.sel_label_38.setVisible(self.state == 3 and len(self.dat.df.ID)>6)
            self.sel_label_37.setVisible(self.state == 3 and len(self.dat.df.ID)>6)
            self.sel_pushButton_11.setVisible(self.state == 3 and len(self.dat.df.ID)>6)
            
            self.sel_label_20.setVisible(self.state == 3 and len(self.dat.df.ID)>7)
            self.sel_label_30.setVisible(self.state == 3 and len(self.dat.df.ID)>7)
            self.sel_pushButton_12.setVisible(self.state == 3 and len(self.dat.df.ID)>7)
            
            self.sel_label_25.setVisible(self.state == 3 and len(self.dat.df.ID)>8)
            self.sel_label_41.setVisible(self.state == 3 and len(self.dat.df.ID)>8)
            self.sel_pushButton_13.setVisible(self.state == 3 and len(self.dat.df.ID)>8)
            
            self.sel_pushButton_2.setVisible(self.state == 3)
            self.sel_pushButton_14.setVisible(self.state == 3)
            self.sel_pushButton_15.setVisible(self.state == 3)
            self.sel_pushButton_16.setVisible(self.state == 3)
        except:
            pass
        #endregion select
        #region user
        try:
            self.usr_label.setVisible(self.state == 4)
            self.usr_pushButton.setVisible(self.state == 4)
            self.usr_pushButton_2.setVisible(self.state == 4)
            self.usr_horizontalLayoutWidget.setVisible(self.state == 4)
            self.usr_pushButton_6.setVisible(self.state == 4 and len(self.dat.df.ID)>0)
            self.usr_pushButton_7.setVisible(self.state == 4 and len(self.dat.df.ID)>1)
            self.usr_pushButton_8.setVisible(self.state == 4 and len(self.dat.df.ID)>2)
            self.usr_pushButton_9.setVisible(self.state == 4 and len(self.dat.df.ID)>3)
            self.usr_pushButton_10.setVisible(self.state == 4 and len(self.dat.df.ID)>4)
            self.usr_pushButton_11.setVisible(self.state == 4 and len(self.dat.df.ID)>5)
            self.usr_pushButton_12.setVisible(self.state == 4 and len(self.dat.df.ID)>6)
            self.usr_pushButton_13.setVisible(self.state == 4 and len(self.dat.df.ID)>7)
            self.usr_pushButton_14.setVisible(self.state == 4 and len(self.dat.df.ID)>8)
            self.usr_pushButton_15.setVisible(self.state == 4 and len(self.dat.df.ID)>9)
            self.usr_label_2.setVisible(self.state == 4)
            self.usr_label_3.setVisible(self.state == 4)
            self.usr_label_4.setVisible(self.state == 4)
            self.usr_label_5.setVisible(self.state == 4)
            self.usr_pushButton_3.setVisible(self.state == 4)
            self.usr_pushButton_4.setVisible(self.state == 4)
            self.usr_pushButton_5.setVisible(self.state == 4)
            self.usr_label_6.setVisible(self.state == 4)
            self.usr_pushButton_16.setVisible(self.state == 4)
            self.usr_pushButton_17.setVisible(self.state == 4)
            self.usr_label_7.setVisible(self.state == 4)
            self.usr_pushButton_18.setVisible(self.state == 4 and bool(self.dat.queue))
        except:
            pass
        #endregion user
        #endregion visible

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form(Form)
    Form.show()
    sys.exit(app.exec_())