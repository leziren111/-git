import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_Database.pyqtui.ui_query_student import Ui_MainWindow

import connect


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWin, self).__init__()
        self.setupUi(self)
        # 添加信号与槽
        self.pushButton.clicked.connect(self.join_query)
        self.pushButton_2.clicked.connect(self.nest_query)
        self.pushButton_3.clicked.connect(self.avg_query)

    # 连接查询,分组查询
    def join_query(self):
        # 查询选课数大于输入的学生
        con = connect.GetConn()
        cur = con.cursor()
        try:
            # 获取输入
            text = self.lineEdit.text()
            if not text:
                QMessageBox.warning(self, '警告', '请输入数目')
            elif int(text) < 0:
                QMessageBox.warning(self, '警告', '请输入正确的数量')
            else:
                # 连接查询，分组查询+having
                sql = f'select sname from student natural join grade group by grade.sid having count(*)>{text}'
                print(sql)
                cur.execute(sql)
                data = cur.fetchall()
                if len(data) > 0:
                    msg = f'课程数目超过{text}的学生有:\n'
                    for item in data:
                        msg += item[0] + '\n'
                else:
                    msg = '无结果'
                QMessageBox.information(self, '学习状况', msg)
        except Exception as e:
            print(e)
            con.rollback()

        connect.CloseConn(con, cur)

    # 嵌套查询
    def nest_query(self):
        # 查找选择了某门课程的学生
        con = connect.GetConn()
        cur = con.cursor()
        try:
            # 获取输入
            cid = self.lineEdit_2.text()
            print(cid)
            if not cid:
                QMessageBox.warning(self, '警告', '请输入课程号')
            elif len(cid) != 3:
                QMessageBox.warning(self, '警告', '课程号为3位数字')
            else:
                sql = f'select sname from student where sid in (select sid from grade where cid={cid})'  # 嵌套查询
                print(sql)
                cur.execute(sql)
                data = cur.fetchall()
                if len(data) > 0:
                    msg = f'选修编号为{cid}的学生有:\n'
                    for item in data:
                        msg += item[0] + '\n'
                else:
                    msg = '无结果'
                QMessageBox.information(self, '课程规模', msg)
        except Exception as e:
            print(e)
            con.rollback()

        connect.CloseConn(con, cur)

    # 嵌套查询，分组查询
    def avg_query(self):
        # 查询某个学生的平均分
        con = connect.GetConn()
        cur = con.cursor()
        try:
            sname = self.lineEdit_3.text()
            print(sname)
            if not sname:
                QMessageBox.warning(self, '警告', '请输入姓名')
            else:
                res = []
                sql = f"select sid, avg(score) from grade where sid in " \
                      f"(select sid from student where sname='{sname}') group by sid"
                print(sql)
                cur.execute(sql)
                data = cur.fetchall()
                for item in data:
                    res.append(
                        f'学号为{str(item[0])}的学生{sname}全部科目的平均成绩为\t{str(item[1])}')
                    print(item[1])
                QMessageBox.information(self, '平均成绩', '\n'.join(res) if len(res) != 0 else '无结果')
        except Exception as e:
            print(e)
            con.rollback()

        connect.CloseConn(con, cur)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyMainWin()
    mywindow.setWindowTitle('学生查询')
    mywindow.show()
    app.exec()
