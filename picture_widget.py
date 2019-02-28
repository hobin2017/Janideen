# -*- coding: utf-8 -*-
"""

"""
import copy

import os
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QMenu, QGraphicsScene

from picture_accessory import PicWidget02_mask01, PicWidget_Reminder02, PicWidget_Label02
from data4label import RootElement01, ObjectElement01
from label_accessary import Label_Editing_Dialog01


class PicWidget01_signals01(QObject):
    """
    Originally, it is used to emit signals for PicWidget01 class
    """
    mouse_left_click = pyqtSignal(object)
    mouse_move01 = pyqtSignal(object)
    mouse_left_click_release = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)


class PicWidget01(QGraphicsPixmapItem):

    def __init__(self, img_path, parent):
        super().__init__()
        #
        self.signals = PicWidget01_signals01(parent=None)
        self.pixmap = QPixmap(img_path)
        self.setPixmap(self.pixmap)
        # others
        self.img_path = img_path
        self.parent = parent
        self.resizing_enable_flag = False
        self.first_qpoint = QPointF()


    def print_mouse_qevent(self, qt_mouse_event):
        """
        :param qt_mouse_event: PyQt5.QtWidgets.QGraphicsSceneMouseEvent
        :return:
        """
        print('------------------print_mouse_qevent starts---------------------------------------')
        print('------------------source---------------------------------------')
        # 0: NotSynthesized; 1, SynthesizedBySystem; 2, SynthesizedByQt; 3, SynthesizedByApplication;
        print(qt_mouse_event.source())  # PyQt5.QtCore.Qt.MouseEventSource
        print('------------------position---------------------------------------')
        print('item coordinate: %s' % qt_mouse_event.pos())  # QPointF
        print('last record in item coordinate: %s' % qt_mouse_event.lastPos())  # # QPointF; used in QMouseMoveEvent
        print('scene coordinate: %s' % qt_mouse_event.scenePos())  # QPointF
        print('screen coordinate: %s' % qt_mouse_event.screenPos())  # QPoint
        print('------------------button type---------------------------------------')
        # 0: not a button action; 1: left; 2: right; 3, middle;
        print(qt_mouse_event.button())  # PyQt5.QtCore.Qt.MouseButton
        print('------------------print_mouse_qevent ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        print('------------------mousePressEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_mouse_qevent(args[0])
        if args[0].button() == Qt.LeftButton:
            self.resizing_enable_flag = True
            self.first_qpoint = args[0].pos()
            self.signals.mouse_left_click.emit(args[0].pos())
        else:
            self.resizing_enable_flag = False
        print('------------------mousePressEvent of %s ends-----------------------------' % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        print('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_mouse_qevent(args[0])
        if self.resizing_enable_flag:
            self.signals.mouse_move01.emit(args[0].pos())
        print('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        print('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_mouse_qevent(args[0])
        if args[0].button() == Qt.LeftButton:
            if self.first_qpoint == args[0].pos():
               print('firs point is equal to second point')
            else:
                self.signals.mouse_left_click_release.emit(args[0].pos())
        print('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)


class PicWidget02(QGraphicsPixmapItem):

    def __init__(self, img_path, parent):
        super().__init__()
        print('------------------initialization of %s starts-----------------------------' % self.__class__)
        #
        self.pixmap = QPixmap(img_path)
        print('height of pixmap in %s: %s' %(self.pixmap.height(), self.__class__))
        print('width of pixmap in %s: %s' %(self.pixmap.width(), self.__class__))
        self.setPixmap(self.pixmap)

        # others
        self.img_path = img_path
        self.parent = parent
        self.resizing_enable_flag = False
        self.first_qpoint = QPointF()
        print('------------------initialization of %s ends-----------------------------' % self.__class__)


    def contextMenuEvent(self, *args, **kwargs):
        print('------------------contextMenuEvent of %s starts-----------------------------' % self.__class__)
        # print(args)  # a list of PyQt5.QtWidgets.QGraphicsSceneContextMenuEvent
        # print(kwargs)
        pos = args[0].screenPos()
        print('current mouse position: %s' %pos)
        menu = QMenu()
        make_action = menu.addAction('make label')  # QAction class
        make_action.triggered.connect(self.parent.operating_mode2making_new_label)
        selected_action = menu.exec(pos)  # the top-left point of the menu
        # print(selected_action)
        print('------------------contextMenuEvent of %s ends-----------------------------' % self.__class__)

    def wheelEvent(self, *args, **kwargs):
        """
        :param args: a list of PyQt5.QtWidgets.QGraphicsSceneWheelEvent
        :param kwargs:
        :return:
        """
        print('------------------wheelEvent of %s starts-----------------------------' % self.__class__)
        print('mouse position relative to the widget that received the event: %s' %args[0].pos())
        print(args[0].delta())  # the rotated degree; the unit is 1/8 degree; positive is forward-rotation;
        print(args[0].orientation())  # 1 is Qt.Horizontal and 2 is Qt.Vertical
        if args[0].delta() > 0:
            self.scene().views()[0].scale(1.05, 1.05)
        else:
            self.scene().views()[0].scale(0.95, 0.95)

        # changing the scroll bar to view the specific part
        current_cursor_x = args[0].pos().x()
        current_cursor_y = args[0].pos().y()
        horizontal_factor =  current_cursor_x / self.pixmap.width()
        veritical_factor = current_cursor_y / self.pixmap.height()
        view_horizon_scroll_bar = self.scene().views()[0].horizontalScrollBar()
        view_vertical_scroll_bar = self.scene().views()[0].verticalScrollBar()
        print('current value of scroll bar:')
        print('horizontal position: %s (max %s)' % (view_horizon_scroll_bar.sliderPosition(), view_horizon_scroll_bar.maximum()))
        print('vertical position: %s (max %s)' % (view_vertical_scroll_bar.sliderPosition(), view_vertical_scroll_bar.maximum()))
        self.scene().views()[0].horizontalScrollBar().setSliderPosition(int(horizontal_factor * view_horizon_scroll_bar.maximum()))
        self.scene().views()[0].verticalScrollBar().setSliderPosition(int(veritical_factor * view_vertical_scroll_bar.maximum()))
        print('new value of scroll bar:')
        print('horizontal position: %s (max %s)' % (view_horizon_scroll_bar.sliderPosition(), view_horizon_scroll_bar.maximum()))
        print('vertical position: %s (max %s)' % (view_vertical_scroll_bar.sliderPosition(), view_vertical_scroll_bar.maximum()))
        print('------------------wheelEvent of %s ends-----------------------------' % self.__class__)

    def reloading_img(self, img_path):
        self.pixmap.load(img_path)
        self.setPixmap(self.pixmap)
        print('height of pixmap in %s: %s' % (self.pixmap.height(), self.__class__))
        print('width of pixmap in %s: %s' % (self.pixmap.width(), self.__class__))


class PicScene01(QGraphicsScene):

    def __init__(self, img_path=r'./images/20190214102814.jpg',
                 pic_visual_fixed_width=1000, pic_visual_fixed_height=860, parent=None):
        super().__init__(parent)
        # parameters used in widget_init()
        self.img_path = img_path
        #
        self.widget_init()
        self.widget_manage()
        #
        self.parent = parent
        self.pic_visual_fixed_width = pic_visual_fixed_width
        self.pic_visual_fixed_height = pic_visual_fixed_height
        self.labels_dict = {}
        self.xml_data = RootElement01()  # xml.etree.ElementTree.Element

    def widget_init(self):
        #
        self.pic_item01 = PicWidget02(img_path=self.img_path, parent=self)
        self.addItem(self.pic_item01)  # takes ownership of the item

        # This 'mask' item is invisible be default
        self.pic_item_mask01 = PicWidget02_mask01(x=self.pic_item01.x(), y=self.pic_item01.y(),
                                                  width=self.pic_item01.pixmap.width(),
                                                  height=self.pic_item01.pixmap.height())
        self.pic_item_mask01.signals.mouse_left_click.connect(self.updating4rect_reminder)
        self.pic_item_mask01.signals.mouse_move01.connect(self.resizing4rect_reminder)
        self.pic_item_mask01.signals.mouse_left_click_release.connect(self.making_new_rect4pic_label)
        self.addItem(self.pic_item_mask01)

        #
        self.rect_reminder01 = PicWidget_Reminder02(boundary_x=self.pic_item01.x(), boundary_y=self.pic_item01.y(),
                                                    boundary_widht=self.pic_item01.pixmap.width(),
                                                    boundary_height=self.pic_item01.pixmap.height(),
                                                    parent=self)
        self.addItem(self.rect_reminder01)
        #
        self.dialog4labels = Label_Editing_Dialog01(parent=None)

    def widget_manage(self):
        pass

    def updating4rect_reminder(self, first_qpoint):
        print('------------------updating4rect_reminder starts-----------------------------')
        self.rect_reminder01.first_qpoint_x = first_qpoint.x()
        self.rect_reminder01.first_qpoint_y = first_qpoint.y()
        self.rect_reminder01.setVisible(True)  # It is set to False when making new rectangle
        print('------------------updating4rect_reminder ends-----------------------------')

    def resizing4rect_reminder(self, second_qpoint):
        # print('------------------resizing4rect_reminder starts-----------------------------')
        self.rect_reminder01.second_qpoint_x = second_qpoint.x()
        self.rect_reminder01.second_qpoint_y = second_qpoint.y()
        if self.rect_reminder01.first_qpoint_x < self.rect_reminder01.second_qpoint_x:
            if self.rect_reminder01.first_qpoint_y < self.rect_reminder01.second_qpoint_y:
                # the first point is the top left point and the second point is the bottom right point.
                self.rect_reminder01.rect4update.setCoords(self.rect_reminder01.first_qpoint_x,
                                                           self.rect_reminder01.first_qpoint_y,
                                                           self.rect_reminder01.second_qpoint_x,
                                                           self.rect_reminder01.second_qpoint_y)
            else:
                self.rect_reminder01.rect4update.setCoords(self.rect_reminder01.first_qpoint_x,
                                                           self.rect_reminder01.second_qpoint_y,
                                                           self.rect_reminder01.second_qpoint_x,
                                                           self.rect_reminder01.first_qpoint_y)
        else:
            if self.rect_reminder01.first_qpoint_y < self.rect_reminder01.second_qpoint_y:
                self.rect_reminder01.rect4update.setCoords(self.rect_reminder01.second_qpoint_x,
                                                           self.rect_reminder01.first_qpoint_y,
                                                           self.rect_reminder01.first_qpoint_x,
                                                           self.rect_reminder01.second_qpoint_y)
            else:
                # the first point is bottom right point and the second point is the the top left point.
                self.rect_reminder01.rect4update.setCoords(self.rect_reminder01.second_qpoint_x,
                                                           self.rect_reminder01.second_qpoint_y,
                                                           self.rect_reminder01.first_qpoint_x,
                                                           self.rect_reminder01.first_qpoint_y)
        self.rect_reminder01.setRect(self.rect_reminder01.rect4update)
        # print('------------------resizing4rect_reminder ends-----------------------------')

    def making_new_rect4pic_label(self, second_qpoint):
        print('------------------making_new_rect4pic_label starts-----------------------------')
        # covering detection of bounding rectangle for left edge and right edge
        horizontal_changed_flag = True
        if self.rect_reminder01.rect4update.x() < self.rect_reminder01.bounding_rect.x():
            # detecting that left edge needs fixing
            # print('original rectangle: %s' %self.rect_reminder01.rect4update)
            self.rect_reminder01.rect4update.setX(self.rect_reminder01.bounding_rect.x())
            # print('modified rectangle: %s' %self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        elif self.rect_reminder01.rect4update.right() > self.rect_reminder01.bounding_rect.right():
            # detecting that right edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect_reminder01.rect4update.setRight(self.rect_reminder01.bounding_rect.right())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        else:
            horizontal_changed_flag = False

        # covering detection of bounding rectangle for top edge and bottom edge
        vertical_changed_flag = True
        if self.rect_reminder01.rect4update.y() < self.rect_reminder01.bounding_rect.y():
            # detecting that top edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect_reminder01.rect4update.setY(self.rect_reminder01.bounding_rect.y())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        elif self.rect_reminder01.rect4update.bottom() > self.rect_reminder01.bounding_rect.bottom():
            # detecting that bottom edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect_reminder01.rect4update.setBottom(self.rect_reminder01.bounding_rect.bottom())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update)  # to verify QGraphicsRectItem.setX() function
        else:
            vertical_changed_flag = False

        if vertical_changed_flag or horizontal_changed_flag:
            self.rect_reminder01.setRect(self.rect_reminder01.rect4update)
            print('updating the rectangle reminder since a part of it is outside the bounding rectangle')

        # new label
        min_width = 5
        min_height = 5
        if self.rect_reminder01.rect().width() > min_width and self.rect_reminder01.rect().height() > min_height:
            # creating new label
            new_label = self.making_new_rect_instance(parent=self,
                                                      init_qrect=copy.copy(self.rect_reminder01.rect4update),
                                                      boundary_x=self.pic_item01.x(),
                                                      boundary_y=self.pic_item01.y(),
                                                      boundary_width=self.pic_item01.pixmap.width(),
                                                      boundary_height=self.pic_item01.pixmap.height(),
                                                      )
            self.labels_dict[new_label.id_str] = new_label  # the key might already exist in the dict
            self.addItem(new_label)

            # user input for object name
            self.dialog4labels.id4object01 = new_label
            result = self.dialog4labels.exec_()  # int, 1: QDialog.Accepted; 0: QDialog.Rejected
            print('dialog result (1 is accepted; 0 is rejected): %s' % result)
        else:
            print('no new label is made since it is too small')

        # end
        self.rect_reminder01.setVisible(False)  # the reminder rectangle might be shown when resizing the rectangle
        self.rect_reminder01.setRect(0, 0, 0, 0)  # without it, there will be a rectangle when creating new label next time;
        self.pic_item_mask01.setVisible(False)
        print('------------------making_new_rect4pic_label ends-----------------------------')

    def making_new_rect_instance(self, init_qrect, boundary_x, boundary_y, boundary_width, boundary_height,
                                           id=None, parent=None,):
        """
           The original purpose to create this function is to avoid forgetting signal connection. And you can create the
        class directly and do corresponding signal connection.
           Basically, it is used in two scenarios: 1, loading xml to create labels; 2, creating one label manually;
        Hence, this function is reused and may be called by other class object. Anyway, this should be fine since the
        signal connection is correct.
        :return:
        """
        new_label = PicWidget_Label02(parent=self, init_qrect=init_qrect, boundary_x=boundary_x, boundary_y=boundary_y,
                                      boundary_width=boundary_width, boundary_height=boundary_height, id=id)
        new_label.signals.label_delete.connect(self.deleting_pic_label)
        new_label.signals.detecting_double_click.connect(self.showing_dialog4editing)
        return new_label

    def deleting_pic_label(self, id):
        """
        Originally, this is executed by the keyReleaseEvent of specific QGraphicsRectItem.
        :param id: str and the content is timestamp
        :return:
        """
        print('------------------deleting_pic_label starts-----------------------------')
        print('current focus item: %s' % self.focusItem())
        deleted_label = self.labels_dict.pop(id)
        print('the deleted label: %s' % deleted_label)
        print('the rest labels with total %s: %s' % (len(self.labels_dict.keys()), self.labels_dict.keys()))
        self.removeItem(deleted_label)
        print('------------------deleting_pic_label ends-----------------------------')

    def operating_mode2making_new_label(self):
        print('------------------operating_mode2making_new_label starts-----------------------------')
        self.pic_item_mask01.setVisible(True)
        print('------------------operating_mode2making_new_label ends-----------------------------')

    def showing_dialog4editing(self, calling_object):
        print('------------------showing_dialog4editing pf %s starts-----------------------------' %self.__class__)
        print('current text of double-clicked label: %s' % calling_object.text4cv_id)
        self.dialog4labels.id4object01 = calling_object
        self.dialog4labels.line_edit.setText(calling_object.text4cv_id)
        result = self.dialog4labels.exec_()  # int, 1: QDialog.Accepted; 0: QDialog.Rejected
        print('dialog result (1 is accepted; 0 is rejected): %s' % result)
        print('------------------showing_dialog4editing of %s ends-----------------------------' %self.__class__)

