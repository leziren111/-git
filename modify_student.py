import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_Database.pyqtui.ui_modify_student import Ui_MainWindow

import connect


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWin, self).__init__()
        self.setupUi(self)
        # # 添加信号与槽
        self.pushButton.clicked.connect(self.insert_student)
        self.pushButton_2.clicked.connect(self.delete_student)

    # 插入信息
    def insert_student(self):
        # 连接数据库
        con = connect.GetConn()
        cur = con.cursor()

        try:
            # 读取输入
            sid, sname, de_name, classid, dorm = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), \
                                                 self.lineEdit_4.text(), self.lineEdit_5.text()
            print('插入：', sid, sname, de_name, classid, dorm)
            if not sid or not sname or not de_name or not classid or not dorm:  # 插入错误值，空值，提醒
                QMessageBox.warning(self, '警告',
                                    '请输入学号、姓名、系名、班号和宿舍')  # 学号为主键，姓名为自定义完整性，其余为外键（空或者不空但在外关系存在）
            elif len(sid) != 4:
                QMessageBox.warning(self, '警告', '学号为4位数字')
            elif len(classid) != 7:
                QMessageBox.warning(self, '警告', '班号为7位数字')
            elif len(dorm) != 4:
                QMessageBox.warning(self, '警告', '宿舍号为4位数字')
            else:
                if cur.execute(f'select * from student where sid={sid}'):
                    QMessageBox.warning(self, '插入异常', '该学号已存在，请重新输入')  # 主键唯一
                elif not cur.execute(f"select * from department where name='{de_name}'"):
                    QMessageBox.warning(self, '插入异常', '该系不存在，请尝试插入正确条目')  # 参照完整性
                elif not cur.execute(f'select * from class where id={classid}'):
                    QMessageBox.warning(self, '插入异常', '该班级不存在，请尝试插入正确条目')  # 参照完整性
                elif not cur.execute(f'select * from dorm where id={dorm}'):
                    QMessageBox.warning(self, '插入异常', '该宿舍不存在，请尝试插入正确条目')  # 参照完整性
                else:
                    sql = f"insert into student(sid, sname, de_name, class, dorm) " \
                          f"values ({sid}, '{sname}', '{de_name}', {classid}, {dorm})"
                    print(sql)
                    cur.execute(sql)
                    QMessageBox.information(self, '插入成功', '成功插入一条学生数据')
                    con.commit()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "插入失败！")
            con.rollback()

        connect.CloseConn(con, cur)

    # 删除信息
    def delete_student(self):
        # 连接数据库
        con = connect.GetConn()
        cur = con.cursor()

        try:
            sid = self.lineEdit.text()
            print('删除学号', sid, '的学生')
            if not sid:
                QMessageBox.warning(self, '警告', '学号为空')
            elif len(sid) != 4:
                QMessageBox.warning(self, '警告', '学号只可为4位数字')
            else:
                sql = f'select * from student where sid={sid}'
                if not cur.execute(sql):
                    QMessageBox.warning(self, "删除异常", "该学号不存在，请重新输入")
                else:
                    if cur.execute(f'select * from grade where sid={sid}'):
                        QMessageBox.information(self, '提示',
                                                '该学号在其他表中被作为外键引用，触发器已默认删除其他表中对应条目的数据')
                        sql = f'delete from grade where sid={sid}'
                        cur.execute(sql, [sid])
                    sql = f'delete from student where sid={sid}'
                    cur.execute(sql)
                    QMessageBox.information(self, '成功', '成功删除学生数据')
                    con.commit()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "删除失败！")
            con.rollback()

        connect.CloseConn(con, cur)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyMainWin()
    mywindow.setWindowTitle('修改信息')
    mywindow.show()
    app.exec()



