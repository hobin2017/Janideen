# -*- coding: utf-8 -*-
"""
Originally, Janideen is designed to help ML learners label their images.
"""
import copy
import os
import sys
from datetime import datetime
from xml.etree import ElementTree

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QApplication, QGraphicsView, QFrame, QPushButton

from data4label import ObjectElement01
from picture_widget import PicScene01


class MyWindow(QFrame):

    def __init__(self):
        super().__init__()
        #
        self.dir4reading_xml = r'.'
        self.dir4writing_xml = r'.'
        self.dir4reading_img = r'.\images'
        self.updating_img_path_list()
        #
        self.layout_init()
        self.layout_manage()


    def layout_init(self):
        # picture widget
        self.scene4picture = PicScene01(img_path=self.current_img_path, parent=self)
        self.pic_view = QGraphicsView(self)
        self.pic_view.setFixedSize(1000, 860)  # w/h = 1.25 by default
        self.pic_view.setScene(self.scene4picture)

        #
        self.button01 = QPushButton('test 1', self)
        self.button01.setFixedSize(100, 100)
        self.button01.clicked.connect(self.test_work01)

        #
        self.button02 = QPushButton('write xml', self)
        self.button02.setFixedSize(100, 100)
        self.button02.clicked.connect(self.test_output_xml4current_pic)

        #
        self.button03 = QPushButton('load xml', self)
        self.button03.setFixedSize(100, 100)
        self.button03.clicked.connect(self.test_loading_xml4current_pic)

        self.button_next_img = QPushButton('next', self)
        self.button_next_img.setFixedSize(100, 100)
        self.button_next_img.clicked.connect(self.reloading_next_img)

        self.button_previous_img = QPushButton('previous', self)
        self.button_previous_img.setFixedSize(100, 100)
        self.button_previous_img.clicked.connect(self.reloading_previous_img)

    def layout_manage(self):
        self.button01.move(0, 0)
        self.button02.move(0, 100)
        self.button03.move(0, 200)
        self.button_previous_img.move(0, 300)
        self.button_next_img.move(0, 400)
        self.pic_view.move(self.button01.width(), 0)

    def img_path2xml_name(self, img_path):
        img_dir, img_name = os.path.split(img_path)
        xml_name = os.path.splitext(img_name)[0] + r'.xml'
        return xml_name

    def updating_img_path_list(self):
        img_name_list = [x for x in os.listdir(self.dir4reading_img) if x.endswith('.jpg')]
        print('%s dirctory has total %s images: %s' %(self.dir4reading_img, len(img_name_list), img_name_list))
        self.index4img_path_list = 0
        if img_name_list:
            self.img_path_list = []
            for img_name in img_name_list:
                self.img_path_list.append(os.path.join(self.dir4reading_img, img_name))
            self.current_img_path = self.img_path_list[self.index4img_path_list]
        else:
            self.current_img_path = None
        print(self.current_img_path)

    def test_work01(self):
        print(self.scene4picture.items())

    def test_output_xml4current_pic(self):
        """
        creating the complete xml and write them into a file
        :return:
        """
        print('------------------test_output_xml4current_pic starts-----------------------------')
        temp_xml = copy.copy(self.scene4picture.xml_data)
        ElementTree.dump(temp_xml)  # original one

        # adding 'object' tags to the xml data
        for key, label in self.scene4picture.labels_dict.items():
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
        ElementTree.dump(temp_xml)  # printing and the parameter is xml.etree.Element.Element class

        # writing the xml data to file
        # xml_path = r'./images/20190214102730.xml'
        xml_path = os.path.join(self.dir4writing_xml, self.img_path2xml_name(img_path=self.current_img_path))
        tree = ElementTree.ElementTree(temp_xml)
        tree.write(xml_path)
        print('------------------test_output_xml4current_pic ends-----------------------------')

    def test_loading_xml4current_pic(self):
        """
        reading a xml file and displaying corresponding labels on the picture
        :return:
        """
        print('------------------test_loading_xml4current_pic starts-----------------------------')
        # xml_path = r'./images/20190214102730.xml'
        xml_path = os.path.join(self.dir4reading_xml, self.img_path2xml_name(img_path=self.current_img_path))
        print('xml path for loading: %s' %xml_path)
        # protection for ElementTree.parse()
        if os.path.isfile(xml_path):
            # file exist and hence next step is reading
            print('The path exists: %s' % xml_path)
            tree = ElementTree.parse(xml_path)
            root = tree.getroot()
            # deleting current labels
            key_list = list(self.scene4picture.labels_dict.keys())
            for key in key_list:
                deleted_item = self.scene4picture.labels_dict.pop(key)
                self.scene4picture.removeItem(deleted_item)

            # adding new labels
            object_size_keyword = 'bndbox'  # it includes these tags: xmin, ymin, xmax, ymax.
            for index, object_label in enumerate(root.findall('./object')):
                timestamp = str(int(datetime.now().timestamp()))
                print('index %s: %s' % (index, object_label))
                # loading only complete data and abandoning the bad data
                xmin_tag = object_label.find(object_size_keyword).find('xmin')  # returns an element instance or None
                if isinstance(xmin_tag, ElementTree.Element):
                    xmin = float(xmin_tag.text)
                else:
                    print('detecting: no xmin tag and continue')
                    continue
                ymin_tag = object_label.find(object_size_keyword).find('ymin')
                if isinstance(ymin_tag, ElementTree.Element):
                    ymin = float(ymin_tag.text)
                else:
                    print('detecting: no ymin tag and continue')
                    continue
                xmax_tag = object_label.find(object_size_keyword).find('xmax')
                if isinstance(xmax_tag, ElementTree.Element):
                    xmax = float(xmax_tag.text)
                else:
                    print('detecting: no xmax tag and continue')
                    continue
                ymax_tag = object_label.find(object_size_keyword).find('ymax')
                if isinstance(ymax_tag, ElementTree.Element):
                    ymax = float(ymax_tag.text)
                else:
                    print('detecting: no ymax tag and continue')
                    continue
                print('xmin: %s, ymin: %s, xmax: %s, ymax:%s' % (xmin, ymin, xmax, ymax))
                name_tag = object_label.find('name')
                name_tag_text = name_tag.text if isinstance(name_tag, ElementTree.Element) else 'Janideen'
                # creating instance of corresponding class
                label_rect = QRectF(xmin, ymin, xmax - xmin, ymax - ymin)
                new_label = self.scene4picture.making_new_rect_instance(
                    parent=self.scene4picture,
                    init_qrect=label_rect,
                    boundary_x=self.scene4picture.pic_item01.x(),
                    boundary_y=self.scene4picture.pic_item01.y(),
                    boundary_width=self.scene4picture.pic_item01.pixmap.width(),
                    boundary_height=self.scene4picture.pic_item01.pixmap.height(),
                    id=timestamp + '_' + str(index)
                )
                new_label.text4cv_id = name_tag_text
                #
                self.scene4picture.labels_dict[new_label.id_str] = new_label  # the key might already exist in the dict
                self.scene4picture.addItem(new_label)
        else:
            print('The path does not exist: %s' %xml_path)
        print('------------------test_loading_xml4current_pic ends-----------------------------')

    def reloading_next_img(self):
        print('------------------reloading_next_img starts-----------------------------')
        # deleting current labels
        key_list = list(self.scene4picture.labels_dict.keys())
        for key in key_list:
            deleted_item = self.scene4picture.labels_dict.pop(key)
            self.scene4picture.removeItem(deleted_item)
        print('labels dict: %s' %self.scene4picture.labels_dict)

        #
        self.index4img_path_list = self.index4img_path_list + 1
        current_length = len(self.img_path_list)
        if self.index4img_path_list >= current_length:
            self.index4img_path_list = self.index4img_path_list - current_length
        elif self.index4img_path_list <= -current_length:
            self.index4img_path_list = self.index4img_path_list + current_length
        self.current_img_path = self.img_path_list[self.index4img_path_list]  # might raise 'index out of range' error
        print('current image path: %s' %self.current_img_path)

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
        print('------------------reloading_next_img ends-----------------------------')

    def reloading_previous_img(self):
        print('------------------reloading_previous_img starts-----------------------------')
        # deleting current labels
        key_list = list(self.scene4picture.labels_dict.keys())
        for key in key_list:
            deleted_item = self.scene4picture.labels_dict.pop(key)
            self.scene4picture.removeItem(deleted_item)
        print('labels dict: %s' % self.scene4picture.labels_dict)

        #
        self.index4img_path_list = self.index4img_path_list - 1
        current_length = len(self.img_path_list)
        if self.index4img_path_list >= current_length:
            self.index4img_path_list = self.index4img_path_list - current_length
        elif self.index4img_path_list <= -current_length:
            self.index4img_path_list = self.index4img_path_list + current_length
        self.current_img_path = self.img_path_list[self.index4img_path_list]  # might raise 'index out of range' error
        print('current image path: %s' % self.current_img_path)

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
        print('------------------reloading_previous_img ends-----------------------------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())

