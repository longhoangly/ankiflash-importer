# Form implementation generated from reading ui file '/ankiflash-importer/ui/ui_fields_updater.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class UiFieldsUpdater(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 352)
        self.importProgressBar = QtWidgets.QProgressBar(parent=Dialog)
        self.importProgressBar.setGeometry(QtCore.QRect(100, 310, 451, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.importProgressBar.setFont(font)
        self.importProgressBar.setProperty("value", 0)
        self.importProgressBar.setObjectName("importProgressBar")
        self.updateBtn = QtWidgets.QPushButton(parent=Dialog)
        self.updateBtn.setEnabled(True)
        self.updateBtn.setGeometry(QtCore.QRect(20, 310, 75, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.updateBtn.setFont(font)
        self.updateBtn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.updateBtn.setAutoFillBackground(False)
        self.updateBtn.setCheckable(False)
        self.updateBtn.setDefault(False)
        self.updateBtn.setObjectName("updateBtn")
        self.mappingGroup = QtWidgets.QGroupBox(parent=Dialog)
        self.mappingGroup.setGeometry(QtCore.QRect(20, 10, 531, 291))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mappingGroup.sizePolicy().hasHeightForWidth())
        self.mappingGroup.setSizePolicy(sizePolicy)
        self.mappingGroup.setObjectName("mappingGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mappingGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.mappingArea = QtWidgets.QScrollArea(parent=self.mappingGroup)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mappingArea.sizePolicy().hasHeightForWidth())
        self.mappingArea.setSizePolicy(sizePolicy)
        self.mappingArea.setMinimumSize(QtCore.QSize(400, 150))
        self.mappingArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mappingArea.setWidgetResizable(True)
        self.mappingArea.setObjectName("mappingArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 240))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.mappingArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.mappingArea, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AnkiFlash Fields Updater"))
        self.updateBtn.setToolTip(
            _translate("Dialog", "Import generated flashcards into Anki")
        )
        self.updateBtn.setText(_translate("Dialog", "Update"))
        self.mappingGroup.setTitle(
            _translate(
                "Dialog", "Field Mapping [Your fields mapped to AnkiFlash's fields]"
            )
        )
