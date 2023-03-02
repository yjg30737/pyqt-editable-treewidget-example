from collections import defaultdict

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QLabel, QHeaderView

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit


class ShortcutLineEdit(QLineEdit):
    keyPressed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__modifiers_list = (Qt.CTRL | Qt.ALT | Qt.SHIFT | Qt.META)

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = int(event.modifiers())
        if modifiers:
            if (modifiers & self.__modifiers_list == modifiers and
                key > 0 and key != Qt.Key_Shift and key != Qt.Key_Alt and
                key != Qt.Key_Control and key != Qt.Key_Meta):
                    keyname = QKeySequence(modifiers + key).toString()
            else:
                keyname = QKeySequence(modifiers).toString()[:-1]
        else:
            keyname = QKeySequence(key).toString()
        self.setText(keyname)


# https://github.com/yjg30737/pyqt-key-binding-example
class KeyBindingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        lbl = QLabel('Key Bindings')

        actionsTableWidget = QTableWidget()

        # actionsDict = defaultdict(str)
        # for w in QApplication.allWidgets():
        #     actions = w.actions()
        #     if actions:
        #         for a in actions:
        #             name = a.text()
        #             key = a.shortcut().toString()
        #             if name:
        #                 actionsDict[name] = key
        #
        # actionsTableWidget.setRowCount(len(actionsDict))
        # actionsTableWidget.setColumnCount(1)
        # actionsTableWidget.horizontalHeader().setVisible(False)
        #
        # actionNames = actionsDict.keys()
        # actionsTableWidget.setVerticalHeaderLabels(actionNames)
        # actionsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        #
        # i = 0
        # for key in actionsDict.values():
        #     lineEdit = ShortcutLineEdit()
        #     lineEdit.setText(key)
        #     actionsTableWidget.setCellWidget(i, 0, lineEdit)
        #     i += 1

        lay = QVBoxLayout()
        lay.addWidget(lbl)
        lay.addWidget(actionsTableWidget)

        self.setLayout(lay)