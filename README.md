# pyqt-editable-treewidget-example
PyQt example of QTreeWidget which is editable

Intuitive enough to use, but this is for example only

## Requirements
* PyQt5 >= 5.8

## Setup
`python -m pip install git+https://github.com/yjg30737/pyqt-editable-treewidget-example.git --upgrade`

## Feature
* Show the exmaple of adding & deleting the tree widget item in convinient way
* Support multiple options:
    * make it unable to edit the parent item's name which has the child
    * convert the QTreeWidget hierarchy into Python dictionary to save in "tree.ini" (with QSettings)
    * Load the saved Python dictionary and convert it into QTreeWidget when user executes the window again

## Usage
Key command
* Enter/Return - Add new child
* F2 - Rename attribute
* Delete - Remove attribute
* Up/Down - Previous/next attribute
* Shift+Up/Down - Go parent/child attribute 

Context Menu
* Add parent attribute
* Add child attribute

## Example
Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_editable_treewidget_example import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    app.exec_()
```

Result

Basic control of the treewidget

https://user-images.githubusercontent.com/55078043/173221882-37766b10-d38a-4953-bc12-fb2b8bd7171b.mp4

Whole window

![image](https://user-images.githubusercontent.com/55078043/221781997-35a5040f-9114-4a32-95ec-c63695ac188a.png)

