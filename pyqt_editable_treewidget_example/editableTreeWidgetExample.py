import sys

from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAction, QMessageBox, QMainWindow, QApplication, QHBoxLayout, \
    QGroupBox, QWidget, QVBoxLayout, QCheckBox, QMenu, QPushButton, QFileDialog, QSpinBox, QLabel, QSpacerItem, \
    QSizePolicy, QSplitter, QTableWidget
from PyQt5.QtCore import Qt, QSettings


class EditableTreeWidget(QTreeWidget):

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__editedAtOnce = False
        self.__parentItemShouldNotChangedFlag = False

        item = QTreeWidgetItem(self)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText(0, 'Parent Attribute')
        self.setCurrentItem(item)

        self.header().setVisible(False)
        self.setIndentation(10)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__prepareMenu)

    def __prepareMenu(self, pos):
        menu = QMenu(self)

        addParentAttrAction = QAction("Add parent attribute")
        addParentAttrAction.triggered.connect(self.addParentAttr)

        addChildAttrAction = QAction("Add child attribute")
        addChildAttrAction.triggered.connect(self.addChildAttr)

        menu.addAction(addParentAttrAction)
        menu.addAction(addChildAttrAction)

        if self.itemAt(pos):
            renameAction = QAction('Rename')
            renameAction.triggered.connect(self.rename)
            menu.addAction(renameAction)

        menu.exec(self.mapToGlobal(pos))

    def keyPressEvent(self, e):
        try:
            if e.key() == Qt.Key_Return:
                if self.isPersistentEditorOpen(self.currentItem(), 0):
                    if self.currentItem().text(0).strip() == '':
                        QMessageBox.information(self, 'Error', "Unable to add empty value.")
                else:
                    self.addChildAttr()
            # parent up
            elif e.matches(QKeySequence.SelectPreviousLine):
                parent_item = self.currentItem().parent()
                if parent_item:
                    self.setCurrentItem(parent_item)
            # parent down
            elif e.matches(QKeySequence.SelectNextLine):
                child_item = self.currentItem().child(0)
                if child_item:
                    self.setCurrentItem(child_item)
            # above no matter what
            elif e.matches(QKeySequence.MoveToPreviousLine):
                above_item = self.itemAbove(self.currentItem())
                if above_item:
                    self.setCurrentItem(above_item)
            # below no matter what
            elif e.matches(QKeySequence.MoveToNextLine):
                below_item = self.itemBelow(self.currentItem())
                if below_item:
                    self.setCurrentItem(below_item)
            elif e.key() == Qt.Key_F2:
                self.editItem(self.currentItem(), 0)
            elif e.key() == Qt.Key_Delete:
                self.remove_attr()
            # prev sibiling
            # next sibiling
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

#        elif e.key() == Qt.Key_Up:
#        elif e.key() == Qt.Key_Down:

    def addParentAttr(self, text=None):
        text = 'dic' if not text or isinstance(text, bool) else text
        item = QTreeWidgetItem(self)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText(0, text)
        self.setCurrentItem(item)
        self.editItem(item, 0)

    def addChildAttr(self, text=None):
        text = 'New Attr' if not text or isinstance(text, bool) else text
        item = QTreeWidgetItem()
        item.setText(0, text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.currentItem().addChild(item)
        self.setCurrentItem(item)
        self.editItem(item, 0)
        if self.__parentItemShouldNotChangedFlag:
            item.parent().setFlags(item.flags() & ~Qt.ItemIsEditable)

    def rename(self):
        self.editItem(self.currentItem(), 0)
        self.__editedAtOnce = True

    def remove_attr(self):
        parent_item = self.currentItem().parent()
        if parent_item:
            item = self.currentItem()
            item.takeChildren()
            parent_item.removeChild(item)
            self.setCurrentItem(parent_item)
        else:
            self.takeTopLevelItem(self.indexOfTopLevelItem(self.currentItem()))

    def parentItemShouldNotChanged(self, f):
        self.__parentItemShouldNotChangedFlag = f


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
        self.__treeWidget.setHeaderLabels(['Name', 'Description'])
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

        self.__leftTopWidget = QWidget()
        self.__leftTopWidget.setLayout(lay)
        self.__leftTopWidget.setVisible(False)

        lay = QVBoxLayout()
        lay.addWidget(self.__leftTopWidget)
        lay.addWidget(self.__treeWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        extendedSelectionChkBox = QCheckBox('Extended Selection')
        extendedSelectionChkBox.toggled.connect(self.__extendedSelectionToggled)
        
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

        keyCommandTable = QTableWidget()
        keyCommandTable.setVisible(False)

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

    def __extendedSelectionToggled(self, f):
        if f:
            self.__treeWidget.setSelectionMode(QTreeWidget.ExtendedSelection)
        else:
            self.__treeWidget.setSelectionMode(QTreeWidget.SingleSelection)
        self.__treeWidget.clearSelection()

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

    def __allowDuplicated(self):
        print('__allowDuplicated')
        
    def __multiColumnToggled(self, f):
        self.__leftTopWidget.setVisible(f)
        self.__treeWidget.setHeaderHidden(f)

    def __load(self):
        if self.__settings_struct.value('dict'):
            data = eval(self.__settings_struct.value('dict'))
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
            dictToTree(data, self.__treeWidget.invisibleRootItem())

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
        treeDictStr = str(treeDict)
        self.__settings_struct.setValue('dict', treeDictStr)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    app.exec_()
