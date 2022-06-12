# pyqt-editable-treewidget-example
PyQt example of QTreeWidget which is editable

Intuitive enough to use, but this is for example only

## Requirements
* PyQt5 >= 5.8

## Setup
`python -m pip install git+https://github.com/yjg30737/pyqt-editable-treewidget-example.git --upgrade`

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

https://user-images.githubusercontent.com/55078043/173221882-37766b10-d38a-4953-bc12-fb2b8bd7171b.mp4

