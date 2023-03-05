import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAction, QMessageBox, QMenu
from PyQt5.QtCore import Qt


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

            editableAction = QAction('Editable')
            editableAction.setCheckable(True)
            editableAction.setChecked(True)
            editableAction.setDisabled(True)
            menu.addAction(editableAction)

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