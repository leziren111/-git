import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_Database.pyqtui.ui_main import Ui_MainWindow

import os


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWin, self).__init__()
        self.setupUi(self)

        # 添加信号与槽
        self.commandLinkButton.clicked.connect(self.query_student)  # 查询学生信息
        self.commandLinkButton_2.clicked.connect(self.make_view)  # 创建视图
        self.commandLinkButton_3.clicked.connect(self.make_index)  # 创建索引
        self.commandLinkButton_4.clicked.connect(self.modify_student)  # 修改学生信息（插入与删除）

    def query_student(self):
        os.system('python query_student.py')

    def make_view(self):
        os.system('python make_view.py')

    def make_index(self):
        os.system('python make_index.py')

    def modify_student(self):
        os.system('python modify_student.py')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyMainWin()
    mywindow.setWindowTitle('学生信息管理系统')
    mywindow.show()
    app.exec()
