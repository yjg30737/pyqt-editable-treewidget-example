from collections import defaultdict

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QLabel, QHeaderView, QTableWidgetItem

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit


KEY_MAP = {
    'ADD_NEW_CHILD': ('Add New Child', 'Enter'),
    'RENAME_ATTR': ('Rename Attribute', 'F2'),
    'REMOVE_ATTR': ('Remove Attribute', 'Delete'),
    'PREVIOUS_ATTR': ('Select Previous Attribute', 'Up'),
    'NEXT_ATTR': ('Select Next Attribute', 'Down'),
    'GO_PARENT_ATTR': ('Go to Parent Attribute', 'Shift+Up'),
    'GO_CHILD_ATTR': ('Go to Child Attribute', 'Shift+Down'),
}


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
        actionsTableWidget.setColumnCount(2)
        key_map_lst = list(KEY_MAP.values())
        actionsTableWidget.setRowCount(len(key_map_lst))
        actionsTableWidget.horizontalHeader().setVisible(False)
        actionsTableWidget.verticalHeader().setVisible(False)
        actionsTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(len(key_map_lst)):
            actionsTableWidget.setItem(i, 0, QTableWidgetItem(key_map_lst[i][0]))
            actionsTableWidget.setItem(i, 1, QTableWidgetItem(key_map_lst[i][1]))

        actionsTableWidget.setDisabled(True)

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