from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QPushButton, QHBoxLayout, QWidget, QCheckBox, QGroupBox
from PyQt5.QtCore import Qt


class CheckBoxDialog(QDialog):
    def __init__(self, title, columns):
        super().__init__()
        self.__columns = columns
        self.__initUi(title)

    def __initUi(self, title):
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.__grpBox = QGroupBox()
        self.__grpBox.setTitle('Uncheck columns to hide')

        lay = QVBoxLayout()

        for col_info in self.__columns:
            hidden_f, name = col_info
            chkBox = QCheckBox(name)
            chkBox.setChecked(not hidden_f)
            lay.addWidget(chkBox)

        lay.itemAt(0).widget().setEnabled(False)

        self.__grpBox.setLayout(lay)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.__okBtn = QPushButton('OK')
        self.__okBtn.clicked.connect(self.accept)

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
        lay.addWidget(self.__grpBox)
        lay.addWidget(sep)
        lay.addWidget(okCancelWidget)

        self.setLayout(lay)

    def getColumnInfo(self):
        lay = self.__grpBox.layout()
        lst = []
        for i in range(lay.count()):
            currentWidget = lay.itemAt(i).widget()
            if isinstance(currentWidget, QCheckBox):
                lst.append((currentWidget.checkState(), i))
        return lst