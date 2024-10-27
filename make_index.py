import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_Database.pyqtui.ui_make_index import Ui_MainWindow

import connect


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWin, self).__init__()
        self.setupUi(self)
        # 添加信号与槽
        self.pushButton.clicked.connect(self.makeindex)

    # 建立索引
    def makeindex(self):
        # 连接数据库
        con = connect.GetConn()
        cur = con.cursor()

        try:
            idx = self.comboBox.currentIndex()

            dic = ['sname', 'de_name', 'class', 'dorm']
            index = dic[idx]
            print(index)

            # 查询索引是否已被定义
            sql = f"select count(*) from information_schema.INNODB_INDEXES where NAME='idx_{index}'"
            cur.execute(sql)
            if cur.fetchone()[0] == 1:
                QMessageBox.warning(self, '提示', f'索引{index}已被定义')
            else:
                sql = f'create index idx_{index} on student({index})'
                print(sql)
                cur.execute(sql)
                con.commit()
                QMessageBox.information(self, '成功', f'成功创建索引：idx_{index}')
        except Exception as e:
            print(e)
            con.rollback()

        connect.CloseConn(con, cur)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyMainWin()
    mywindow.setWindowTitle('索引建立')
    mywindow.show()
    app.exec()





