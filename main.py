from PyQt5.QtWidgets import QApplication
from pyqt_editable_treewidget_example import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    app.exec_()