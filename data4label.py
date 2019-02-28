# -*- coding: utf-8 -*-
"""

"""

from xml.etree import ElementTree


class ObjectElement01(ElementTree.Element):

    def __init__(self, tag_name='object', name='hobin', truncated='0', difficult='0', xmin='0', ymin='0', xmax='0', ymax='0'):
        super().__init__(tag_name)
        first_name = ElementTree.Element('name')
        first_name.text = name
        self.append(first_name)

        first_pose = ElementTree.Element('pose')
        first_pose.text = 'Unspecified'
        self.append(first_pose)

        first_truncated = ElementTree.Element('truncated')
        first_truncated.text = truncated
        self.append(first_truncated)

        first_difficult = ElementTree.Element('difficult')
        first_difficult.text = difficult
        self.append(first_difficult)

        first_bndbox = ElementTree.Element('bndbox')
        self.append(first_bndbox)

        second_xmin = ElementTree.Element('xmin')
        second_xmin.text = xmin
        first_bndbox.append(second_xmin)

        second_ymin = ElementTree.Element('ymin')
        second_ymin.text = ymin
        first_bndbox.append(second_ymin)

        second_xmax = ElementTree.Element('xmax')
        second_xmax.text = xmax
        first_bndbox.append(second_xmax)

        second_ymax = ElementTree.Element('ymax')
        second_ymax.text = ymax
        first_bndbox.append(second_ymax)


class RootElement01(ElementTree.Element):

    def __init__(self, tag_name='annotation', folder='VOC2007', filename='test.jpg', path='/home/commaai/test.jpg',
                 database='unknown', hard='0', width='0', height='0', depth='0', segmented='0'):
        super().__init__(tag_name)
        # the first way to create a sub-element by using ElementTree.Element()
        first_folder = ElementTree.Element('folder')  # storing to self.first_folder will raise error!
        first_folder.text = folder
        self.append(first_folder)

        first_filename = ElementTree.Element('filename')
        first_filename.text = filename
        self.append(first_filename)

        first_path = ElementTree.Element('path')
        first_path.text = path
        self.append(first_path)
        #
        first_source = ElementTree.Element('source')
        self.append(first_source)
        second_database = ElementTree.Element('database')
        second_database.text = database
        first_source.append(second_database)

        first_hard = ElementTree.Element('hard')
        first_hard.text = hard
        self.append(first_hard)

        #
        first_size = ElementTree.Element('size')
        self.append(first_size)
        second_width = ElementTree.Element('width')
        second_width.text = width
        first_size.append(second_width)
        second_height = ElementTree.Element('height')
        second_height.text = height
        first_size.append(second_height)
        second_depth = ElementTree.Element('depth')
        second_depth.text = depth
        first_size.append(second_depth)
        first_segmented = ElementTree.Element('segmented')
        first_segmented.text = segmented
        self.append(first_segmented)


if __name__ == '__main__':
    a = RootElement01()
    b = ObjectElement01()
    a.append(b)
    ElementTree.dump(a)  # print

