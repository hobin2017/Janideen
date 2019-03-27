# -*- coding: utf-8 -*-
"""

"""
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QColor, QStandardItem
from PyQt5.QtWidgets import QTableView, QHeaderView, QFrame, QApplication, QPushButton

from LoggingModule import MyLogging1_2


class CheckBox_Text_Item(QStandardItem):

    def __init__(self, text='hobin', parent=None):
        super().__init__(parent)
        self.setEditable(False)
        self.setSelectable(False)
        self.setCheckable(True)
        self.setCheckState(Qt.Checked)
        #
        self.init_text = text
        self.setText(self.init_text)


class Label_List_Model01(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['labels list'])
        # others
        self.mylogging4label_list_model01 = MyLogging1_2(logger_name='hobin')


    def adding_new_row(self, column_index=0, text='hobin'):
        self.mylogging4label_list_model01.logger.info('---------adding_new_row of %s starts---------' % self.__class__)
        new_label = CheckBox_Text_Item(text=text)
        row_index = self.rowCount()
        self.setItem(row_index, column_index, new_label)
        self.mylogging4label_list_model01.logger.info('---------adding_new_row of %s ends---------' % self.__class__)

    def deleting_current_row(self, row_index, column_index=0):
        self.mylogging4label_list_model01.logger.info('---------deleting_current_row of %s starts---------' % self.__class__)
        self.mylogging4label_list_model01.logger.info(row_index)
        self.removeRow(row_index)
        self.mylogging4label_list_model01.logger.info('---------deleting_current_row of %s ends---------' % self.__class__)

    def refreshing(self):
        self.mylogging4label_list_model01.logger.info('---------deleting_current_row of %s starts---------' % self.__class__)
        # todo:
        self.mylogging4label_list_model01.logger.info('---------deleting_current_row of %s ends---------' % self.__class__)

    def modifying_text(self, row_index, column_index=0, text=''):
        self.mylogging4label_list_model01.logger.info('---------modifying_text of %s starts---------' % self.__class__)
        self.mylogging4label_list_model01.logger.info(row_index)
        self.mylogging4label_list_model01.logger.info(text)
        self.setData(self.index(row_index, column_index), text, Qt.DisplayRole)
        self.mylogging4label_list_model01.logger.info('---------modifying_text of %s ends---------' % self.__class__)

    def modifying_color(self, qcolor, row_index, column_index=0):
        self.mylogging4label_list_model01.logger.info('---------modifying_color of %s starts---------' % self.__class__)
        self.setData(self.index(row_index, column_index), qcolor, Qt.BackgroundRole)
        self.mylogging4label_list_model01.logger.info('---------modifying_color of %s ends---------' % self.__class__)


class Label_List_Widget01(QTableView):
    reminder_selecting = pyqtSignal(object)
    reminder_unselecting = pyqtSignal(object)

    def __init__(self, parent=None, width=300, height=600):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setFixedSize(width, height)

        # header
        self.horizontalHeader().hide()
        # self.horizontalHeader().setStretchLastSection(True)  # only the last column do the stretching
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # every column do the stretching

        # model for item management
        self.table_model = Label_List_Model01(parent=self)
        self.setModel(self.table_model)

        # signal management
        # self.clicked.connect(self.onclick_table_view01)
        self.entered.connect(self.mouse_enter2table_view01)  # This requires that the mouse track is enabled

        # others
        self.last_mouse_enter_index = 0


    def onclick_table_view01(self, qmodel_index):
        print('---------onclick_table_view01 of %s starts---------' % self.__class__)
        print('row: %s' % qmodel_index.row())
        if qmodel_index.data(Qt.CheckStateRole) == Qt.Checked:
            print('checked')
        elif qmodel_index.data(Qt.CheckStateRole) == Qt.Unchecked:
            print('unchecked')
        print('---------onclick_table_view01 of %s ends---------' % self.__class__)

    def mouse_enter2table_view01(self, qmodel_index):
        # print('---------mouse_enter2table_view01 of %s starts---------' % self.__class__)
        # print('row: %s' % qmodel_index.row())  # int
        self.reminder_unselecting.emit(self.last_mouse_enter_index)
        self.reminder_selecting.emit(qmodel_index.row())
        self.last_mouse_enter_index = qmodel_index.row()
        # print('---------mouse_enter2table_view01 of %s ends---------' % self.__class__)

    def leaveEvent(self, *args, **kwargs):
        # print('---------leaveEvent of %s starts---------' % self.__class__)
        self.reminder_unselecting.emit(self.last_mouse_enter_index)
        # print('---------leaveEvent of %s ends---------' % self.__class__)


class MyWindow(QFrame):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.layout_init()
        self.layout_manage()

    def layout_init(self):
        self.setFixedSize(800, 600)
        #
        self.button01 = QPushButton('add row', self)
        self.button01.setFixedSize(100, 100)
        self.button01.clicked.connect(self.clicked2adding_new_row)
        #
        self.table_view01 = Label_List_Widget01(parent=self)

    def layout_manage(self):
        self.table_view01.move(0, 0)
        width_table_view = self.table_view01.width()
        self.button01.move(width_table_view, 0)

    def clicked2adding_new_row(self):
        self.table_view01.table_model.adding_new_row()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())

