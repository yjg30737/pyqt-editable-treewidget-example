from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QFrame, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt


class InputDialog(QDialog):
    def __init__(self, title, labels):
        super().__init__()
        self.__labels = labels
        self.__initUi(title)

    def __initUi(self, title):
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.__newName = QLineEdit()
        self.__newName.textChanged.connect(self.__setAccept)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.__okBtn = QPushButton('OK')
        self.__okBtn.clicked.connect(self.accept)
        self.__okBtn.setEnabled(False)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__okBtn)
        lay.addWidget(cancelBtn)
        lay.setAlignment(Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        okCancelWidget = QWidget()
        okCancelWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(self.__newName)
        lay.addWidget(sep)
        lay.addWidget(okCancelWidget)

        self.setLayout(lay)

    def getNewName(self):
        return self.__newName.text()
    
    def __setAccept(self, text):
        self.__okBtn.setEnabled(text.strip() != '' and text not in self.__labels)