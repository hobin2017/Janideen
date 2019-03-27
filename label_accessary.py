# -*- coding: utf-8 -*-
"""

"""
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QLineEdit, QApplication, QLabel, QTableView, QHeaderView, QPushButton, QCheckBox

from LoggingModule import MyLogging1_2


class LabelNameItem01(QStandardItem):

    def __init__(self, text='hobin', parent=None):
        super().__init__(parent)
        self.setEditable(False)
        #
        self.init_text = text
        self.setText(self.init_text)


class HistoryView01(QTableView):
    choosing_string = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # every column do the stretching
        self.setModel(QStandardItemModel())
        #
        self.doubleClicked.connect(self.onclick_tableview)
        #
        self.history_record = set()
        self.refreshing_view()


    def refreshing_view(self, total_column=6):
        print('---------refreshing_view of %s starts---------' % self.__class__)
        self.model().clear()
        #
        max_column_count = total_column
        for index, item_string in enumerate(self.history_record):
            new_item = LabelNameItem01(text=item_string)
            row_index = index // max_column_count
            column_index = index % max_column_count
            self.model().setItem(row_index, column_index, new_item)
        print('---------refreshing_view of %s ends---------' % self.__class__)

    def updating_view(self, new_text, total_column=6):
        print('---------updating_view of %s starts---------' % self.__class__)
        max_column_count = total_column
        temp_last_index = len(self.history_record) - 1
        row_index = temp_last_index // max_column_count
        column_index = temp_last_index % max_column_count
        new_item = LabelNameItem01(text=new_text)
        self.model().setItem(row_index, column_index, new_item)
        print('---------updating_view of %s ends---------' % self.__class__)

    def onclick_tableview(self, qmodel_index):
        self.choosing_string.emit(str(qmodel_index.data()))


class HistoryView02(QTableView):
    """
      Compared with HistoryView01, the logging module is first introduced to this class
    """
    choosing_string = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mylogging4history_view02 = MyLogging1_2(logger_name='hobin')
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # every column do the stretching
        self.setModel(QStandardItemModel())
        #
        self.doubleClicked.connect(self.onclick_tableview)
        #
        self.history_record = set()
        self.refreshing_view()


    def refreshing_view(self, total_column=6):
        self.mylogging4history_view02.logger.info('---------refreshing_view of %s starts---------' % self.__class__)
        self.model().clear()
        #
        max_column_count = total_column
        for index, item_string in enumerate(self.history_record):
            new_item = LabelNameItem01(text=item_string)
            row_index = index // max_column_count
            column_index = index % max_column_count
            self.model().setItem(row_index, column_index, new_item)
        self.mylogging4history_view02.logger.info('---------refreshing_view of %s ends---------' % self.__class__)

    def updating_view(self, new_text, total_column=6):
        self.mylogging4history_view02.logger.info('---------updating_view of %s starts---------' % self.__class__)
        max_column_count = total_column
        temp_last_index = len(self.history_record) - 1
        row_index = temp_last_index // max_column_count
        column_index = temp_last_index % max_column_count
        new_item = LabelNameItem01(text=new_text)
        self.model().setItem(row_index, column_index, new_item)
        self.mylogging4history_view02.logger.info('---------updating_view of %s ends---------' % self.__class__)

    def onclick_tableview(self, qmodel_index):
        self.choosing_string.emit(str(qmodel_index.data()))


class Label_Editing_Dialog01(QDialog):

    def __init__(self, parent=None, width=800, height=600):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.layout_init()
        self.layout_manage()
        # others
        self.id4object01 = None  # pointer to object when showing the QDialog


    def layout_init(self):
        self.setFixedSize(self.width, self.height)
        #
        self.label_name01 = QLabel('label', self)
        self.label_name01.setAlignment(Qt.AlignCenter)
        self.label_name01.setFixedSize(50, 50)
        #
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(self.width - self.label_name01.width(), 50)
        #
        self.history_view = HistoryView01(parent=self)
        self.history_view.setFixedSize(self.width, 450)
        self.history_view.choosing_string.connect(self.changing_editer)
        #
        self.label_name02 = QLabel('label history:', self)
        self.label_name02.setFixedSize(200, 50)
        #
        self.button_confirm = QPushButton('OK', self)
        self.button_confirm.setFixedSize(100, 50)
        self.button_confirm.clicked.connect(self.onclick_button_confirm)
        #
        self.button_cancel = QPushButton('Cancel', self)
        self.button_cancel.setFixedSize(100, 50)
        self.button_cancel.clicked.connect(self.onclick_button_cancel)

    def layout_manage(self):
        self.label_name01.move(0, 0)
        self.line_edit.move(self.label_name01.width(), 0)
        self.label_name02.move(0, self.label_name01.height())
        self.history_view.move(0, self.label_name01.height() + self.label_name02.height())
        self.button_cancel.move(self.width - self.button_cancel.width(), self.height-self.button_cancel.height())
        self.button_confirm.move(self.button_cancel.x()-self.button_confirm.width(), self.height-self.button_confirm.height())

    def changing_editer(self, string):
        """
        The 'choosing_string' signal will cause this function executed.
        :param string:
        :return:
        """
        self.line_edit.setText(string)

    def onclick_button_confirm(self):
        print('---------onclick_button_confirm of %s starts---------' % self.__class__)
        temp_text = str(self.line_edit.text())
        print('current text: %s' %temp_text)
        if self.id4object01:
            self.id4object01.text4cv_id = temp_text  # storing it in the 'PicWidget_Label02' object (target object)
            print('text of target object: %s' %self.id4object01.text4cv_id)
            # updating the history view
            if temp_text in self.history_view.history_record:
                print('the text already exists')
            else:
                print('the text is new')
                self.history_view.history_record.add(temp_text)
                self.history_view.updating_view(new_text=temp_text)
        else:
            print('error happens: no corresponding object for storing the text')
        # end
        self.id4object01 = None
        self.done(QDialog.Accepted)  # The value of the parameter will appear if using QDialog.exec()
        print('---------onclick_button_confirm of %s ends---------' % self.__class__)

    def onclick_button_cancel(self):
        print('---------onclick_button_cancel of %s starts---------' % self.__class__)
        self.done(QDialog.Rejected)  # The value of the parameter will appear if using QDialog.exec()
        print('---------onclick_button_cancel of %s ends---------' % self.__class__)


class Label_Editing_Dialog02(QDialog):
    """
      Compared with Label_Editing_Dialog01, this class introduces two signals 'new_accepted_text' and
    'changing_label_color' to change cv_id information and the rectangle color (QGraphicsItem).
      Compared with Label_Editing_Dialog01, the logging module is first introduced to this class.
    """
    new_accepted_text = pyqtSignal(object, object, object)  # op_code, label_id, cv_id
    changing_label_color = pyqtSignal(object)  # 'QGraphicsItem' class
    using_default_name_mode = pyqtSignal(object)

    def __init__(self, parent=None, width=800, height=600):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.layout_init()
        self.layout_manage()
        # others
        self.id4object01 = None  # pointer to object when showing the QDialog
        self.mylogging4label_editing_dialog02 = MyLogging1_2()

    def layout_init(self):
        self.setFixedSize(self.width, self.height)
        #
        self.label_name01 = QLabel('label', self)
        self.label_name01.setAlignment(Qt.AlignCenter)
        self.label_name01.setFixedSize(50, 50)
        #
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(self.width - self.label_name01.width(), 50)
        #
        self.history_view = HistoryView02(parent=self)
        self.history_view.setFixedSize(self.width, 450)
        self.history_view.choosing_string.connect(self.changing_editer)
        #
        self.label_name02 = QLabel('label history:', self)
        self.label_name02.setFixedSize(200, 50)
        #
        self.checkbox4default_name = QCheckBox('default cv_id for next item', self)
        self.checkbox4default_name.setCheckState(Qt.Unchecked)
        #
        self.button_confirm = QPushButton('OK', self)
        self.button_confirm.setFixedSize(100, 50)
        self.button_confirm.clicked.connect(self.onclick_button_confirm)
        #
        self.button_cancel = QPushButton('Cancel', self)
        self.button_cancel.setFixedSize(100, 50)
        self.button_cancel.clicked.connect(self.onclick_button_cancel)

    def layout_manage(self):
        self.label_name01.move(0, 0)
        self.line_edit.move(self.label_name01.width(), 0)
        self.checkbox4default_name.move(0, self.label_name01.height())
        self.label_name02.move(0, self.label_name01.height() + self.checkbox4default_name.height())
        self.history_view.move(0, self.label_name02.y() + self.label_name02.height())
        self.button_cancel.move(self.width - self.button_cancel.width(), self.height - self.button_cancel.height())
        self.button_confirm.move(self.button_cancel.x() - self.button_confirm.width(),
                                 self.height - self.button_confirm.height())

    def changing_editer(self, string):
        """
        The 'choosing_string' signal will cause this function executed.
        :param string:
        :return:
        """
        self.line_edit.setText(string)

    def onclick_button_confirm(self):
        self.mylogging4label_editing_dialog02.logger.info('---------onclick_button_confirm of %s starts---------'
                                                          % self.__class__)
        temp_text = str(self.line_edit.text())
        self.mylogging4label_editing_dialog02.logger.info('current text: %s' % temp_text)
        if self.id4object01:
            self.id4object01.text4cv_id = temp_text  # storing it in the 'PicWidget_Label02' object (target object)
            self.mylogging4label_editing_dialog02.logger.info('text of target object: %s' % self.id4object01.text4cv_id)
            # updating the history view
            if temp_text in self.history_view.history_record:
                self.mylogging4label_editing_dialog02.logger.info('the text already exists')
            else:
                self.mylogging4label_editing_dialog02.logger.info('the text is new')
                self.history_view.history_record.add(temp_text)
                self.history_view.updating_view(new_text=temp_text)

            self.new_accepted_text.emit('changing_text', self.id4object01.id_info, self.id4object01.text4cv_id)
            self.changing_label_color.emit(self.id4object01)
        else:
            self.mylogging4label_editing_dialog02.logger.info('error happens: no corresponding object for storing the text')

        checkbox_status = True if self.checkbox4default_name.checkState() == Qt.Checked else False
        self.using_default_name_mode.emit(checkbox_status)
        # end
        self.id4object01 = None
        self.done(QDialog.Accepted)  # The value of the parameter will appear if using QDialog.exec()
        self.mylogging4label_editing_dialog02.logger.info('---------onclick_button_confirm of %s ends---------'
                                                          % self.__class__)

    def onclick_button_cancel(self):
        # self.mylogging4label_editing_dialog02.logger.info('---------onclick_button_cancel of %s starts---------' % self.__class__)
        self.done(QDialog.Rejected)  # The value of the parameter will appear if using QDialog.exec()
        # self.mylogging4label_editing_dialog02.logger.info('---------onclick_button_cancel of %s ends---------' % self.__class__)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Label_Editing_Dialog02()
    mywindow.show()
    sys.exit(app.exec_())

