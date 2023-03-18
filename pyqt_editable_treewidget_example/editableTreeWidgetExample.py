import os.path
import sys, json

from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAction, QMessageBox, QMainWindow, QApplication, QHBoxLayout, \
    QGroupBox, QWidget, QVBoxLayout, QCheckBox, QMenu, QPushButton, QFileDialog, QSpinBox, QLabel, QSpacerItem, \
    QSizePolicy, QSplitter, QTableWidget, QDialog
from PyQt5.QtCore import Qt, QSettings

from pyqt_editable_treewidget_example.checkBoxDialog import CheckBoxDialog
from pyqt_editable_treewidget_example.editableTreeWidget import EditableTreeWidget, EditableTreeWidgetItem
from pyqt_editable_treewidget_example.inputDialog import InputDialog
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
        addColBtn.clicked.connect(self.__addCol)
        hideColBtn = QPushButton('Hide Column')
        hideColBtn.clicked.connect(self.__hideCol)

        treeLbl = QLabel('Tree')
        treeLblFont = QFont('Arial', 12)
        treeLbl.setFont(treeLblFont)

        lay = QHBoxLayout()
        lay.addWidget(treeLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(addColBtn)
        lay.addWidget(hideColBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__leftNavWidget = QWidget()
        self.__leftNavWidget.setLayout(lay)
        self.__leftNavWidget.setVisible(False)

        self.__expandTreeBtn = QPushButton('Expand')
        self.__expandTreeBtn.setCheckable(True)
        self.__expandTreeBtn.toggled.connect(self.__expandToggled)

        self.__clearBtn = QPushButton('Clear')
        self.__clearBtn.clicked.connect(self.__treeWidget.clear)

        lay = QHBoxLayout()
        lay.addWidget(self.__expandTreeBtn)
        lay.addWidget(self.__clearBtn)
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

        multiColumnChkBox = QCheckBox('Multi Column Mode')
        multiColumnChkBox.toggled.connect(self.__multiColumnToggled)
        f = True if self.__settings_struct.value('multicolumn') == '1' else False
        multiColumnChkBox.setChecked(f)

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

    def __addCol(self):
        labels = [self.__treeWidget.headerItem().text(i) for i in range(self.__treeWidget.headerItem().columnCount())]
        dialog = InputDialog('New header', labels)
        reply = dialog.exec()
        if reply == QDialog.Accepted:
            self.__treeWidget.setColumnCount(self.__treeWidget.columnCount()+1)
            self.__treeWidget.setHeaderLabels(labels + [dialog.getNewName()])

    def __hideCol(self):
        columns = [(self.__treeWidget.isColumnHidden(i), self.__treeWidget.headerItem().text(i))
                  for i in range(self.__treeWidget.headerItem().columnCount())]
        dialog = CheckBoxDialog('Show/Hide Columns', columns)
        reply = dialog.exec()
        if reply == QDialog.Accepted:
            col_info_lst = dialog.getColumnInfo()
            for i in range(len(col_info_lst)-1, -1, -1):
                state, idx = col_info_lst[i]
                if state == 0:
                    self.__treeWidget.hideColumn(idx)
                else:
                    self.__treeWidget.showColumn(idx)

    def __multiColumnToggled(self, f):
        self.__leftNavWidget.setVisible(f)
        self.__treeWidget.setHeaderHidden(not f)
        self.__settings_struct.setValue('multicolumn', str(int(f)))

    def __load(self):
        if os.path.exists('tree.json'):
            with open('tree.json', 'r') as f:
                json_data = json.load(f)

                def dictToTree(data, parent):
                    for obj in data:
                        item = EditableTreeWidgetItem(parent)
                        header_val_lst = list(obj['name'].values())
                        for i in range(len(header_val_lst)):
                            item.setText(i, header_val_lst[i])
                        if obj['editable']:
                            item.setFlags(item.flags() | Qt.ItemIsEditable)
                        else:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                        if len(obj['data']) > 0:
                            dictToTree(obj['data'], item)

                self.__treeWidget.clear()
                header_key_lst = json_data[0]['name'].keys()
                self.__treeWidget.setColumnCount(len(header_key_lst))
                self.__treeWidget.setHeaderLabels(header_key_lst)
                dictToTree(json_data, self.__treeWidget.invisibleRootItem())

    def __save(self):
        def treeToDict(tree):
            result_obj_lst = []
            for i in range(tree.topLevelItemCount()):
                top_item = tree.topLevelItem(i)

                # get each header's name(key) and its data(value)
                header_item = tree.headerItem()
                header_name_dict = dict()
                for j in range(header_item.columnCount()):
                    header_name_dict[header_item.text(j)] = top_item.text(j)

                result_obj = {'name': header_name_dict, 'editable': bool(top_item.flags() & Qt.ItemIsEditable),
                              'data': treeToDictHelper(tree, top_item)}
                result_obj_lst.append(result_obj)
            return result_obj_lst

        def treeToDictHelper(tree, item):
            result_obj_lst = []
            for i in range(item.childCount()):
                child = item.child(i)

                # get each header's name(key) and its data(value)
                header_item = tree.headerItem()
                header_name_dict = dict()
                for j in range(header_item.columnCount()):
                    header_name_dict[header_item.text(j)] = child.text(j)

                result_obj = {'name': header_name_dict, 'editable': bool(child.flags() & Qt.ItemIsEditable),
                              'data': treeToDictHelper(tree, child)}
                result_obj_lst.append(result_obj)
            return result_obj_lst

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
