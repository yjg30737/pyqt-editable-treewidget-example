import sys, json

from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAction, QMessageBox, QMainWindow, QApplication, QHBoxLayout, \
    QGroupBox, QWidget, QVBoxLayout, QCheckBox, QMenu, QPushButton, QFileDialog, QSpinBox, QLabel, QSpacerItem, \
    QSizePolicy, QSplitter, QTableWidget
from PyQt5.QtCore import Qt, QSettings

from pyqt_editable_treewidget_example.editableTreeWidget import EditableTreeWidget
from pyqt_editable_treewidget_example.keyCommandWidget import KeyBindingWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__settings_struct = QSettings('tree.ini', QSettings.IniFormat)

    def __initUi(self):
        self.setWindowTitle('QTreeWidget Playground')
        self.__treeWidget = EditableTreeWidget()
        # ['Name', 'Description']
        self.__treeWidget.setHeaderLabels(['Name'])
        self.__treeWidget.setHeaderHidden(True)

        addColBtn = QPushButton('Add Column')
        delColBtn = QPushButton('Delete Column')

        treeLbl = QLabel('Tree')
        treeLblFont = QFont('Arial', 12)
        treeLbl.setFont(treeLblFont)

        lay = QHBoxLayout()
        lay.addWidget(treeLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(addColBtn)
        lay.addWidget(delColBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__leftNavWidget = QWidget()
        self.__leftNavWidget.setLayout(lay)
        self.__leftNavWidget.setVisible(False)

        self.__expandTreeBtn = QPushButton('Expand')
        self.__expandTreeBtn.setCheckable(True)
        self.__expandTreeBtn.toggled.connect(self.__expandToggled)

        lay = QHBoxLayout()
        lay.addWidget(self.__expandTreeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__rightNavWidget = QWidget()
        self.__rightNavWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(self.__leftNavWidget)
        lay.addWidget(self.__rightNavWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        navWidget = QWidget()
        navWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(navWidget)
        lay.addWidget(self.__treeWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        extendedSelectionChkBox = QCheckBox('Extended Selection')
        extendedSelectionChkBox.toggled.connect(self.__extendedSelectionToggled)
        f = True if self.__settings_struct.value('selection') == '1' else False
        extendedSelectionChkBox.setChecked(f)
        
        self.__duplicatedChkBox = QCheckBox('Allow duplicated name (testing)')
        self.__duplicatedChkBox.toggled.connect(self.__allowDuplicated)
        self.__duplicatedChkBox.setChecked(True)
        self.__duplicatedChkBox.setDisabled(True)

        self.__makeItUnableToChangeWhichHasChild = QCheckBox('Make it unable to change item\'s name which has child')
        self.__makeItUnableToChangeWhichHasChild.toggled.connect(self.__makeItUnableToChangeWhichHasChildToggled)

        multiColumnChkBox = QCheckBox('Multi Column Mode (testing)')
        multiColumnChkBox.setChecked(False)
        multiColumnChkBox.setDisabled(True)
        multiColumnChkBox.toggled.connect(self.__multiColumnToggled)
        
        saveBtn = QPushButton('Save')
        saveBtn.clicked.connect(self.__save)

        keyCommandTable = KeyBindingWidget()

        lay = QVBoxLayout()
        lay.addWidget(keyCommandTable)

        controlGrpBox = QGroupBox('Control (testing)')
        controlGrpBox.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(extendedSelectionChkBox)
        lay.addWidget(self.__makeItUnableToChangeWhichHasChild)
        lay.addWidget(self.__duplicatedChkBox)
        lay.addWidget(multiColumnChkBox)
        lay.addWidget(saveBtn)
        lay.setAlignment(Qt.AlignTop)

        optionGrpBox = QGroupBox('Option')
        optionGrpBox.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(controlGrpBox)
        lay.addWidget(optionGrpBox)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        leftWidget.setObjectName('leftWidget')
        leftWidget.setStyleSheet('QWidget#leftWidget { background-color: #DDD }')

        splitter = QSplitter()
        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)
        splitter.setSizes([600, 400])
        splitter.setChildrenCollapsible(False)

        self.setCentralWidget(splitter)

        self.__load()

        # set the attributes which should set after the loading
        f = True if self.__settings_struct.value('makeItUnableToChangeWhichHasChild') == '1' else False
        self.__makeItUnableToChangeWhichHasChild.setChecked(f)

    def __expandToggled(self, f):
        if f:
            self.__treeWidget.expandAll()
            self.__expandTreeBtn.setText('Collapse')
        else:
            self.__treeWidget.collapseAll()
            self.__expandTreeBtn.setText('Expand')

    def __extendedSelectionToggled(self, f):
        if f:
            self.__treeWidget.setSelectionMode(QTreeWidget.ExtendedSelection)
        else:
            self.__treeWidget.setSelectionMode(QTreeWidget.SingleSelection)
        self.__treeWidget.clearSelection()
        self.__settings_struct.setValue('selection', str(int(f)))

    # update all previous ones who have the child to toggle the ItemIsEditable flag
    def __makeItUnableToChangeWhichHasChildToggled(self, f):
        self.__treeWidget.parentItemShouldNotChanged(f)
        if f:
            for i in range(self.__treeWidget.topLevelItemCount()):
                item = self.__treeWidget.topLevelItem(i)
                while item:
                    if item.childCount() > 0:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        item = item.child(0)
                    else:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                        break
        else:
            for i in range(self.__treeWidget.topLevelItemCount()):
                item = self.__treeWidget.topLevelItem(i)
                while item:
                    if item.childCount() > 0:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                        item = item.child(0)
                    else:
                        break
        self.__settings_struct.setValue('makeItUnableToChangeWhichHasChild', str(int(f)))

    def __allowDuplicated(self):
        print('__allowDuplicated')
        
    def __multiColumnToggled(self, f):
        self.__leftNavWidget.setVisible(f)
        self.__treeWidget.setHeaderHidden(f)

    def __load(self):
        with open('tree.json', 'r') as f:
            json_data = json.load(f)

            def dictToTree(data, parent):
                for key, value in data.items():
                    item = QTreeWidgetItem(parent)
                    item.setText(0, str(key))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    if isinstance(value, dict):
                        dictToTree(value, item)
                    else:
                        item.setText(1, str(value))

            self.__treeWidget.clear()
            dictToTree(json_data, self.__treeWidget.invisibleRootItem())

    def __save(self):
        def treeToDict(tree):
            result = {}
            for i in range(tree.topLevelItemCount()):
                item = tree.topLevelItem(i)
                result[item.text(0)] = treeToDictHelper(item)
            return result

        def treeToDictHelper(item):
            result = {}
            for i in range(item.childCount()):
                child = item.child(i)
                result[child.text(0)] = treeToDictHelper(child)
            return result

        treeDict = treeToDict(self.__treeWidget)

        json_data = json.dumps(treeDict)

        with open('tree.json', 'w') as f:
            f.write(json_data)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    app.exec_()
