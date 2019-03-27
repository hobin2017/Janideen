# -*- coding: utf-8 -*-
"""

"""

import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QFrame, QColorDialog


class ColorMapper01(object):
    
    def __init__(self):
        super().__init__()
        self.id2index_dict = {}
        self.color_list = [
            QColor(255,175,207),
            QColor(85, 85, 127), QColor(255, 85, 127), QColor(85, 170, 127), QColor(255, 170, 127), QColor(85, 255, 127),
            QColor(170, 170, 255), QColor(0, 255, 255), QColor(170, 255, 255), QColor(85, 85, 0), QColor(255, 85, 0),
            QColor(85, 170, 0), QColor(255, 170, 0), QColor(85, 255, 0), QColor(255, 255, 0), QColor(255, 0, 127),
            QColor(170, 170, 127), QColor(170, 0, 255), QColor(0, 85, 255),  QColor(0, 170, 255),
            QColor(170, 255, 0), QColor(170, 0, 127), QColor(0, 85, 127), QColor(170, 85, 127), QColor(0, 170, 127),
            QColor(0,85,0), QColor(170,85,0), QColor(0,170,0), QColor(170,170,0), QColor(0,255,0),
            QColor(255,255,127), QColor(85,0,255), QColor(255,0,255), QColor(85,85,255), QColor(255,85,255),
            QColor(85,170,255), QColor(255,170,255), QColor(85,255,255),
        ]
        # print('total number of color list: %s' % len(self.color_list))
        self.used_index = 0
    
    
    def cv_id2color(self, cv_id):
        """
        :param cv_id: str
        :return: 
        """
        if self.id2index_dict.get(cv_id, None):
            return self.id2index_dict[cv_id]
        else:
            self.id2index_dict[cv_id] = self.color_list[self.used_index]
            self.used_index = (self.used_index + 1) % len(self.color_list)
            return self.id2index_dict[cv_id]


class MyWindow(QColorDialog):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.layout_init()
        self.layout_manage()


    def layout_init(self):
        pass

    def layout_manage(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
