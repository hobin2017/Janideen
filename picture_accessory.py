# -*- coding: utf-8 -*-
"""
  Currently, these classes are used with QGraphicsScene class and hence only store QGraphicsScene-related classes here.
"""
import copy

from PyQt5.QtCore import QObject, QRectF, Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem
from datetime import datetime

from LoggingModule import MyLogging1_2


class PicWidget_Reminder01(QGraphicsRectItem):
    """
    Currently, this class is used to remind user the rectangle of the new label. And it stores the temporary information
which is used when making new labels.
    """

    def __init__(self, parent):
        super().__init__()
        # rectangle
        self.first_qpoint_x = 0
        self.first_qpoint_y = 0
        self.second_qpoint_x = 0
        self.second_qpoint_y = 0
        self.rect4update = QRectF()
        # pen
        self.pen01 = QPen(QColor(255, 0, 0))
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.DashLine)
        self.setPen(self.pen01)

        # others
        self.parent = parent


class PicWidget_Reminder02(QGraphicsRectItem):
    """
    Currently, this class is used to remind user the rectangle of the new label. And it stores the temporary information
which is used when making new labels.
    """

    def __init__(self, boundary_x, boundary_y, boundary_widht, boundary_height, parent):
        super().__init__()
        self.bounding_rect = QRectF(boundary_x, boundary_y, boundary_widht, boundary_height)
        self.prepareGeometryChange()  # This will executed the corresponding QGraphicsItem.boundingRect();
        # print('bounding rectangle of %s :%s' % (self.__class__, self.bounding_rect))
        # rectangle
        self.first_qpoint_x = 0
        self.first_qpoint_y = 0
        self.second_qpoint_x = 0
        self.second_qpoint_y = 0
        self.rect4update = QRectF()
        # pen
        self.pen01 = QPen(QColor(255, 0, 0))
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.DashLine)
        self.setPen(self.pen01)

        # others
        self.parent = parent


    def boundingRect(self):
        """
        Reimplement this function to let QGraphicsView determine what parts of the widget need to be redrawn.
        :return:
        """
        return self.bounding_rect

    def resetting_bounding_rect(self, boundary_x, boundary_y, boundary_widht, boundary_height):
        self.bounding_rect = QRectF(boundary_x, boundary_y, boundary_widht, boundary_height)


class PicWidget_Label_signals01(QObject):
    """
    Originally, it is used to emit signals for PicWidget_Label01 class
    """
    label_delete = pyqtSignal(object)
    label_clear_focus = pyqtSignal(object)
    detecting_double_click = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)


class PicWidget_Label01(QGraphicsRectItem):

    def __init__(self, parent, init_qrect):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsFocusable, True) # enable key press event
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        # self.setFlag(QGraphicsItem.ItemIsMovable)  # It will fail when you defines the mouseMoveEvent.
        self.signals = PicWidget_Label_signals01(parent=None)
        # rectangle
        self.rect4update = init_qrect
        self.setRect(self.rect4update)
        # pen
        self.color01 = QColor(0, 0, 255)
        self.pen01 = QPen(self.color01)
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.SolidLine)
        self.setPen(self.pen01)

        # others
        self.selected_flag = False
        self.resizing_enable_flag = False
        self.parent = parent


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

    def print_key_qevent(self, qt_key_event):
        print('------------------print_key_qevent starts---------------------------------------')
        print(qt_key_event.count())  # Returns the number of keys involved in this event. If text() is not empty, this is simply the length of the string.
        print(qt_key_event.isAutoRepeat())  # Returns true if this event comes from an auto-repeating key; returns false if it comes from an initial key press.
        print(qt_key_event.key())  # Returns the code of the key that was pressed or released.
        print(qt_key_event.text())  # Returns the Unicode text that this key generated.
        print('------------------print_key_qevent ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        print('------------------mousePressEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        click_point = args[0].pos()
        if self.contains(click_point):
            if self.selected_flag:
                if args[0].button() == Qt.LeftButton:
                    # updating algorithm
                    self.resizing_enable_flag = True
                    center_point = self.rect().center()
                    relative_vector = click_point - center_point
                    if relative_vector.x() > 0 and relative_vector.y() > 0:
                        self.setCursor(Qt.SizeFDiagCursor)
                        self.rect4update.setBottomRight(click_point)
                        self.setRect(self.rect4update)
                    elif relative_vector.x() > 0 and relative_vector.y() < 0:
                        self.setCursor(Qt.SizeBDiagCursor)
                        self.rect4update.setTopRight(click_point)
                        self.setRect(self.rect4update)
                    elif relative_vector.x() < 0 and relative_vector.y() > 0:
                        self.setCursor(Qt.SizeBDiagCursor)
                        self.rect4update.setBottomLeft(click_point)
                        self.setRect(self.rect4update)
                    elif relative_vector.x() < 0 and relative_vector.y() < 0:
                        self.setCursor(Qt.SizeFDiagCursor)
                        self.rect4update.setTopLeft(click_point)
                        self.setRect(self.rect4update)
                else:
                    self.resizing_enable_flag = False
            else:
                # first time for selecting rectangle
                self.selected_flag = True
                self.color01.setRgb(255, 0, 0)
                self.pen01.setColor(self.color01)
                self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle
                # QGraphicsItem.grabMouse()
                # This function will receives all kinds of mouse events that occur inside the scene.
                # This will not block the execution of those code below grabMouse().
                # This can be called twice and the result is like the result that it is called only once.
                # This will stop until 1, item is invisible; 2, item is removed from scene; 3, item is deleted;
                # 4, corresponding ungrabMouse() is called; 5, another item calls grabMouse();
                self.grabMouse()
        else:
            self.ungrabMouse()
            self.signals.label_clear_focus.emit(11)
            self.selected_flag = False
            self.color01.setRgb(0, 0, 255)
            self.pen01.setColor(self.color01)
            self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle

        print('------------------mousePressEvent of %s ends-----------------------------' % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        print('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        print(args)
        # print(kwargs)
        # self.print_mouse_qevent(args[0])
        if self.resizing_enable_flag:
            temp_moving_point = args[0].pos()
            center_point = self.rect().center()
            relative_vector = temp_moving_point - center_point
            if relative_vector.x() > 0 and relative_vector.y() > 0:
                self.rect4update.setBottomRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() > 0 and relative_vector.y() < 0:
                self.rect4update.setTopRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() > 0:
                self.rect4update.setBottomLeft(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() < 0:
                self.rect4update.setTopLeft(temp_moving_point)
                self.setRect(self.rect4update)
        print('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        print('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_mouse_qevent(args[0])
        self.unsetCursor()
        if args[0].button() == Qt.LeftButton:
            self.resizing_enable_flag = False
        print('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)

    def keyReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtGui.QKeyEvent object
        :param kwargs:
        :return:
        """
        print('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        if args[0].key() == Qt.Key_Delete and self.selected_flag:
            self.signals.label_delete.emit(11)
        print('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)


class PicWidget_Label02(QGraphicsRectItem):
    """
      Compared with PicWidget_Label01, the main difference is the mousePressEvent and mouseMoveEvent. Currently the item
    can be resized and moved.
    """

    def __init__(self, parent, init_qrect, boundary_x, boundary_y, boundary_width, boundary_height, id=None):
        """
        :param parent: QGraphicsScene
        :param init_qrect:
        :param boundary_x:
        :param boundary_y:
        :param boundary_widht:
        :param boundary_height:
        :param id:
        """
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)  # enable key press event
        self.setAcceptHoverEvents(True)  # enable key hover event
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        # self.setFlag(QGraphicsItem.ItemIsMovable)  # It will fail when you defines the mouseMoveEvent.
        self.bounding_rect = QRectF(boundary_x, boundary_y, boundary_width, boundary_height)
        self.prepareGeometryChange()  # This will executed the corresponding QGraphicsItem.boundingRect();
        print('bounding rectangle of %s :%s' % (self.__class__, self.bounding_rect))
        self.signals = PicWidget_Label_signals01(parent=None)
        # rectangle
        self.rect4update = init_qrect
        self.setRect(self.rect4update)
        # pen
        self.color01 = QColor(0, 0, 255)
        self.pen01 = QPen(self.color01)
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.SolidLine)
        self.setPen(self.pen01)

        # others
        self.moving_mode_flag = False
        self.resizing_mode_flag = False
        self.parent = parent
        if id:
            self.id_str = id
        else:
            self.id_str = str(float(datetime.now().timestamp()))  # used as 'id'
        self.text4cv_id = None  # used with QDialog when there is a need to change the value
        self.timestamp4last_click = datetime.now().timestamp()  # used to execute codes for double click

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

    def print_key_qevent(self, qt_key_event):
        print('------------------print_key_qevent starts---------------------------------------')
        print(
            qt_key_event.count())  # Returns the number of keys involved in this event. If text() is not empty, this is simply the length of the string.
        print(
            qt_key_event.isAutoRepeat())  # Returns true if this event comes from an auto-repeating key; returns false if it comes from an initial key press.
        print(qt_key_event.key())  # Returns the code of the key that was pressed or released.
        print(qt_key_event.text())  # Returns the Unicode text that this key generated.
        print('------------------print_key_qevent ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        print('------------------mousePressEvent of %s starts-----------------------------' % self.__class__)
        self.moving_mode_flag = False
        self.resizing_mode_flag = False
        timestamp4current_click = datetime.now().timestamp()
        if timestamp4current_click - self.timestamp4last_click > 1:
            print('detecting single mouse click')
            self.timestamp4last_click = timestamp4current_click  # the current click is accepted and become the last click
            #
            self.color01.setRgb(255, 0, 0)
            self.pen01.setColor(self.color01)
            self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle
            #
            click_point = args[0].pos()
            topleft_point = self.rect().topLeft()
            rect_width = self.rect().width()
            rect_height = self.rect().height()
            factor_left = 1 / 10
            factor_right = 9 / 10
            factor_top = 1 / 10
            factor_bottom = 9 / 10
            compared_point01 = QPointF(topleft_point.x() + rect_width * factor_left, topleft_point.y())
            compared_point02 = QPointF(topleft_point.x() + rect_width * factor_right, topleft_point.y())
            compared_point03 = QPointF(topleft_point.x(), topleft_point.y() + rect_height * factor_top)
            compared_point04 = QPointF(topleft_point.x(), topleft_point.y() + rect_height * factor_bottom)
            if compared_point01.x() < click_point.x() < compared_point02.x():
                self.moving_mode_flag = True
                self.setCursor(Qt.ClosedHandCursor)
            elif compared_point03.y() < click_point.y() < compared_point04.y():
                self.moving_mode_flag = True
                self.setCursor(Qt.ClosedHandCursor)
            else:
                self.resizing_mode_flag = True
                self.setCursor(Qt.CrossCursor)
        else:
            print('detecting double mouse click')
            self.signals.detecting_double_click.emit(self)
        print('------------------mousePressEvent of %s ends-----------------------------' % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        # print('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        if self.moving_mode_flag:
            event = args[0]
            self.offset_vector = event.pos() - event.lastPos()
            self.rect4update.translate(self.offset_vector)
            self.setRect(self.rect4update)
        elif self.resizing_mode_flag:
            temp_moving_point = args[0].pos()
            center_point = self.rect().center()
            relative_vector = temp_moving_point - center_point
            if relative_vector.x() > 0 and relative_vector.y() > 0:
                self.rect4update.setBottomRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() > 0 and relative_vector.y() < 0:
                self.rect4update.setTopRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() > 0:
                self.rect4update.setBottomLeft(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() < 0:
                self.rect4update.setTopLeft(temp_moving_point)
                self.setRect(self.rect4update)
        # print('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        print('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        self.color01.setRgb(0, 0, 255)
        self.pen01.setColor(self.color01)
        self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle
        self.setCursor(Qt.ArrowCursor)
        self.rectangle_correcting()
        print('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)

    def keyReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtGui.QKeyEvent object
        :param kwargs:
        :return:
        """
        print('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        if args[0].key() == Qt.Key_Delete:
            self.signals.label_delete.emit(self.id_str)
        print('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)

    def boundingRect(self):
        """
        Reimplement this function to let QGraphicsView determine what parts of the widget need to be redrawn.
        :return:
        """
        return self.bounding_rect

    def rectangle_correcting(self):
        # covering detection of bounding rectangle for left edge and right edge
        horizontal_changed_flag = True
        if self.rect4update.x() < self.bounding_rect.x():
            # detecting that left edge needs fixing
            # print('original rectangle: %s' %self.rect_reminder01.rect4update)
            self.rect4update.setX(self.bounding_rect.x())
            # print('modified rectangle: %s' %self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        elif self.rect4update.right() > self.bounding_rect.right():
            # detecting that right edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setRight(self.bounding_rect.right())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        else:
            horizontal_changed_flag = False

        # covering detection of bounding rectangle for top edge and bottom edge
        vertical_changed_flag = True
        if self.rect4update.y() < self.bounding_rect.y():
            # detecting that top edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setY(self.bounding_rect.y())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        elif self.rect4update.bottom() > self.bounding_rect.bottom():
            # detecting that bottom edge needs fixing
            # print('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setBottom(self.bounding_rect.bottom())
            # print('modified rectangle: %s' % self.rect_reminder01.rect4update)  # to verify QGraphicsRectItem.setX() function
        else:
            vertical_changed_flag = False

        if vertical_changed_flag or horizontal_changed_flag:
            self.setRect(self.rect4update)
            print('updating the rectangle reminder since a part of it is outside the bounding rectangle')

    def hoverEnterEvent(self, *args, **kwargs):
        print('------------------hoverEnterEvent of %s starts-----------------------------' % self.__class__)
        self.color01.setRgb(255, 0, 0)
        self.pen01.setColor(self.color01)
        self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle
        self.parent.setFocusItem(self)
        print('------------------hoverEnterEvent of %s ends-----------------------------' % self.__class__)

    def hoverLeaveEvent(self, *args, **kwargs):
        print('------------------hoverLeaveEvent of %s starts-----------------------------' % self.__class__)
        self.color01.setRgb(0, 0, 255)
        self.pen01.setColor(self.color01)
        self.setPen(self.pen01)  # QGraphicsRectItem.setPen() will update the current status of the rectangle
        self.clearFocus()
        print('------------------hoverLeaveEvent of %s ends-----------------------------' % self.__class__)


class PicWidget_Label03(QGraphicsRectItem):
    """
      Compared with PicWidget_Label02, one difference is information about id (self.id_info) is changed to list index.
    """

    def __init__(self, parent, init_qrect, boundary_x, boundary_y, boundary_width, boundary_height, id=None):
        """
        :param parent: QGraphicsScene
        :param init_qrect:
        :param boundary_x:
        :param boundary_y:
        :param boundary_widht:
        :param boundary_height:
        :param id:
        """
        super().__init__()
        self.mylogging4picwidget_label03 = MyLogging1_2(logger_name='hobin')
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)  # enable key press event
        self.setAcceptHoverEvents(True)  # enable key hover event
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        # self.setFlag(QGraphicsItem.ItemIsMovable)  # It will fail when you defines the mouseMoveEvent.
        self.bounding_rect = QRectF(boundary_x, boundary_y, boundary_width, boundary_height)
        self.prepareGeometryChange()  # This will executed the corresponding QGraphicsItem.boundingRect();
        self.mylogging4picwidget_label03.logger.debug('bounding rectangle of %s :%s' % (self.__class__, self.bounding_rect))
        self.signals = PicWidget_Label_signals01(parent=None)
        # rectangle
        self.rect4update = init_qrect
        self.setRect(self.rect4update)
        # pen
        self.color01 = QColor(0, 0, 255)
        self.pen01 = QPen(self.color01)
        self.pen01.setWidth(2)  # unit: pixel
        self.pen01.setStyle(Qt.SolidLine)
        self.setPen(self.pen01)
        #
        self.brush01 = QBrush(Qt.NoBrush)
        self.brush02 = QBrush(QColor(48, 155, 255, 200), Qt.SolidPattern)

        # others
        self.moving_mode_flag = False
        self.resizing_mode_flag = False
        self.parent = parent
        if isinstance(id, int):
            self.id_info = id
        else:
            self.id_info = int(datetime.now().timestamp())  # used as 'id'
        self.text4cv_id = None  # used with QDialog when there is a need to change the value
        self.timestamp4last_click = datetime.now().timestamp()  # used to execute codes for double click

    def print_mouse_qevent(self, qt_mouse_event):
        """
        :param qt_mouse_event: PyQt5.QtWidgets.QGraphicsSceneMouseEvent
        :return:
        """
        self.mylogging4picwidget_label03.logger.debug('------------------print_mouse_qevent starts---------------------------------------')
        self.mylogging4picwidget_label03.logger.debug('------------------source---------------------------------------')
        # 0: NotSynthesized; 1, SynthesizedBySystem; 2, SynthesizedByQt; 3, SynthesizedByApplication;
        self.mylogging4picwidget_label03.logger.debug(qt_mouse_event.source())  # PyQt5.QtCore.Qt.MouseEventSource
        self.mylogging4picwidget_label03.logger.debug('------------------position---------------------------------------')
        self.mylogging4picwidget_label03.logger.debug('item coordinate: %s' % qt_mouse_event.pos())  # QPointF
        self.mylogging4picwidget_label03.logger.debug('last record in item coordinate: %s' % qt_mouse_event.lastPos())  # # QPointF; used in QMouseMoveEvent
        self.mylogging4picwidget_label03.logger.debug('scene coordinate: %s' % qt_mouse_event.scenePos())  # QPointF
        self.mylogging4picwidget_label03.logger.debug('screen coordinate: %s' % qt_mouse_event.screenPos())  # QPoint
        self.mylogging4picwidget_label03.logger.debug('------------------button type---------------------------------------')
        # 0: not a button action; 1: left; 2: right; 3, middle;
        self.mylogging4picwidget_label03.logger.debug(qt_mouse_event.button())  # PyQt5.QtCore.Qt.MouseButton
        self.mylogging4picwidget_label03.logger.debug('------------------print_mouse_qevent ends---------------------------------------')

    def print_key_qevent(self, qt_key_event):
        self.mylogging4picwidget_label03.logger.debug('------------------print_key_qevent starts---------------------------------------')
        self.mylogging4picwidget_label03.logger.debug(
            qt_key_event.count())  # Returns the number of keys involved in this event. If text() is not empty, this is simply the length of the string.
        self.mylogging4picwidget_label03.logger.debug(
            qt_key_event.isAutoRepeat())  # Returns true if this event comes from an auto-repeating key; returns false if it comes from an initial key press.
        self.mylogging4picwidget_label03.logger.debug(qt_key_event.key())  # Returns the code of the key that was pressed or released.
        self.mylogging4picwidget_label03.logger.debug(qt_key_event.text())  # Returns the Unicode text that this key generated.
        self.mylogging4picwidget_label03.logger.debug('------------------print_key_qevent ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        self.mylogging4picwidget_label03.logger.info('------------------mousePressEvent of %s starts-----------------------------' % self.__class__)
        self.moving_mode_flag = False
        self.resizing_mode_flag = False
        timestamp4current_click = datetime.now().timestamp()
        if timestamp4current_click - self.timestamp4last_click > 1:
            self.mylogging4picwidget_label03.logger.info('detecting single mouse click')
            self.timestamp4last_click = timestamp4current_click  # the current click is accepted and become the last click
            #
            click_point = args[0].pos()
            topleft_point = self.rect().topLeft()
            rect_width = self.rect().width()
            rect_height = self.rect().height()
            factor_left = 1 / 10
            factor_right = 9 / 10
            factor_top = 1 / 10
            factor_bottom = 9 / 10
            compared_point01 = QPointF(topleft_point.x() + rect_width * factor_left, topleft_point.y())
            compared_point02 = QPointF(topleft_point.x() + rect_width * factor_right, topleft_point.y())
            compared_point03 = QPointF(topleft_point.x(), topleft_point.y() + rect_height * factor_top)
            compared_point04 = QPointF(topleft_point.x(), topleft_point.y() + rect_height * factor_bottom)
            if compared_point01.x() < click_point.x() < compared_point02.x():
                self.moving_mode_flag = True
                self.setCursor(Qt.ClosedHandCursor)
            elif compared_point03.y() < click_point.y() < compared_point04.y():
                self.moving_mode_flag = True
                self.setCursor(Qt.ClosedHandCursor)
            else:
                self.resizing_mode_flag = True
                self.setCursor(Qt.CrossCursor)
        else:
            self.mylogging4picwidget_label03.logger.info('detecting double mouse click')
            self.signals.detecting_double_click.emit(self)
        self.mylogging4picwidget_label03.logger.info('------------------mousePressEvent of %s ends-----------------------------' % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        # self.mylogging4picwidget_label03.logger.info('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        if self.moving_mode_flag:
            event = args[0]
            self.offset_vector = event.pos() - event.lastPos()
            self.rect4update.translate(self.offset_vector)
            self.setRect(self.rect4update)
        elif self.resizing_mode_flag:
            temp_moving_point = args[0].pos()
            center_point = self.rect().center()
            relative_vector = temp_moving_point - center_point
            if relative_vector.x() > 0 and relative_vector.y() > 0:
                self.rect4update.setBottomRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() > 0 and relative_vector.y() < 0:
                self.rect4update.setTopRight(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() > 0:
                self.rect4update.setBottomLeft(temp_moving_point)
                self.setRect(self.rect4update)
            elif relative_vector.x() < 0 and relative_vector.y() < 0:
                self.rect4update.setTopLeft(temp_moving_point)
                self.setRect(self.rect4update)
        # self.mylogging4picwidget_label03.logger.info('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.mylogging4picwidget_label03.logger.info('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        self.setCursor(Qt.ArrowCursor)
        self.rectangle_correcting()
        self.mylogging4picwidget_label03.logger.info('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)

    def keyReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtGui.QKeyEvent object
        :param kwargs:
        :return:
        """
        self.mylogging4picwidget_label03.logger.info('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)
        # self.mylogging4picwidget_label03.logger.debug(args)
        # self.mylogging4picwidget_label03.logger.debug(kwargs)
        if args[0].key() == Qt.Key_Delete:
            self.signals.label_delete.emit(self.id_info)
        self.mylogging4picwidget_label03.logger.info('------------------keyReleaseEvent of %s starts-----------------------------' % self.__class__)

    def boundingRect(self):
        """
        Reimplement this function to let QGraphicsView determine what parts of the widget need to be redrawn.
        :return:
        """
        return self.bounding_rect

    def rectangle_correcting(self):
        # covering detection of bounding rectangle for left edge and right edge
        horizontal_changed_flag = True
        if self.rect4update.x() < self.bounding_rect.x():
            # detecting that left edge needs fixing
            # self.mylogging4picwidget_label03.logger.debug('original rectangle: %s' %self.rect_reminder01.rect4update)
            self.rect4update.setX(self.bounding_rect.x())
            # to verify QGraphicsRectItem.setX() function
            # self.mylogging4picwidget_label03.logger.debug('modified rectangle: %s' %self.rect_reminder01.rect4update)
        elif self.rect4update.right() > self.bounding_rect.right():
            # detecting that right edge needs fixing
            # self.mylogging4picwidget_label03.logger.debug('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setRight(self.bounding_rect.right())
            # self.mylogging4picwidget_label03.logger.debug('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        else:
            horizontal_changed_flag = False

        # covering detection of bounding rectangle for top edge and bottom edge
        vertical_changed_flag = True
        if self.rect4update.y() < self.bounding_rect.y():
            # detecting that top edge needs fixing
            # self.mylogging4picwidget_label03.logger.debug('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setY(self.bounding_rect.y())
            # self.mylogging4picwidget_label03.logger.debug('modified rectangle: %s' % self.rect_reminder01.rect4update) # to verify QGraphicsRectItem.setX() function
        elif self.rect4update.bottom() > self.bounding_rect.bottom():
            # detecting that bottom edge needs fixing
            # self.mylogging4picwidget_label03.logger.debug('original rectangle: %s' % self.rect_reminder01.rect4update)
            self.rect4update.setBottom(self.bounding_rect.bottom())
            # self.mylogging4picwidget_label03.logger.debug('modified rectangle: %s' % self.rect_reminder01.rect4update)  # to verify QGraphicsRectItem.setX() function
        else:
            vertical_changed_flag = False

        if vertical_changed_flag or horizontal_changed_flag:
            self.setRect(self.rect4update)
            self.mylogging4picwidget_label03.logger.info('updating the rectangle reminder since a part of it is outside the bounding rectangle')

    def hoverEnterEvent(self, *args, **kwargs):
        self.mylogging4picwidget_label03.logger.info('------------------hoverEnterEvent of %s starts-----------------------------' % self.__class__)
        self.setBrush(self.brush02)
        self.parent.setFocusItem(self)
        self.mylogging4picwidget_label03.logger.info('------------------hoverEnterEvent of %s ends-----------------------------' % self.__class__)

    def hoverLeaveEvent(self, *args, **kwargs):
        self.mylogging4picwidget_label03.logger.info('------------------hoverLeaveEvent of %s starts-----------------------------' % self.__class__)
        self.setBrush(self.brush01)
        self.clearFocus()
        self.mylogging4picwidget_label03.logger.info('------------------hoverLeaveEvent of %s ends-----------------------------' % self.__class__)

    def updating_color(self, qcolor):
        self.color01 = copy.copy(qcolor)
        self.pen01.setColor(self.color01)
        self.setPen(self.pen01)

    def updating_brush(self, qbrush=None):
        if qbrush:
            self.setBrush(qbrush)
        else:
            self.setBrush(self.brush01)


class PicWidget02_mask01_signals01(QObject):
    """
    It is used to emit signals for PicWidget02_mask01 class
    """
    mouse_left_click = pyqtSignal(object)
    mouse_move01 = pyqtSignal(object)
    mouse_left_click_release = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)


class PicWidget02_mask01(QGraphicsRectItem):
    """
    Originally, it is stacked on top of another QGraphicsItem (PicWidget02 class)
    """
    def __init__(self, x, y, width, height, parent=None):
        super().__init__()
        self.setAcceptHoverEvents(True)  # enable the item to accept hover events
        self.setZValue(1)
        self.setVisible(False)
        # pen
        self.color01 = QColor(0, 255, 0)
        self.pen01 = QPen(self.color01)
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.SolidLine)
        self.setPen(self.pen01)
        #
        self.rect4update = QRectF(x, y, width, height)
        self.setRect(self.rect4update)
        #
        self.parent = parent
        self.signals = PicWidget02_mask01_signals01(parent=None)

        # self.test_work01()

    def test_work01(self):
        """
        visualization of this rectangle
        :return:
        """
        self.setVisible(True)  # It is invisible in this application by default
        self.pen01 = QPen(QColor(255, 0, 0))
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.DashLine)
        self.setPen(self.pen01)

    def print_event(self, qt_event):
        """
        :param qt_event: PyQt5.QtWidgets.QGraphicsSceneMouseEvent
        :return:
        """
        print('------------------print_event starts---------------------------------------')
        print('------------------source---------------------------------------')
        # 0: NotSynthesized; 1, SynthesizedBySystem; 2, SynthesizedByQt; 3, SynthesizedByApplication;
        print(qt_event.source())  # PyQt5.QtCore.Qt.MouseEventSource
        print('------------------position---------------------------------------')
        print('item coordinate: %s' % qt_event.pos())  # QPointF
        print('last record in item coordinate: %s' % qt_event.lastPos())  # # QPointF; used in QMouseMoveEvent
        print('scene coordinate: %s' % qt_event.scenePos())  # QPointF
        print('screen coordinate: %s' % qt_event.screenPos())  # QPoint
        print('------------------button type---------------------------------------')
        # 0: not a button action; 1: left; 2: right; 3, middle;
        print(qt_event.button())  # PyQt5.QtCore.Qt.MouseButton
        print('------------------print_event ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        print('------------------mousePressEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_left_click.emit(args[0].pos())
        print('------------------mousePressEvent of %s ends-----------------------------' % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        # print('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_move01.emit(args[0].pos())
        # print('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        print('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        # print(args)
        # print(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_left_click_release.emit(args[0].pos())
        print('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)

    def hoverEnterEvent(self, *args, **kwargs):
        print('------------------hoverEnterEvent of %s starts-----------------------------' % self.__class__)
        # print(self.hasCursor())  # Originally it is False;
        self.setCursor(Qt.CrossCursor)
        # print(self.hasCursor())
        print('------------------hoverEnterEvent of %s ends-----------------------------' % self.__class__)

    def hoverLeaveEvent(self, *args, **kwargs):
        print('------------------hoverLeaveEvent of %s starts-----------------------------' % self.__class__)
        self.setCursor(Qt.ArrowCursor)
        print('------------------hoverLeaveEvent of %s ends-----------------------------' % self.__class__)

    def resetting_size(self, x, y, width, height):
        self.rect4update = QRectF(x, y, width, height)
        self.setRect(self.rect4update)


class PicWidget02_mask02(QGraphicsRectItem):
    """
    Originally, it is stacked on top of another QGraphicsItem (PicWidget02 class)
    Compared with PicWidget02_mask01, the logging model is first introduced to this class.
    """
    def __init__(self, x, y, width, height, parent=None):
        super().__init__()
        self.setAcceptHoverEvents(True)  # enable the item to accept hover events
        self.setZValue(1)
        self.setVisible(False)

        # pen
        self.color01 = QColor(0, 255, 0)
        self.pen01 = QPen(self.color01)
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.SolidLine)
        self.setPen(self.pen01)
        #
        self.rect4update = QRectF(x, y, width, height)
        self.setRect(self.rect4update)
        #
        self.parent = parent
        self.signals = PicWidget02_mask01_signals01(parent=None)
        self.mylogging4picwidget02_mask02 = MyLogging1_2(logger_name='hobin')

        # self.test_work01()

    def test_work01(self):
        """
        visualization of this rectangle
        :return:
        """
        self.setVisible(True)  # It is invisible in this application by default
        self.pen01 = QPen(QColor(255, 0, 0))
        self.pen01.setWidth(3)  # unit: pixel
        self.pen01.setStyle(Qt.DashLine)
        self.setPen(self.pen01)

    def print_event(self, qt_event):
        """
        :param qt_event: PyQt5.QtWidgets.QGraphicsSceneMouseEvent
        :return:
        """
        self.mylogging4picwidget02_mask02.logger.info('------------------print_event starts---------------------------------------')
        self.mylogging4picwidget02_mask02.logger.debug('------------------source---------------------------------------')
        # 0: NotSynthesized; 1, SynthesizedBySystem; 2, SynthesizedByQt; 3, SynthesizedByApplication;
        self.mylogging4picwidget02_mask02.logger.debug(qt_event.source())  # PyQt5.QtCore.Qt.MouseEventSource
        self.mylogging4picwidget02_mask02.logger.debug('------------------position---------------------------------------')
        self.mylogging4picwidget02_mask02.logger.debug('item coordinate: %s' % qt_event.pos())  # QPointF
        self.mylogging4picwidget02_mask02.logger.debug('last record in item coordinate: %s' % qt_event.lastPos())  # # QPointF; used in QMouseMoveEvent
        self.mylogging4picwidget02_mask02.logger.debug('scene coordinate: %s' % qt_event.scenePos())  # QPointF
        self.mylogging4picwidget02_mask02.logger.debug('screen coordinate: %s' % qt_event.screenPos())  # QPoint
        self.mylogging4picwidget02_mask02.logger.debug('------------------button type---------------------------------------')
        # 0: not a button action; 1: left; 2: right; 3, middle;
        self.mylogging4picwidget02_mask02.logger.debug(qt_event.button())  # PyQt5.QtCore.Qt.MouseButton
        self.mylogging4picwidget02_mask02.logger.info('------------------print_event ends---------------------------------------')

    def mousePressEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        self.mylogging4picwidget02_mask02.logger.info('------------------mousePressEvent of %s starts-----------------'
                                                      % self.__class__)
        # self.mylogging4picwidget02_mask02.logger.(args)
        # self.mylogging4picwidget02_mask02.logger.(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_left_click.emit(args[0].pos())
        self.mylogging4picwidget02_mask02.logger.info('------------------mousePressEvent of %s ends-----------------'
                                                      % self.__class__)

    def mouseMoveEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        self.mylogging4picwidget02_mask02.logger.info('------------------mouseMoveEvent of %s starts-----------------------------' % self.__class__)
        # self.mylogging4picwidget02_mask02.logger.debug(args)
        # self.mylogging4picwidget02_mask02.logger.debug(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_move01.emit(args[0].pos())
        self.mylogging4picwidget02_mask02.logger.info('------------------mouseMoveEvent of %s ends-----------------------------' % self.__class__)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        :param args: a tuple of PyQt5.QtWidgets.QGraphicsSceneMouseEvent object
        :param kwargs:
        :return:
        """
        self.mylogging4picwidget02_mask02.logger.info('------------------mouseReleaseEvent of %s starts-----------------------------' % self.__class__)
        # self.mylogging4picwidget02_mask02.logger.(args)
        # self.mylogging4picwidget02_mask02.logger.(kwargs)
        # self.print_event(args[0])
        self.signals.mouse_left_click_release.emit(args[0].pos())
        self.mylogging4picwidget02_mask02.logger.info('------------------mouseReleaseEvent of %s ends-----------------------------' % self.__class__)

    def hoverEnterEvent(self, *args, **kwargs):
        self.mylogging4picwidget02_mask02.logger.info('------------------hoverEnterEvent of %s starts-----------------------------' % self.__class__)
        # self.mylogging4picwidget02_mask02.logger.(self.hasCursor())  # Originally it is False;
        self.setCursor(Qt.CrossCursor)
        # self.mylogging4picwidget02_mask02.logger.(self.hasCursor())
        self.mylogging4picwidget02_mask02.logger.info('------------------hoverEnterEvent of %s ends-----------------------------' % self.__class__)

    def hoverLeaveEvent(self, *args, **kwargs):
        self.mylogging4picwidget02_mask02.logger.info('------------------hoverLeaveEvent of %s starts-----------------------------' % self.__class__)
        self.setCursor(Qt.ArrowCursor)
        self.mylogging4picwidget02_mask02.logger.info('------------------hoverLeaveEvent of %s ends-----------------------------' % self.__class__)

    def resetting_size(self, x, y, width, height):
        self.rect4update = QRectF(x, y, width, height)
        self.setRect(self.rect4update)

