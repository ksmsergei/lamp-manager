# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uncompiled/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(277, 149)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/manage_lamp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lblStatus = QtWidgets.QLabel(self.centralwidget)
        self.lblStatus.setGeometry(QtCore.QRect(5, 5, 267, 41))
        self.lblStatus.setText("<table width=\"100%\">\n"
"<tr>\n"
"<td align=\"left\">Status of <b>apache2</b>: </td>\n"
"<td align=\"right\"><span style=\"color: red;\">inactive</span></td>\n"
"</tr>\n"
"<tr>\n"
"<td align=\"left\">Status of <b>mysql</b>: </td>\n"
"<td align=\"right\"><span style=\"color: red;\">inactive</span></td>\n"
"</tr>\n"
"</table>")
        self.lblStatus.setObjectName("lblStatus")
        self.btnStartStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartStop.setGeometry(QtCore.QRect(5, 56, 267, 27))
        self.btnStartStop.setText("Start services")
        self.btnStartStop.setObjectName("btnStartStop")
        self.btnRestart = QtWidgets.QPushButton(self.centralwidget)
        self.btnRestart.setEnabled(False)
        self.btnRestart.setGeometry(QtCore.QRect(5, 93, 267, 27))
        self.btnRestart.setText("Restart services")
        self.btnRestart.setObjectName("btnRestart")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 277, 24))
        self.menuBar.setObjectName("menuBar")
        self.menuOptions = QtWidgets.QMenu(self.menuBar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuLanguage = QtWidgets.QMenu(self.menuOptions)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menuBar)
        self.aToTray = QtWidgets.QAction(MainWindow)
        self.aToTray.setCheckable(True)
        self.aToTray.setChecked(True)
        self.aToTray.setObjectName("aToTray")
        self.langEn = QtWidgets.QAction(MainWindow)
        self.langEn.setText("en")
        self.langEn.setIconText("en")
        self.langEn.setToolTip("en")
        self.langEn.setStatusTip("")
        self.langEn.setWhatsThis("")
        self.langEn.setShortcut("")
        self.langEn.setObjectName("langEn")
        self.menuLanguage.addAction(self.langEn)
        self.menuOptions.addAction(self.aToTray)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LAMP Manager"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.aToTray.setText(_translate("MainWindow", "Minimize to tray"))
        self.aToTray.setToolTip(_translate("MainWindow", "Minimize to tray"))
import resources_rc