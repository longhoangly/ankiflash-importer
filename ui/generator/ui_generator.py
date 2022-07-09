# Form implementation generated from reading ui file '/ankiflash-importer/ui/ui_generator.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class UiGenerator(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(682, 623)
        Dialog.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("../../resources/anki.ico"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(True)
        self.inputBox = QtWidgets.QGroupBox(Dialog)
        self.inputBox.setGeometry(QtCore.QRect(10, 10, 421, 451))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.inputBox.setFont(font)
        self.inputBox.setObjectName("inputBox")
        self.inputTxt = QtWidgets.QPlainTextEdit(self.inputBox)
        self.inputTxt.setGeometry(QtCore.QRect(20, 40, 381, 151))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.inputTxt.setFont(font)
        self.inputTxt.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.inputTxt.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.inputTxt.setObjectName("inputTxt")
        self.generateBtn = QtWidgets.QPushButton(self.inputBox)
        self.generateBtn.setGeometry(QtCore.QRect(20, 400, 91, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.generateBtn.setFont(font)
        self.generateBtn.setDefault(False)
        self.generateBtn.setObjectName("generateBtn")
        self.totalLbl = QtWidgets.QLabel(self.inputBox)
        self.totalLbl.setGeometry(QtCore.QRect(20, 200, 200, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.totalLbl.setFont(font)
        self.totalLbl.setObjectName("totalLbl")
        self.sourceBox = QtWidgets.QGroupBox(self.inputBox)
        self.sourceBox.setGeometry(QtCore.QRect(20, 234, 121, 111))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.sourceBox.setFont(font)
        self.sourceBox.setFlat(False)
        self.sourceBox.setCheckable(False)
        self.sourceBox.setObjectName("sourceBox")
        self.source3 = QtWidgets.QRadioButton(self.sourceBox)
        self.source3.setGeometry(QtCore.QRect(10, 66, 101, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.source3.setFont(font)
        self.source3.setObjectName("source3")
        self.source4 = QtWidgets.QRadioButton(self.sourceBox)
        self.source4.setGeometry(QtCore.QRect(10, 84, 101, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.source4.setFont(font)
        self.source4.setObjectName("source4")
        self.source2 = QtWidgets.QRadioButton(self.sourceBox)
        self.source2.setGeometry(QtCore.QRect(10, 48, 101, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.source2.setFont(font)
        self.source2.setObjectName("source2")
        self.source1 = QtWidgets.QRadioButton(self.sourceBox)
        self.source1.setGeometry(QtCore.QRect(10, 30, 101, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.source1.setFont(font)
        self.source1.setChecked(True)
        self.source1.setObjectName("source1")
        self.translatedToBox = QtWidgets.QGroupBox(self.inputBox)
        self.translatedToBox.setGeometry(QtCore.QRect(230, 234, 171, 151))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.translatedToBox.setFont(font)
        self.translatedToBox.setObjectName("translatedToBox")
        self.target6 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target6.setGeometry(QtCore.QRect(10, 127, 151, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target6.setFont(font)
        self.target6.setObjectName("target6")
        self.target2 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target2.setGeometry(QtCore.QRect(10, 49, 141, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target2.setFont(font)
        self.target2.setObjectName("target2")
        self.target1 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target1.setGeometry(QtCore.QRect(10, 30, 141, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target1.setFont(font)
        self.target1.setChecked(True)
        self.target1.setObjectName("target1")
        self.target4 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target4.setGeometry(QtCore.QRect(10, 88, 141, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target4.setFont(font)
        self.target4.setObjectName("target4")
        self.target5 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target5.setGeometry(QtCore.QRect(10, 107, 151, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target5.setFont(font)
        self.target5.setObjectName("target5")
        self.target3 = QtWidgets.QRadioButton(self.translatedToBox)
        self.target3.setGeometry(QtCore.QRect(10, 69, 141, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target3.setFont(font)
        self.target3.setObjectName("target3")
        self.generateProgressBar = QtWidgets.QProgressBar(self.inputBox)
        self.generateProgressBar.setGeometry(QtCore.QRect(120, 400, 201, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.generateProgressBar.setFont(font)
        self.generateProgressBar.setToolTip("")
        self.generateProgressBar.setProperty("value", 0)
        self.generateProgressBar.setObjectName("generateProgressBar")
        self.allWordTypes = QtWidgets.QCheckBox(self.inputBox)
        self.allWordTypes.setGeometry(QtCore.QRect(20, 350, 121, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.allWordTypes.setFont(font)
        self.allWordTypes.setChecked(True)
        self.allWordTypes.setObjectName("allWordTypes")
        self.isOnline = QtWidgets.QCheckBox(self.inputBox)
        self.isOnline.setGeometry(QtCore.QRect(20, 370, 121, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.isOnline.setFont(font)
        self.isOnline.setChecked(True)
        self.isOnline.setObjectName("isOnline")
        self.cancelBtn = QtWidgets.QPushButton(self.inputBox)
        self.cancelBtn.setGeometry(QtCore.QRect(330, 400, 71, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setDefault(False)
        self.cancelBtn.setObjectName("cancelBtn")
        self.keywordCx = QtWidgets.QComboBox(self.inputBox)
        self.keywordCx.setGeometry(QtCore.QRect(283, 195, 121, 26))
        self.keywordCx.setObjectName("keywordCx")
        self.keywordLbl = QtWidgets.QLabel(self.inputBox)
        self.keywordLbl.setGeometry(QtCore.QRect(227, 197, 61, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.keywordLbl.setFont(font)
        self.keywordLbl.setObjectName("keywordLbl")
        self.outputBox = QtWidgets.QGroupBox(Dialog)
        self.outputBox.setGeometry(QtCore.QRect(440, 10, 231, 451))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputBox.setFont(font)
        self.outputBox.setObjectName("outputBox")
        self.outputTxt = QtWidgets.QPlainTextEdit(self.outputBox)
        self.outputTxt.setGeometry(QtCore.QRect(20, 40, 191, 181))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.outputTxt.setFont(font)
        self.outputTxt.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.outputTxt.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.outputTxt.setObjectName("outputTxt")
        self.completedLbl = QtWidgets.QLabel(self.outputBox)
        self.completedLbl.setGeometry(QtCore.QRect(20, 230, 200, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.completedLbl.setFont(font)
        self.completedLbl.setObjectName("completedLbl")
        self.failureLbl = QtWidgets.QLabel(self.outputBox)
        self.failureLbl.setGeometry(QtCore.QRect(20, 420, 200, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.failureLbl.setFont(font)
        self.failureLbl.setObjectName("failureLbl")
        self.failureTxt = QtWidgets.QPlainTextEdit(self.outputBox)
        self.failureTxt.setGeometry(QtCore.QRect(20, 270, 191, 141))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.failureTxt.setFont(font)
        self.failureTxt.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.failureTxt.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.failureTxt.setObjectName("failureTxt")
        self.ankiflashInfoBox = QtWidgets.QGroupBox(Dialog)
        self.ankiflashInfoBox.setGeometry(QtCore.QRect(10, 470, 661, 141))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ankiflashInfoBox.setFont(font)
        self.ankiflashInfoBox.setObjectName("ankiflashInfoBox")
        self.buycoffee = QtWidgets.QLabel(self.ankiflashInfoBox)
        self.buycoffee.setGeometry(QtCore.QRect(20, 107, 811, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.buycoffee.setFont(font)
        self.buycoffee.setOpenExternalLinks(True)
        self.buycoffee.setObjectName("buycoffee")
        self.inbox = QtWidgets.QLabel(self.ankiflashInfoBox)
        self.inbox.setGeometry(QtCore.QRect(20, 83, 391, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.inbox.setFont(font)
        self.inbox.setObjectName("inbox")
        self.caption = QtWidgets.QLabel(self.ankiflashInfoBox)
        self.caption.setGeometry(QtCore.QRect(20, 30, 391, 16))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.caption.setFont(font)
        self.caption.setObjectName("caption")
        self.support = QtWidgets.QLabel(self.ankiflashInfoBox)
        self.support.setGeometry(QtCore.QRect(20, 57, 391, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.support.setFont(font)
        self.support.setOpenExternalLinks(True)
        self.support.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self.support.setObjectName("support")
        self.importBtn = QtWidgets.QPushButton(self.ankiflashInfoBox)
        self.importBtn.setGeometry(QtCore.QRect(535, 30, 113, 32))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.importBtn.setFont(font)
        self.importBtn.setObjectName("importBtn")
        self.mappingBtn = QtWidgets.QPushButton(self.ankiflashInfoBox)
        self.mappingBtn.setGeometry(QtCore.QRect(410, 30, 113, 32))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.mappingBtn.setFont(font)
        self.mappingBtn.setObjectName("mappingBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AnkiFlash"))
        self.inputBox.setTitle(_translate("Dialog", "Input"))
        self.inputTxt.setPlaceholderText(_translate("Dialog", "Input your words"))
        self.generateBtn.setToolTip(
            _translate("Dialog", "Generate flashcards for the input words")
        )
        self.generateBtn.setText(_translate("Dialog", "Generate"))
        self.totalLbl.setText(_translate("Dialog", "Total: 0"))
        self.sourceBox.setTitle(_translate("Dialog", "Source"))
        self.source3.setText(_translate("Dialog", "Japanese"))
        self.source4.setText(_translate("Dialog", "Vietnamese"))
        self.source2.setText(_translate("Dialog", "French"))
        self.source1.setText(_translate("Dialog", "English"))
        self.translatedToBox.setTitle(_translate("Dialog", "Translated To"))
        self.target6.setText(_translate("Dialog", "Chinese (Simplified)"))
        self.target2.setText(_translate("Dialog", "Vietnamese"))
        self.target1.setText(_translate("Dialog", "English"))
        self.target4.setText(_translate("Dialog", "Japanese"))
        self.target5.setText(_translate("Dialog", "Chinese (Traditional)"))
        self.target3.setText(_translate("Dialog", "French"))
        self.allWordTypes.setToolTip(
            _translate(
                "Dialog",
                "If a word has more than one type (noun, adjective, verb...), AnkiFlash will create cards for all of them",
            )
        )
        self.allWordTypes.setText(_translate("Dialog", "All word types?"))
        self.isOnline.setToolTip(
            _translate(
                "Dialog",
                "Usually, card sound will be downloaded to local computer. AnkiFlash provide an option to use online sound, your computer don't need to store sound file.",
            )
        )
        self.isOnline.setText(_translate("Dialog", "Online sound?"))
        self.cancelBtn.setToolTip(
            _translate("Dialog", "Cancel flashcards generation process")
        )
        self.cancelBtn.setText(_translate("Dialog", "Cancel"))
        self.keywordLbl.setText(_translate("Dialog", "Keyword"))
        self.outputBox.setTitle(_translate("Dialog", "Output"))
        self.outputTxt.setPlaceholderText(_translate("Dialog", "Output cards"))
        self.completedLbl.setText(_translate("Dialog", "Completed: 0"))
        self.failureLbl.setText(_translate("Dialog", "Failure: 0"))
        self.failureTxt.setPlaceholderText(_translate("Dialog", "Failure words"))
        self.ankiflashInfoBox.setTitle(_translate("Dialog", "AnkiFlash Info"))
        self.buycoffee.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p>If you want to buy me a coffee: <a href="https://www.buymeacoffee.com/longhoangly">https://www.buymeacoffee.com/longhoangly</a></p></body></html>',
            )
        )
        self.inbox.setText(
            _translate(
                "Dialog", "Feel free to drop me a message if any issue or suggestion"
            )
        )
        self.caption.setText(
            _translate("Dialog", "Always beside and help you to learn vocabularies")
        )
        self.support.setText(
            _translate(
                "Dialog",
                'Support: <a href="https://www.facebook.com/ankiflashcom/inbox" target="_blank">https://www.facebook.com/ankiflashcom/inbox</a>',
            )
        )
        self.importBtn.setToolTip(
            _translate("Dialog", "Cick here to import / create new cards.")
        )
        self.importBtn.setText(_translate("Dialog", "Import"))
        self.mappingBtn.setToolTip(
            _translate("Dialog", "To update existing flashcards with mapping fields")
        )
        self.mappingBtn.setText(_translate("Dialog", "Mapping"))
