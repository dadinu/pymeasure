#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

import pyqtgraph as pg
from ..curves import ResultsImage, Results3DImage, Results3DCurve
from ..Qt import QtCore, QtWidgets, QtGui
from qfluentwidgets import ComboBox, PrimaryPushButton
from qfluentwidgets import FluentIcon as FIF
from .tab_widget import TabWidget
from .image_frame import ImageFrame, Image3DFrame
from .plot_frame import Plot3DFrame
from copy import deepcopy

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ImageWidget(TabWidget, QtWidgets.QWidget):
    """ Extends the :class:`ImageFrame<pymeasure.display.widgets.image_frame.ImageFrame>`
    to allow different columns of the data to be dynamically chosen
    """
    sendROISignal = QtCore.pyqtSignal(object)

    def __init__(self, name, columns, x_axis, y_axis, z_axis=None, refresh_time=0.2,
                 check_status=True, roi_enable = False, target_enable = False, 
                 max_area_enable = False, max_area = None, parent=None):
        super().__init__(name, parent)
        self.columns = columns
        self.refresh_time = refresh_time
        self.check_status = check_status
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.roi_enable = roi_enable
        self.target_enable = target_enable
        self.max_area_enable = max_area_enable
        self.max_area = max_area
        self._setup_ui()
        self._layout()
        if z_axis is not None:
            self.columns_z.setCurrentIndex(self.columns_z.findText(z_axis))
            self.image_frame.change_z_axis(z_axis)

    def _setup_ui(self):
        self.columns_z_label = QtWidgets.QLabel(self)
        self.columns_z_label.setMaximumSize(QtCore.QSize(45, 16777215))
        self.columns_z_label.setText('Z Axis:')

        self.columns_z = ComboBox(self)
        for column in self.columns:
            self.columns_z.addItem(column)
        self.columns_z.currentIndexChanged.connect(self.update_z_column)

        self.image_frame = ImageFrame(
            self.x_axis,
            self.y_axis,
            self.columns[0],
            self.refresh_time,
            self.check_status,
            self.roi_enable,
            self.target_enable,
            self.max_area_enable,
            self.max_area
        )

        if self.roi_enable: 
            self.setROIButton = PrimaryPushButton(FIF.LEFT_ARROW, "Send ROI")
            self.setROIButton.clicked.connect(self.__onSetROIButtonClicked)
            
        self.updated = self.image_frame.updated
        self.plot = self.image_frame.plot
        self.columns_z.setCurrentIndex(2)

    def _layout(self):
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.setSpacing(0)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(10)
        hbox.setContentsMargins(-1, 6, -1, 6)
        hbox.addWidget(self.columns_z_label)
        hbox.addWidget(self.columns_z)

        if self.roi_enable: hbox.addWidget(self.setROIButton)

        vbox.addLayout(hbox)
        vbox.addWidget(self.image_frame)
        self.setLayout(vbox)

    def sizeHint(self):
        return QtCore.QSize(300, 600)

    def new_curve(self, results, color=pg.intColor(0), **kwargs):
        """ Creates a new image """
        image = ResultsImage(results,
                             wdg=self,
                             x=self.image_frame.x_axis,
                             y=self.image_frame.y_axis,
                             z=self.image_frame.z_axis,
                             **kwargs
                             )
        return image

    def update_z_column(self, index):
        axis = self.columns_z.itemText(index)
        self.image_frame.change_z_axis(axis)

    def load(self, curve):
        curve.z = self.columns_z.currentText()
        curve.update_data()
        self.plot.addItem(curve)

    def remove(self, curve):
        self.plot.removeItem(curve)

    def __onSetROIButtonClicked(self):
        self.sendROISignal.emit((*self.image_frame.roi.pos(),*self.image_frame.roi.size()))

class Image3DWidget(TabWidget, QtWidgets.QWidget):
    """ Extends the :class:`ImageFrame<pymeasure.display.widgets.image_frame.ImageFrame>`
    to allow different columns of the data to be dynamically chosen
    """
    sendROISignal = QtCore.pyqtSignal(object)

    def __init__(self, name, columns, x_axis, y_axis, z_axis, var_axis = None, refresh_time=0.2,
                 check_status=True, linewidth = 1, roi_enable = False, target_enable = False, 
                 max_area_enable = False, max_area = None, parent=None):
        super().__init__(name, parent)
        self.columns = columns
        self.refresh_time = refresh_time
        self.check_status = check_status
        self.linewidth = linewidth
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis
        self.roi_enable = roi_enable
        self.target_enable = target_enable
        self.max_area_enable = max_area_enable
        self.max_area = max_area
        self._setup_ui()
        self._layout()
        if var_axis is not None:
            self.columns_var.setCurrentIndex(self.columns_var.findText(var_axis))
            self.image3D_frame.change_var_axis(var_axis)

    def _setup_ui(self):
        self.columns_var_label = QtWidgets.QLabel(self)
        self.columns_var_label.setMaximumSize(QtCore.QSize(45, 16777215))
        self.columns_var_label.setText('Var Axis:')

        self.columns_var = ComboBox(self)
        for column in self.columns:
            self.columns_var.addItem(column)
        self.columns_var.currentIndexChanged.connect(self.update_var_column)

        self.image3D_frame = Image3DFrame(
            self.x_axis,
            self.y_axis,
            self.z_axis,
            self.columns[0],
            self.refresh_time,
            self.check_status,
            self.roi_enable,
            self.target_enable,
            self.max_area_enable,
            self.max_area
        )

        self.plot3D_frame = Plot3DFrame(
            self.z_axis,
            self.columns[0],
            self.refresh_time,
            self.check_status
        )

        self.plot3D_frame.slider_moved.connect(self.image3D_frame.change_shown_zidx)
        self.image3D_frame.target_changed.connect(self.plot3D_frame.change_shown_xidx_yidx)
        if self.roi_enable: 
            self.setROIButton = PrimaryPushButton(FIF.LEFT_ARROW, "Send ROI")
            self.setROIButton.clicked.connect(self.__onSetROIButtonClicked)
            
        self.updated = self.image3D_frame.updated
        self.plot3D = self.image3D_frame.plot
        self.plot = self.plot3D_frame.plot
        self.columns_var.setCurrentIndex(2)

    def _layout(self):
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.setSpacing(0)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(10)
        hbox.setContentsMargins(-1, 6, -1, 6)
        hbox.addWidget(self.columns_var_label)
        hbox.addWidget(self.columns_var)

        if self.roi_enable: hbox.addWidget(self.setROIButton)

        vbox.addLayout(hbox)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.image3D_frame)
        hbox2.addWidget(self.plot3D_frame)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    def sizeHint(self):
        return QtCore.QSize(300, 600)

    def new_curve(self, results, color=pg.intColor(0), **kwargs):
        """ Creates a new image """
        image = Results3DImage(results,
                             wdg=self,
                             x=self.image3D_frame.x_axis,
                             y=self.image3D_frame.y_axis,
                             z=self.image3D_frame.z_axis,
                             var=self.image3D_frame.var_axis,
                             parent = self,
                             **kwargs
                             )
        if 'pen' not in kwargs:
            kwargs['pen'] = pg.mkPen(color=color, width=self.linewidth)
        if 'antialias' not in kwargs:
            kwargs['antialias'] = False
        
        curve = Results3DCurve(results,
                               wdg = self,
                               z = self.plot3D_frame.x_axis,
                               var = self.plot3D_frame.y_axis,
                               **kwargs)
        return curve, image

    def update_var_column(self, index):
        axis = self.columns_var.itemText(index)
        self.image3D_frame.change_var_axis(axis)

    def load(self, curve):
        curve.var = self.columns_var.currentText()
        curve.update_data()
        if isinstance(curve, Results3DImage):
            self.image3D_frame.plot.addItem(curve)
        if isinstance(curve, Results3DCurve):
            self.plot3D_frame.plot.addItem(curve)

    def remove(self, curve):
        self.plot.removeItem(curve)
        self.plot3D.removeItem(curve)

    def __onSetROIButtonClicked(self):
        self.sendROISignal.emit((*self.image3D_frame.roi.pos(),*self.image3D_frame.roi.size()))
