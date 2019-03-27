# -*- coding: utf-8 -*-
"""
Originally, Janideen is designed to help ML learners label their images.
"""
import copy
import os
import sys
from datetime import datetime
from xml.etree import ElementTree

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsView, QFrame, QPushButton, QFileDialog, QSizePolicy, QVBoxLayout, \
    QHBoxLayout, QLabel

from LoggingModule import MyLogging1_2
from color_table import ColorMapper01
from data4label import ObjectElement01
from label_list_widget import Label_List_Widget01
from picture_widget import PicScene02
from reminder_widget import FileOperation_Reminder01


class MyWindow(QFrame):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Janideen')
        icon_path = r'./images/whiteHand.png'
        if os.path.exists(icon_path): self.setWindowIcon(QIcon(icon_path))
        self.mylogging = MyLogging1_2(logger_name='hobin')
        #
        self.dir4reading_xml = os.path.abspath('.')
        self.dir4writing_xml = self.dir4reading_xml
        self.dir4reading_img = os.path.abspath('.')
        self.current_img_path = r'.'  # used by QPixmap class

        #
        self.layout_init()
        self.layout_manage()

        #others
        self.color_mapper = ColorMapper01()

        # pre-work
        # self.updating_img_path_list()
        # self.loading_xml4current_pic02()

    def layout_init(self):
        # picture widget
        self.scene4picture = PicScene02(img_path=r'.', parent=self)
        self.scene4picture.label_notification_signal.connect(self.updating4label_view)
        self.scene4picture.changing_label_color.connect(self.changing_label_color4scene)
        self.scene4picture.selecting_next_img.connect(self.reloading_next_img02)
        self.scene4picture.selecting_previous_img.connect(self.reloading_previous_img02)

        #
        self.pic_view = QGraphicsView(self)
        self.pic_view.setFixedSize(1000, 860)  # w/h = 1.25 by default
        self.pic_view.setScene(self.scene4picture)

        #
        self.label_view01 = Label_List_Widget01(parent=self, width=300, height=860)
        self.label_view01.reminder_selecting.connect(self.label_view2scene_selecting)
        self.label_view01.reminder_unselecting.connect(self.label_view2scene_unselecting)

        #
        self.button_img_dir = QPushButton('img dir', self)
        self.button_img_dir.setFixedSize(100, 100)
        self.button_img_dir.clicked.connect(self.getting_img_dir)

        #
        self.button_xml_dir = QPushButton('xml dir', self)
        self.button_xml_dir.setFixedSize(100, 100)
        self.button_xml_dir.clicked.connect(self.getting_xml_dir)

        #
        self.button_next_img = QPushButton('next', self)
        self.button_next_img.setFixedSize(100, 100)
        self.button_next_img.clicked.connect(self.reloading_next_img02)

        #
        self.button_previous_img = QPushButton('previous', self)
        self.button_previous_img.setFixedSize(100, 100)
        self.button_previous_img.clicked.connect(self.reloading_previous_img02)

        self.button_writing_xml = QPushButton('write xml', self)
        self.button_writing_xml.setFixedSize(100, 100)
        self.button_writing_xml.clicked.connect(self.output_xml4current_pic02)

        #
        self.reminder4file_operation = FileOperation_Reminder01(parent=None)
        self.reminder4file_operation.updating4img_list.connect(self.updating_img_list41file_operation_reminder)
        self.reminder4file_operation.deleting4current_labels.connect(self.deleting_current_labels41file_operation_reminder)

    def layout_manage(self):
        # first column of the main layout
        self.sub_layout4buttons = QVBoxLayout()
        self.button_img_dir.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sub_layout4buttons.addWidget(self.button_img_dir)
        self.button_xml_dir.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sub_layout4buttons.addWidget(self.button_xml_dir)
        self.button_previous_img.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sub_layout4buttons.addWidget(self.button_previous_img)
        self.button_next_img.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sub_layout4buttons.addWidget(self.button_next_img)
        self.button_writing_xml.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sub_layout4buttons.addWidget(self.button_writing_xml)
        invisible_label = QLabel()
        invisible_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.sub_layout4buttons.addWidget(invisible_label)

        # main layout
        self.main_layout4labelling = QHBoxLayout()
        self.main_layout4labelling.setSpacing(0)  # the space between two widgets
        self.main_layout4labelling.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout4labelling)
        self.main_layout4labelling.addLayout(self.sub_layout4buttons)
        self.pic_view.setMaximumSize(10000, 10000)  # QWidget.setFixedSize() will affect its maximum size
        self.pic_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout4labelling.addWidget(self.pic_view)
        self.label_view01.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.label_view01.setMaximumSize(10000, 10000)  # QWidget.setFixedSize() will affect its maximum size
        self.main_layout4labelling.addWidget(self.label_view01)

        # temp code for testing
        # self.button01 = QPushButton('test', self)
        # self.button01.clicked.connect(lambda : print(self.sub_layout4buttons.spacing()))
        # self.sub_layout4buttons.addWidget(self.button01)

    def img_path2xml_name(self, img_path):
        img_dir, img_name = os.path.split(img_path)
        xml_name = os.path.splitext(img_name)[0] + r'.xml'
        return xml_name

    def updating_img_path_list(self):
        self.mylogging.logger.info('------------------updating_img_path_list starts-----------------------------')
        if not os.path.isdir(self.dir4reading_img):
            self.mylogging.logger.error('invalid path in updating_img_path_list')
            return
        img_name_list = [x for x in os.listdir(self.dir4reading_img) if x.endswith('.jpg')]
        self.mylogging.logger.info('%s dirctory has total %s images: %s'
                                   %(self.dir4reading_img, len(img_name_list), img_name_list))
        self.index4img_path_list = 0
        if img_name_list:
            self.img_path_list = []
            for img_name in img_name_list:
                self.img_path_list.append(os.path.join(self.dir4reading_img, img_name))
            self.current_img_path = self.img_path_list[self.index4img_path_list]
        else:
            self.current_img_path = r'.'
        self.mylogging.logger.info('current image path: %s' %self.current_img_path)
        self.mylogging.logger.info('------------------updating_img_path_list ends-----------------------------')

    def getting_img_dir(self):
        self.mylogging.logger.info('------------------getting_img_dir starts-----------------------------')
        default_dir = self.dir4reading_img
        user_selected_dir = QFileDialog.getExistingDirectory(parent=self, caption='Choosing for image directory',
                                                        directory=default_dir,
                                                        options=QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks,
                                                        ) # str

        if user_selected_dir:
            self.mylogging.logger.info('selected dir with type %s: %s' % (type(user_selected_dir), user_selected_dir))
            self.dir4reading_img = user_selected_dir
            self.updating_img_path_list()
            self.reloading_current_img01()
        else:
            self.mylogging.logger.info('selected dir with type %s: %s' % (type(user_selected_dir), user_selected_dir))
        self.mylogging.logger.info('------------------getting_img_dir ends-----------------------------')

    def getting_xml_dir(self):
        self.mylogging.logger.info('------------------getting_xml_dir starts-----------------------------')
        default_dir = self.dir4reading_xml
        user_selected_dir = QFileDialog.getExistingDirectory(parent=self, caption='Choosing for xml directory',
                                                             directory=default_dir,
                                                             options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
                                                             )  # str

        if user_selected_dir:
            self.mylogging.logger.info('selected dir with type %s: %s' % (type(user_selected_dir), user_selected_dir))
            self.dir4reading_xml = user_selected_dir
            self.dir4writing_xml = user_selected_dir
            self.reloading_current_img01()
        else:
            self.mylogging.logger.info('selected dir with type %s: %s' % (type(user_selected_dir), user_selected_dir))
        self.mylogging.logger.info('------------------getting_xml_dir ends-----------------------------')

    def output_xml4current_pic02(self):
        """
        creating the complete xml and write them into a file
        :return:
        """
        self.mylogging.logger.info('------------------output_xml4current_pic02 starts-----------------------------')
        # check the current image path
        if os.path.exists(self.current_img_path) and os.path.isfile(self.current_img_path):
            pass
        else:
            self.mylogging.logger.info('no need to write xml since the current image path is invalid')
            self.mylogging.logger.info('------------------output_xml4current_pic02 ends-----------------------------')
            return

        #
        temp_xml = copy.deepcopy(self.scene4picture.xml_data)
        # ElementTree.dump(temp_xml)  # printing and the parameter is xml.etree.Element.Element class

        # adding 'object' tags to the xml data
        for label in self.scene4picture.labels_list:
            # label is the subclass of the QGraphicsRectItem class
            topleft = label.rect().topLeft()
            # topleft = label.mapToScene(label.rect().topLeft())  # Is this will be more safe?
            bottomright = label.rect().bottomRight()
            xmin = str(int(topleft.x()))
            ymin = str(int(topleft.y()))
            xmax = str(int(bottomright.x()))
            ymax = str(int(bottomright.y()))
            object = ObjectElement01(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, name=label.text4cv_id)
            temp_xml.append(object)

        # adding image info: width, height, depth
        for size_tag in temp_xml.findall('size'):
            width_tag = size_tag.find('width')
            if isinstance(width_tag, ElementTree.Element):
                width_tag.text = str(self.scene4picture.pic_item01.pixmap.width())

            height_tag = size_tag.find('height')
            if isinstance(height_tag, ElementTree.Element):
                height_tag.text = str(self.scene4picture.pic_item01.pixmap.height())

        # adding filename
        for filename_tag in temp_xml.findall('filename'):
            filename_tag.text = str(os.path.split(self.current_img_path)[1])

        # ElementTree.dump(temp_xml)  # printing and the parameter is xml.etree.Element.Element class

        # writing the xml data to file
        xml_path = os.path.join(self.dir4writing_xml, self.img_path2xml_name(img_path=self.current_img_path))
        tree = ElementTree.ElementTree(temp_xml)
        tree.write(xml_path)
        self.mylogging.logger.info('------------------output_xml4current_pic02 ends-----------------------------')

    def loading_xml4current_pic02(self):
        """
        reading a xml file and displaying corresponding labels on the picture
        :return:
        """
        self.mylogging.logger.info('------------------loading_xml4current_pic02 starts-----------------------------')
        # xml_path = r'./images/20190214102730.xml'
        xml_path = os.path.join(self.dir4reading_xml, self.img_path2xml_name(img_path=self.current_img_path))
        self.mylogging.logger.info('xml path for loading: %s' %xml_path)
        # protection for ElementTree.parse()
        if os.path.isfile(xml_path):
            # file exist and hence next step is reading
            self.mylogging.logger.info('The path exists: %s' % xml_path)
            tree = ElementTree.parse(xml_path)
            root = tree.getroot()
            # deleting current labels
            for list_index in range(0, len(self.scene4picture.labels_list)):
                deleted_item = self.scene4picture.labels_list.pop(list_index)
                self.scene4picture.removeItem(deleted_item)

            # adding new labels
            object_size_keyword = 'bndbox'  # it includes these tags: xmin, ymin, xmax, ymax.
            for index, object_label in enumerate(root.findall('./object')):
                timestamp = str(int(datetime.now().timestamp()))
                self.mylogging.logger.info('index %s: %s' % (index, object_label))
                # loading only complete data and abandoning the bad data
                xmin_tag = object_label.find(object_size_keyword).find('xmin')  # returns an element instance or None
                if isinstance(xmin_tag, ElementTree.Element):
                    xmin = float(xmin_tag.text)
                else:
                    self.mylogging.logger.info('detecting: no xmin tag and continue')
                    continue
                ymin_tag = object_label.find(object_size_keyword).find('ymin')
                if isinstance(ymin_tag, ElementTree.Element):
                    ymin = float(ymin_tag.text)
                else:
                    self.mylogging.logger.info('detecting: no ymin tag and continue')
                    continue
                xmax_tag = object_label.find(object_size_keyword).find('xmax')
                if isinstance(xmax_tag, ElementTree.Element):
                    xmax = float(xmax_tag.text)
                else:
                    self.mylogging.logger.info('detecting: no xmax tag and continue')
                    continue
                ymax_tag = object_label.find(object_size_keyword).find('ymax')
                if isinstance(ymax_tag, ElementTree.Element):
                    ymax = float(ymax_tag.text)
                else:
                    self.mylogging.logger.info('detecting: no ymax tag and continue')
                    continue
                self.mylogging.logger.info('xmin: %s, ymin: %s, xmax: %s, ymax:%s' % (xmin, ymin, xmax, ymax))
                name_tag = object_label.find('name')
                name_tag_text = name_tag.text if isinstance(name_tag, ElementTree.Element) else 'Janideen'
                # creating instance of corresponding class
                label_rect = QRectF(xmin, ymin, xmax - xmin, ymax - ymin)
                new_label_id = len(self.scene4picture.labels_list)
                new_label = self.scene4picture.making_new_rect_instance(
                    parent=self.scene4picture,
                    init_qrect=label_rect,
                    boundary_x=self.scene4picture.pic_item01.x(),
                    boundary_y=self.scene4picture.pic_item01.y(),
                    boundary_width=self.scene4picture.pic_item01.pixmap.width(),
                    boundary_height=self.scene4picture.pic_item01.pixmap.height(),
                    id= new_label_id
                )
                new_label.text4cv_id = name_tag_text
                self.changing_label_color4scene(new_label)

                #
                self.scene4picture.labels_list.append(new_label)
                self.scene4picture.list_id_management(op_code='insert', id=new_label_id)
                self.scene4picture.addItem(new_label)
                #
                self.updating4label_view(op_code='insert', label_id=new_label_id, cv_id=new_label.text4cv_id)

            # others
            self.label_view01.last_mouse_enter_index = 0
        else:
            self.mylogging.logger.error('The path does not exist: %s' %xml_path)
        self.mylogging.logger.info('------------------loading_xml4current_pic02 ends-----------------------------')

    def clearing_current_img(self):
        self.mylogging.logger.info('------------------clearing_current_img starts-----------------------------')
        self.scene4picture.pic_item01.reloading_img(None)
        self.scene4picture.pic_item_mask01.resetting_size(x=0, y=0, width=0, height=0)
        self.scene4picture.rect_reminder01.resetting_bounding_rect(boundary_x=0, boundary_y=0,
                                                                   boundary_widht=0, boundary_height=0)
        # visualizing the image properly
        self.pic_view.setSceneRect(self.scene4picture.pic_item_mask01.boundingRect())
        self.mylogging.logger.info('------------------clearing_current_img ends-----------------------------')

    def reloading_current_img01(self):
        self.mylogging.logger.info('------------------reloading_current_img01 starts-----------------------------')
        # deleting current labels
        self.updating4label_view(op_code='clearing', label_id=0, cv_id='')
        for list_index in range(0, len(self.scene4picture.labels_list)):
            deleted_item = self.scene4picture.labels_list[list_index]
            self.scene4picture.removeItem(deleted_item)
        self.scene4picture.labels_list = []
        self.mylogging.logger.info('successfully deleting current labels')

        # updating items for reuse purpose
        if os.path.isfile(self.current_img_path) and os.path.exists(self.current_img_path):
            self.mylogging.logger.info('current image path: %s' % self.current_img_path)
            self.scene4picture.pic_item01.reloading_img(self.current_img_path)
            self.scene4picture.pic_item_mask01.resetting_size(x=self.scene4picture.pic_item01.x(),
                                                              y=self.scene4picture.pic_item01.y(),
                                                              width=self.scene4picture.pic_item01.pixmap.width(),
                                                              height=self.scene4picture.pic_item01.pixmap.height())
            self.scene4picture.rect_reminder01.resetting_bounding_rect(boundary_x=self.scene4picture.pic_item01.x(),
                                                                       boundary_y=self.scene4picture.pic_item01.y(),
                                                                       boundary_widht=self.scene4picture.pic_item01.pixmap.width(),
                                                                       boundary_height=self.scene4picture.pic_item01.pixmap.height())
            # visualizing the image properly
            self.pic_view.setSceneRect(self.scene4picture.pic_item_mask01.boundingRect())

            # try to load corresponding xml file
            self.loading_xml4current_pic02()
        else:
            self.mylogging.logger.error('the image path does not exist in reloading_current_img01')
            self.clearing_current_img()
        self.mylogging.logger.info('------------------reloading_current_img01 ends-----------------------------')

    def reloading_next_img02(self):
        self.mylogging.logger.info('------------------reloading_next_img02 starts-----------------------------')
        self.output_xml4current_pic02()
        # deleting current labels
        self.updating4label_view(op_code='clearing', label_id=0, cv_id='')
        for list_index in range(0, len(self.scene4picture.labels_list)):
            deleted_item = self.scene4picture.labels_list[list_index]
            self.scene4picture.removeItem(deleted_item)
        self.scene4picture.labels_list = []
        self.mylogging.logger.info('successfully deleting current labels')
        #
        self.index4img_path_list = self.index4img_path_list + 1
        current_length = len(self.img_path_list)
        if self.index4img_path_list >= current_length:
            self.index4img_path_list = self.index4img_path_list - current_length
        elif self.index4img_path_list <= -current_length:
            self.index4img_path_list = self.index4img_path_list + current_length
        self.current_img_path = self.img_path_list[self.index4img_path_list]  # might raise 'index out of range' error
        self.mylogging.logger.info('current image path: %s' %self.current_img_path)

        # updating items for reuse purpose
        self.scene4picture.pic_item01.reloading_img(self.current_img_path)
        self.scene4picture.pic_item_mask01.resetting_size(x=self.scene4picture.pic_item01.x(),
                                                          y=self.scene4picture.pic_item01.y(),
                                                          width=self.scene4picture.pic_item01.pixmap.width(),
                                                          height=self.scene4picture.pic_item01.pixmap.height())
        self.scene4picture.rect_reminder01.resetting_bounding_rect(boundary_x=self.scene4picture.pic_item01.x(),
                                                                   boundary_y=self.scene4picture.pic_item01.y(),
                                                                   boundary_widht=self.scene4picture.pic_item01.pixmap.width(),
                                                                   boundary_height=self.scene4picture.pic_item01.pixmap.height())

        # visualizing the image properly
        self.pic_view.setSceneRect(self.scene4picture.pic_item_mask01.boundingRect())

        # try to load corresponding xml file
        self.loading_xml4current_pic02()
        self.mylogging.logger.info('------------------reloading_next_img02 ends-----------------------------')

    def reloading_previous_img02(self):
        self.mylogging.logger.info('------------------reloading_previous_img02 starts-----------------------------')
        self.output_xml4current_pic02()
        # deleting current labels
        self.updating4label_view(op_code='clearing', label_id=0, cv_id='')
        for list_index in range(0, len(self.scene4picture.labels_list)):
            deleted_item = self.scene4picture.labels_list[list_index]
            self.scene4picture.removeItem(deleted_item)
        self.scene4picture.labels_list = []
        self.mylogging.logger.info('successfully deleting current labels')

        #
        self.index4img_path_list = self.index4img_path_list - 1
        current_length = len(self.img_path_list)
        if self.index4img_path_list >= current_length:
            self.index4img_path_list = self.index4img_path_list - current_length
        elif self.index4img_path_list <= -current_length:
            self.index4img_path_list = self.index4img_path_list + current_length
        self.current_img_path = self.img_path_list[self.index4img_path_list]  # might raise 'index out of range' error
        self.mylogging.logger.info('current image path: %s' % self.current_img_path)

        # updating items for reuse purpose
        self.scene4picture.pic_item01.reloading_img(self.current_img_path)
        self.scene4picture.pic_item_mask01.resetting_size(x=self.scene4picture.pic_item01.x(),
                                                          y=self.scene4picture.pic_item01.y(),
                                                          width=self.scene4picture.pic_item01.pixmap.width(),
                                                          height=self.scene4picture.pic_item01.pixmap.height())
        self.scene4picture.rect_reminder01.resetting_bounding_rect(boundary_x=self.scene4picture.pic_item01.x(),
                                                                   boundary_y=self.scene4picture.pic_item01.y(),
                                                                   boundary_widht=self.scene4picture.pic_item01.pixmap.width(),
                                                                   boundary_height=self.scene4picture.pic_item01.pixmap.height())

        # visualize the image properly
        self.pic_view.setSceneRect(self.scene4picture.pic_item_mask01.boundingRect())

        # try to load corresponding xml file
        self.loading_xml4current_pic02()
        self.mylogging.logger.info('------------------reloading_previous_img02 ends-----------------------------')

    def updating4label_view(self, op_code, label_id, cv_id='', **kwargs):
        # self.mylogging.logger.info('------------------updating4label_view starts-----------------------------')
        # self.mylogging.logger.debug('operation code: %s' %op_code)
        # self.mylogging.logger.debug('label_id: %s' %label_id)
        # self.mylogging.logger.debug('cv_id: %s' %cv_id)
        if op_code == 'changing_text':
            self.label_view01.table_model.modifying_text(row_index=label_id, text=cv_id)
            self.label_view01.table_model.modifying_color(row_index=label_id, qcolor=self.color_mapper.cv_id2color(cv_id))
        elif op_code == 'insert':
            self.label_view01.table_model.adding_new_row(text=cv_id)
            self.label_view01.table_model.modifying_color(row_index=label_id, qcolor=self.color_mapper.cv_id2color(cv_id))
        elif op_code == 'delete':
            self.label_view01.table_model.deleting_current_row(row_index=label_id)
        elif op_code == 'refreshing':
            self.label_view01.table_model.refreshing()
        elif op_code == 'clearing':
            self.label_view01.table_model.removeRows(0, len(self.scene4picture.labels_list))
        # self.mylogging.logger.info('------------------updating4label_view ends-----------------------------')

    def changing_label_color4scene(self, q_graphics_item):
        self.mylogging.logger.info('------------------changing_label_color4scene starts-----------------------------')
        qcolor = self.color_mapper.cv_id2color(q_graphics_item.text4cv_id)
        q_graphics_item.updating_color(qcolor)
        self.mylogging.logger.info('------------------changing_label_color4scene starts-----------------------------')

    def label_view2scene_selecting(self, current_row_index):
        self.mylogging.logger.info('------------------label_view2scene_selecting starts-----------------------------')
        self.mylogging.logger.info('current index: %s' %current_row_index)
        label_item = self.scene4picture.labels_list[current_row_index]  # QGraphicsRectItem
        label_item.updating_brush(QBrush(QColor(48, 155, 255, 200), Qt.SolidPattern))
        self.mylogging.logger.info('------------------label_view2scene_selecting ends-----------------------------')

    def label_view2scene_unselecting(self, last_row_index):
        self.mylogging.logger.info('------------------label_view2scene_unselecting starts-----------------------------')
        self.mylogging.logger.info('last index: %s' %last_row_index)
        if self.scene4picture.labels_list[last_row_index: last_row_index + 1]:
            label_item = self.scene4picture.labels_list[last_row_index]  # QGraphicsRectItem
            label_item.updating_brush()
        else:
            self.mylogging.logger.error('error: index does not exist in label_view2scene_unselecting function')
        self.mylogging.logger.info('------------------label_view2scene_unselecting ends-----------------------------')

    def showing_file_operation_reminder(self):
        """
        Currently, this is called in of PicWidget02 class
        """
        self.mylogging.logger.info('------------------showing_file_operation_reminder starts-----------------------------')
        self.reminder4file_operation.updating_text4current_img_editor(self.current_img_path)
        xml_path = os.path.join(self.dir4reading_xml, self.img_path2xml_name(self.current_img_path))
        self.reminder4file_operation.updating_text4current_xml_editor(xml_path)
        self.reminder4file_operation.exec_()
        self.mylogging.logger.info('------------------showing_file_operation_reminder ends-----------------------------')

    def updating_img_list41file_operation_reminder(self):
        self.mylogging.logger.info('------------------updating_img_list41file_operation_reminder starts-----------------------------')
        # index management
        try:
            self.img_path_list.pop(self.index4img_path_list)
            self.current_img_path = self.img_path_list[self.index4img_path_list]
        except BaseException:
            self.mylogging.logger.info('fails to find next image path')
            self.current_img_path = r'.'

        if os.path.exists(self.current_img_path) and os.path.isfile(self.current_img_path):
            self.reloading_current_img01()
        else:
            self.updating_img_path_list()
            self.reloading_current_img01()
        self.mylogging.logger.info('------------------updating_img_list41file_operation_reminder ends-----------------------------')

    def deleting_current_labels41file_operation_reminder(self):
        self.mylogging.logger.info(
            '------------------deleting_current_labels41file_operation_reminder starts-----------------------------')
        # deleting current labels
        self.updating4label_view(op_code='clearing', label_id=0, cv_id='')
        for list_index in range(0, len(self.scene4picture.labels_list)):
            deleted_item = self.scene4picture.labels_list[list_index]
            self.scene4picture.removeItem(deleted_item)
        self.scene4picture.labels_list = []
        self.mylogging.logger.info('successfully deleting current labels')
        self.mylogging.logger.info(
            '------------------deleting_current_labels41file_operation_reminder ends-----------------------------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())

