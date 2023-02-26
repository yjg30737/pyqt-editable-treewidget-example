import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAction, QMessageBox, QMainWindow, QApplication, QHBoxLayout, \
    QGroupBox, QWidget, QVBoxLayout, QCheckBox, QMenu
from PyQt5.QtCore import Qt


class EditableTreeWidget(QTreeWidget):

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__editedAtOnce = False

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

    def addParentAttr(self):
        item = QTreeWidgetItem(self)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText(0, 'dic')
        self.setCurrentItem(item)
        self.editItem(item, 0)

    def addChildAttr(self):
        item = QTreeWidgetItem()
        item.setText(0, 'New Attr')
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.currentItem().addChild(item)
        self.setCurrentItem(item)
        self.editItem(item, 0)

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

    def event(self, e):
        return super().event(e)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__treeWidget = EditableTreeWidget()
        self.__treeWidget.itemChanged.connect(self.__treeWidgetItemChanged)

        extendedSelectionChkBox = QCheckBox('Extended Selection')
        extendedSelectionChkBox.toggled.connect(self.__extendedSelectionToggled)

        self.__makeItUnableToChangeWhichHasChild = QCheckBox('Make it unable to change item\'s name which has child')
        self.__makeItUnableToChangeWhichHasChild.toggled.connect(self.__makeItUnableToChangeWhichHasChildToggled)

        lay = QVBoxLayout()
        lay.addWidget(extendedSelectionChkBox)
        lay.addWidget(self.__makeItUnableToChangeWhichHasChild)
        lay.setAlignment(Qt.AlignTop)

        optionGrpBox = QGroupBox('Option')
        optionGrpBox.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(self.__treeWidget)
        lay.addWidget(optionGrpBox)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __extendedSelectionToggled(self, f):
        if f:
            self.__treeWidget.setSelectionMode(QTreeWidget.ExtendedSelection)
        else:
            self.__treeWidget.setSelectionMode(QTreeWidget.SingleSelection)
        self.__treeWidget.clearSelection()

    def __makeItUnableToChangeWhichHasChildToggled(self, f):
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

    def __treeWidgetItemChanged(self, item: QTreeWidgetItem):
        f = self.__makeItUnableToChangeWhichHasChild.isChecked()
        if f:
            parentItem = item.parent()
            if parentItem:
                parentItem.setFlags(item.flags() & ~Qt.ItemIsEditable)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    app.exec_()
