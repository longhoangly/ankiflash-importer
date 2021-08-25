# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/long.hoangly/Library/Application Support/Anki2/addons21/1129289384/Ui/UiImporter.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# Modified
# 0. Change object name: UiImporter
# 1. Added version, iconPath params for setupUi method
# Dialog.setWindowTitle("Importer {}".format(version))
# icon = QtGui.QIcon(iconPath)
# Dialog.setWindowIcon(icon)
# 3. Set fixed window size
# Dialog.setFixedSize(424, 100)

from PyQt5 import QtCore, QtGui, QtWidgets


class UiImporter(object):
    def setupUi(self, Dialog, version, iconPath):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(424, 100)
        Dialog.setWindowTitle("Importer {}".format(version))
        icon = QtGui.QIcon(iconPath)
        Dialog.setWindowIcon(icon)
        self.deckNameTxt = QtWidgets.QLineEdit(Dialog)
        self.deckNameTxt.setGeometry(QtCore.QRect(100, 10, 301, 31))
        self.deckNameTxt.setObjectName("deckNameTxt")
        self.importProgressBar = QtWidgets.QProgressBar(Dialog)
        self.importProgressBar.setGeometry(QtCore.QRect(100, 50, 301, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.importProgressBar.setFont(font)
        self.importProgressBar.setProperty("value", 0)
        self.importProgressBar.setObjectName("importProgressBar")
        self.deckNameLbl = QtWidgets.QLabel(Dialog)
        self.deckNameLbl.setGeometry(QtCore.QRect(20, 18, 81, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.deckNameLbl.setFont(font)
        self.deckNameLbl.setObjectName("deckNameLbl")
        self.importBtn = QtWidgets.QPushButton(Dialog)
        self.importBtn.setEnabled(False)
        self.importBtn.setGeometry(QtCore.QRect(20, 50, 75, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.importBtn.setFont(font)
        self.importBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.importBtn.setAutoFillBackground(False)
        self.importBtn.setCheckable(False)
        self.importBtn.setDefault(False)
        self.importBtn.setObjectName("importBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.deckNameTxt.setPlaceholderText(_translate("Dialog", " Input deck name"))
        self.deckNameLbl.setText(_translate("Dialog", "Deck Name"))
        self.importBtn.setToolTip(_translate("Dialog", "Import generated flashcards into Anki"))
        self.importBtn.setText(_translate("Dialog", "Import"))
