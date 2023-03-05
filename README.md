# pyqt-editable-treewidget-example
PyQt example of QTreeWidget which is editable

Intuitive enough to use, but this is for example only

## Requirements
* PyQt5 >= 5.8

## Setup
* git clone ~

## Feature
* Show the exmaple of adding & deleting the tree widget item in convinient way
* Support multiple options:
    * make it unable to edit the parent item's name which has the child
    * user can make the certain item not editable
    * convert the QTreeWidget hierarchy into JSON format (in Python, array of Python dictionary) to save in "tree.json"
    * Load the saved JSON content and convert it into QTreeWidget when user executes the window again
    
The each object of tree.json contains multiple properties - name of the item(name), editable flag(editable), childs of the item(data)

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
* Rename - rename the item
* Editable - check to make the item editable or not

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

Whole window (v0.0.161)

![image](https://user-images.githubusercontent.com/55078043/222945406-34ff5410-d8f5-4ba7-8511-79e7e947fc6d.png)

