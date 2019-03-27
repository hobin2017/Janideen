# -*- coding: utf-8 -*-
"""

"""

import sys

import os
from PyQt5.QtCore import Qt, pyqtSignal, QFile
from PyQt5.QtWidgets import QApplication, QFrame, QDialog, QCheckBox, QLabel, QLineEdit, QSizePolicy, QHBoxLayout, \
    QPushButton, QFileDialog, QVBoxLayout

from LoggingModule import MyLogging1_2


class FileOperation_Reminder01(QDialog):
    updating4img_list = pyqtSignal()
    deleting4current_labels = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('File Operation')
        #
        self.layout_init()
        self.layout_manage()
        # others
        self.dest_dir4xml = ''
        self.dest_dir4img = ''
        self.mylogging4file_op_reminder01 = MyLogging1_2(logger_name='hobin')

    def layout_init(self):
        self.setFixedSize(600, 300)
        # a group for current image
        height4current_img = 40
        self.text4current_img = QLabel('Curr_img')
        self.text4current_img.setFixedSize(100, height4current_img)
        #
        self.editor4current_img = QLineEdit()
        self.editor4current_img.setReadOnly(True)
        self.editor4current_img.setFixedHeight(height4current_img)
        #
        self.button4current_img = QPushButton('open')
        self.button4current_img.setFixedSize(100, height4current_img)
        self.button4current_img.clicked.connect(self.onclick4current_img)

        # a group for directory about current xml
        height4current_xml = 40
        self.text4current_xml = QLabel('Curr_xml')
        self.text4current_xml.setFixedSize(100, height4current_xml)
        #
        self.editor4current_xml = QLineEdit()
        self.editor4current_xml.setReadOnly(True)
        self.editor4current_xml.setFixedHeight(height4current_xml)
        #
        self.button4current_xml = QPushButton('open')
        self.button4current_xml.setFixedSize(100, height4current_xml)
        self.button4current_xml.clicked.connect(self.onclick4current_xml)

        # a group for directory about xml
        height_dir4xml = 40
        self.text_dir4xml = QLabel('Dest_dir4xml')
        self.text_dir4xml.setFixedSize(100, height_dir4xml)
        #
        self.editor_dir4xml = QLineEdit()
        self.editor_dir4xml.setFixedHeight(height_dir4xml)
        #
        self.button_dir4xml = QPushButton('open')
        self.button_dir4xml.setFixedSize(100, height_dir4xml)
        self.button_dir4xml.clicked.connect(self.onclick_dir4xml)

        # a group for directory about image
        height_dir4img = 40
        self.text_dir4img = QLabel('Dest_dir4img')
        self.text_dir4img.setFixedSize(100, height_dir4img)
        #
        self.editor_dir4img = QLineEdit()
        self.editor_dir4img.setFixedHeight(height_dir4img)
        #
        self.button_dir4img = QPushButton('open')
        self.button_dir4img.setFixedSize(100, height_dir4img)
        self.button_dir4img.clicked.connect(self.onclick_dir4img)

        # a group of checkboxes about mode
        self.rect_widget01 = QLabel('Mode')
        self.rect_widget01.setFixedSize(100, 150)
        self.rect_widget01.setAlignment(Qt.AlignTop)
        self.rect_widget01.setStyleSheet('''
                    font-size:20px; 
                    background: white;
                    margin-top:0px;
                    margin-right:0px;
                    margin-bottom:0px;
                    margin-left:0px;
                    ''')
        #
        self.checkbox_mode_del = QCheckBox('delete', self.rect_widget01)
        self.checkbox_mode_del.setFixedSize(100, 50)
        self.checkbox_mode_del.setCheckState(Qt.Checked)
        #
        self.checkbox_mode_copy = QCheckBox('copy', self.rect_widget01)
        self.checkbox_mode_copy.setFixedSize(100, 50)
        self.checkbox_mode_copy.setCheckState(Qt.Checked)

        # a group of checkboxes about target
        self.rect_widget02 = QLabel('Target')
        self.rect_widget02.setFixedSize(100, 150)
        self.rect_widget02.setAlignment(Qt.AlignTop)
        self.rect_widget02.setStyleSheet('''
                    font-size: 20px; 
                    background: white;
                    margin-top:0px;
                    margin-right:0px;
                    margin-bottom:0px;
                    margin-left:0px;
                    ''')
        #
        self.checkbox_target_img = QCheckBox('image', self.rect_widget02)
        self.checkbox_target_img.setFixedSize(100, 50)
        self.checkbox_target_img.setCheckState(Qt.Checked)
        #
        self.checkbox_target_xml = QCheckBox('xml', self.rect_widget02)
        self.checkbox_target_xml.setFixedSize(100, 50)
        self.checkbox_target_xml.setCheckState(Qt.Checked)

        self.button_ok = QPushButton('OK')
        self.button_ok.setFixedSize(100, 50)
        self.button_ok.clicked.connect(self.onclick_ok_button)

        self.button_cancel = QPushButton('Cancel')
        self.button_cancel.setFixedSize(100, 50)
        self.button_cancel.clicked.connect(self.onclick_cancel_button)

    def layout_manage(self):
        #
        self.checkbox_mode_del.move(0, 20)
        self.checkbox_mode_copy.move(0, 70)
        self.checkbox_target_img.move(0, 20)
        self.checkbox_target_xml.move(0, 70)
        #
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # sub-layout -1
        self.sub_layout4current_img_editor = QHBoxLayout()
        self.sub_layout4current_img_editor.setSpacing(0)
        self.sub_layout4current_img_editor.setContentsMargins(0, 0, 0, 0)
        self.sub_layout4current_img_editor.addWidget(self.text4current_img)
        self.editor4current_img.setMaximumSize(10000, 10000)
        self.editor4current_img.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sub_layout4current_img_editor.addWidget(self.editor4current_img)
        self.sub_layout4current_img_editor.addWidget(self.button4current_img)
        self.main_layout.addLayout(self.sub_layout4current_img_editor)

        # sub0layout 0
        self.sub_layout4current_xml_editor = QHBoxLayout()
        self.sub_layout4current_xml_editor.setSpacing(0)
        self.sub_layout4current_xml_editor.setContentsMargins(0, 0, 0, 0)
        self.sub_layout4current_xml_editor.addWidget(self.text4current_xml)
        self.editor4current_xml.setMaximumSize(10000, 10000)
        self.editor4current_xml.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sub_layout4current_xml_editor.addWidget(self.editor4current_xml)
        self.sub_layout4current_xml_editor.addWidget(self.button4current_xml)
        self.main_layout.addLayout(self.sub_layout4current_xml_editor)

        # sub-layout 1
        self.sub_layout4xml_editor = QHBoxLayout()
        self.sub_layout4xml_editor.setSpacing(0)
        self.sub_layout4xml_editor.setContentsMargins(0, 0, 0, 0)
        self.sub_layout4xml_editor.addWidget(self.text_dir4xml)
        self.editor_dir4xml.setMaximumSize(10000, 10000)
        self.editor_dir4xml.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sub_layout4xml_editor.addWidget(self.editor_dir4xml)
        self.sub_layout4xml_editor.addWidget(self.button_dir4xml)
        self.main_layout.addLayout(self.sub_layout4xml_editor)
        # sub-layout 2
        self.sub_layout4img_editor = QHBoxLayout()
        self.sub_layout4img_editor.setSpacing(0)
        self.sub_layout4img_editor.setContentsMargins(0, 0, 0, 0)
        self.sub_layout4img_editor.addWidget(self.text_dir4img)
        self.editor_dir4img.setMaximumSize(10000, 10000)
        self.editor_dir4img.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sub_layout4img_editor.addWidget(self.editor_dir4img)
        self.sub_layout4img_editor.addWidget(self.button_dir4img)
        self.main_layout.addLayout(self.sub_layout4img_editor)
        # sub-layout 3
        self.sub_layout4options = QHBoxLayout()
        self.sub_layout4options.setSpacing(0)
        self.sub_layout4options.setContentsMargins(0, 0, 0, 0)
        self.sub_layout4options.addWidget(self.rect_widget01)
        self.sub_layout4options.addWidget(self.rect_widget02)
        invisible_widget01 = QLabel()
        invisible_widget01.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sub_layout4options.addWidget(invisible_widget01)
        self.sub_layout4options.addWidget(self.button_ok)
        self.sub_layout4options.addWidget(self.button_cancel)
        self.main_layout.addLayout(self.sub_layout4options)

    def onclick_dir4xml(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick_dir4xml of %s starts---------' % self.__class__)
        default_dir = self.dest_dir4xml
        user_selected_dir = QFileDialog.getExistingDirectory(parent=self, caption='Choosing xml directory',
                                                             directory=default_dir,
                                                             options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
                                                             )  # str

        if user_selected_dir:
            self.mylogging4file_op_reminder01.logger.info('selected dir with type %s: %s'
                                                          % (type(user_selected_dir), user_selected_dir))
            self.dest_dir4xml = user_selected_dir
            self.editor_dir4xml.setText(self.dest_dir4xml)
        else:
            self.mylogging4file_op_reminder01.logger.info('selected dir with type %s: %s'
                                                          % (type(user_selected_dir), user_selected_dir))
        self.mylogging4file_op_reminder01.logger.info('---------onclick_dir4xml of %s ends---------' % self.__class__)

    def onclick_dir4img(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick_dir4img of %s starts---------' % self.__class__)
        default_dir = self.dest_dir4img
        user_selected_dir = QFileDialog.getExistingDirectory(parent=self, caption='Choosing image directory',
                                                             directory=default_dir,
                                                             options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
                                                             )  # str

        if user_selected_dir:
            self.mylogging4file_op_reminder01.logger.info('selected dir with type %s: %s'
                                                          % (type(user_selected_dir), user_selected_dir))
            self.dest_dir4img = user_selected_dir
            self.editor_dir4img.setText(self.dest_dir4img)
        else:
            self.mylogging4file_op_reminder01.logger.info('selected dir with type %s: %s'
                                                          % (type(user_selected_dir), user_selected_dir))
        self.mylogging4file_op_reminder01.logger.info('---------onclick_dir4img of %s ends---------' % self.__class__)

    def onclick4current_img(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick4current_img of %s starts---------' % self.__class__)
        default_dir = ''
        user_selected_image, filter_text = QFileDialog.getOpenFileName(parent=self, caption='Choosing current image',
                                                        directory=default_dir,
                                                        filter='Images (*.png *.jpg);;All Files(*)'
                                                        )  # str

        if user_selected_image:
            self.mylogging4file_op_reminder01.logger.info('selected image with type %s: %s'
                                                          % (type(user_selected_image), user_selected_image))
            self.editor4current_img.setText(user_selected_image)
        else:
            self.mylogging4file_op_reminder01.logger.info('selected image with type %s: %s'
                                                          % (type(user_selected_image), user_selected_image))
        self.mylogging4file_op_reminder01.logger.info('---------onclick4current_img of %s ends---------' % self.__class__)

    def onclick4current_xml(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick4current_xml of %s starts---------'% self.__class__)
        default_dir = ''
        user_selected_xml, filter_text = QFileDialog.getOpenFileName(parent=self, caption='Choosing current xml',
                                                                     directory=default_dir,
                                                                     filter='XML (*.xml);;All Files(*)'
                                                                     )  # str

        if user_selected_xml:
            self.mylogging4file_op_reminder01.logger.info('selected image with type %s: %s'
                                                          % (type(user_selected_xml), user_selected_xml))
            self.editor4current_xml.setText(user_selected_xml)
        else:
            self.mylogging4file_op_reminder01.logger.info('selected image with type %s: %s'
                                                          % (type(user_selected_xml), user_selected_xml))
        self.mylogging4file_op_reminder01.logger.info('---------onclick4current_xml of %s ends---------'% self.__class__)
    
    def onclick_ok_button(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick_ok_button of %s starts---------' % self.__class__)
        checkbox4target_xml_status = True if self.checkbox_target_xml.checkState() == Qt.Checked else False
        checkbox4target_img_status = True if self.checkbox_target_img.checkState() == Qt.Checked else False
        checkbox4mode_del_status = True if self.checkbox_mode_del.checkState() == Qt.Checked else False
        checkbox4mode_copy_status = True if self.checkbox_mode_copy.checkState() == Qt.Checked else False
        if checkbox4target_img_status:
            if checkbox4mode_copy_status:
                # self.mylogging4file_op_reminder01.logger.info('try to copy the image')
                self.copying_image()
            # other operations should be performed before deleting
            if checkbox4mode_del_status:
                # self.mylogging4file_op_reminder01.logger.info('try to delete the image')
                self.deleting_image()
        if checkbox4target_xml_status:
            if checkbox4mode_copy_status:
                # self.mylogging4file_op_reminder01.logger.info('try to copy the xml')
                self.copying_xml()
            # other operations should be performed before deleting
            if checkbox4mode_del_status:
                # self.mylogging4file_op_reminder01.logger.info('try to delete the xml')
                self.deleting_xml(delete_img_flag=checkbox4target_img_status and checkbox4mode_del_status)
        self.done(QDialog.Accepted)  # The value of the parameter will appear if using QDialog.exec()
        self.mylogging4file_op_reminder01.logger.info('---------onclick_ok_button of %s ends---------' % self.__class__)
    
    def onclick_cancel_button(self):
        self.mylogging4file_op_reminder01.logger.info('---------onclick_cancel_button of %s starts---------' % self.__class__)
        self.done(QDialog.Rejected)  # The value of the parameter will appear if using QDialog.exec()
        self.mylogging4file_op_reminder01.logger.info('---------onclick_cancel_button of %s ends---------' % self.__class__)

    def updating_text4current_img_editor(self, new_img_path):
        """
          Currently, this function is called manually before showing this dialog.
        """
        self.editor4current_img.setText(str(new_img_path))

    def updating_text4current_xml_editor(self, new_xml_path):
        """
          Currently, this function is called manually before showing this dialog.
        """
        self.editor4current_xml.setText(str(new_xml_path))

    def copying_image(self):
        self.mylogging4file_op_reminder01.logger.info('------copying_image of %s starts------' % self.__class__)
        source_img_path = self.editor4current_img.text()
        # checking for source file
        if not (os.path.isfile(source_img_path) and os.path.exists(source_img_path)):
            self.mylogging4file_op_reminder01.logger.info('the source of image path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------copying_image of %s ends------' % self.__class__)
            return

        # checking for destination directory
        destination_dir = self.editor_dir4img.text()
        if not (os.path.isdir(destination_dir) and os.path.exists(destination_dir)):
            self.mylogging4file_op_reminder01.logger.info('the destination of image path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------copying_image of %s ends------' % self.__class__)
            return

        # start to copy image
        destination_img_path = self.editor_dir4img.text() + '/' + os.path.split(source_img_path)[1]
        qfile_src_img = QFile(source_img_path)
        op_copy_result = qfile_src_img.copy(destination_img_path)
        if op_copy_result:
            self.mylogging4file_op_reminder01.logger.info('copy successfully')
            # recording for further use
            self.mylogging4file_op_reminder01.logger.info(
                'recording: copy, %s, %s' % (source_img_path, destination_img_path)
            )
        else:
            # the file already exists
            self.mylogging4file_op_reminder01.logger.info('copy fails')

        self.mylogging4file_op_reminder01.logger.info('------copying_image of %s ends------' % self.__class__)

    def deleting_image(self):
        self.mylogging4file_op_reminder01.logger.info('------deleting_image of %s starts------' % self.__class__)
        source_img_path = self.editor4current_img.text()
        # checking for source file
        if not (os.path.isfile(source_img_path) and os.path.exists(source_img_path)):
            self.mylogging4file_op_reminder01.logger.info('the source of image path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------deleting_image of %s ends------' % self.__class__)
            return

        # start to delete image
        qfile_src_img = QFile(source_img_path)
        op_del_result = qfile_src_img.remove()
        if op_del_result:
            self.mylogging4file_op_reminder01.logger.info('delete successfully')
            # recording for further use
            self.mylogging4file_op_reminder01.logger.info(
                'recording: del, %s' % (source_img_path)
            )
            # others
            self.updating4img_list.emit()
        else:
            # file may be opened when deleting
            self.mylogging4file_op_reminder01.logger.info('delete fails')

        self.mylogging4file_op_reminder01.logger.info('------deleting_image of %s ends------' % self.__class__)

    def copying_xml(self):
        self.mylogging4file_op_reminder01.logger.info('------copying_xml of %s starts------' % self.__class__)
        source_xml_path = self.editor4current_xml.text()
        # checking for source file
        if not (os.path.isfile(source_xml_path) and os.path.exists(source_xml_path)):
            self.mylogging4file_op_reminder01.logger.info('the source of xml path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------copying_xml of %s ends------' % self.__class__)
            return

        # checking for destination directory
        destination_dir = self.editor_dir4xml.text()
        if not (os.path.isdir(destination_dir) and os.path.exists(destination_dir)):
            self.mylogging4file_op_reminder01.logger.info('the destination of xml path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------copying_xml of %s ends------' % self.__class__)
            return

        # start to copy xml
        destination_xml_path = self.editor_dir4xml.text() + '/' + os.path.split(source_xml_path)[1]
        qfile_src_xml = QFile(source_xml_path)
        op_copy_result = qfile_src_xml.copy(destination_xml_path)
        if op_copy_result:
            self.mylogging4file_op_reminder01.logger.info('copy successfully')
            # recording for further use
            self.mylogging4file_op_reminder01.logger.info(
                'recording: copy, %s, %s' % (source_xml_path, destination_xml_path)
            )
        else:
            # the file already exists
            self.mylogging4file_op_reminder01.logger.info('copy fails')

        self.mylogging4file_op_reminder01.logger.info('------copying_xml of %s ends------' % self.__class__)

    def deleting_xml(self, delete_img_flag):
        self.mylogging4file_op_reminder01.logger.info('------deleting_xml of %s starts------' % self.__class__)
        source_xml_path = self.editor4current_xml.text()
        # checking for source file
        if not (os.path.isfile(source_xml_path) and os.path.exists(source_xml_path)):
            self.mylogging4file_op_reminder01.logger.info('the source of xml path goes wrong')
            self.mylogging4file_op_reminder01.logger.info('------deleting_xml of %s ends------' % self.__class__)
            return

        # start to delete xml
        qfile_src_xml = QFile(source_xml_path)
        op_del_result = qfile_src_xml.remove()
        if op_del_result:
            if not delete_img_flag: self.deleting4current_labels.emit()
            self.mylogging4file_op_reminder01.logger.info('delete successfully')
            # recording for further use
            self.mylogging4file_op_reminder01.logger.info(
                'recording: del, %s' % (source_xml_path)
            )
        else:
            # file may be opened when deleting
            self.mylogging4file_op_reminder01.logger.info('delete fails')

        self.mylogging4file_op_reminder01.logger.info('------deleting_xml of %s ends------' % self.__class__)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = FileOperation_Reminder01()
    mywindow.show()
    sys.exit(app.exec_())

