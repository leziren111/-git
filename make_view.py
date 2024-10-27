import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from Ui_Database.pyqtui.ui_make_view import Ui_MainWindow

import connect


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWin, self).__init__()
        self.setupUi(self)
        # 添加信号与槽
        self.pushButton.clicked.connect(self.makeview)

    # 建立视图
    def makeview(self):
        # 连接数据库
        con = connect.GetConn()
        cur = con.cursor()

        try:
            # 获取数据
            index = self.comboBox.currentIndex()
            de_name = self.comboBox.currentText()
            name_view = ['cs', 'se', 'ai', 'ins', 'ds', 'iot', 'bio', 'mm', 'id', 'ce', 'ee', 'cse', 'aero']
            print(index, name_view[index], de_name)
            # 先将已有的视图删除掉
            sql = f"drop view if exists {name_view[index]}"
            cur.execute(sql)
            # 建立视图
            sql = f"create view {name_view[index]} as select * from student where de_name='{de_name}'"
            print(sql)
            cur.execute(sql)
            con.commit()
            print("创建视图成功")

            # 读取视图，输出到表格
            cur.execute(f"select * from {name_view[index]}")
            # 获取数据
            data = cur.fetchall()
            # 设置表格行列数
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))
            # 设置表头
            self.tableWidget.setHorizontalHeaderLabels(['学号', '姓名', '系名', '班号', '宿舍'])
            # 设置表格内容
            for i in range(len(data)):
                for j in range(len(data[i])):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
            # 设置表格自适应大小
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Exception as e:
            print(e)
            con.rollback()

        connect.CloseConn(con, cur)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyMainWin()
    mywindow.setWindowTitle('视图建立')
    mywindow.show()
    app.exec()
