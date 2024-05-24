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

from ..curves import ResultsImage, Results3DImage
from ..Qt import QtCore
from .plot_frame import PlotFrame
import pyqtgraph as pg

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ImageFrame(PlotFrame):
    """ Extends :class:`PlotFrame<pymeasure.display.widgets.plot_frame.PlotFrame>`
    to plot also axis Z using colors
    """
    ResultsClass = ResultsImage
    z_axis_changed = QtCore.Signal(str)

    def __init__(self, x_axis, y_axis, z_axis=None,
                 refresh_time=0.2, check_status=True, roi_enable = False, target_enable = False,
                max_area_enable = False, max_area = None, parent=None):
        super().__init__(x_axis, y_axis, refresh_time, check_status, target_enable, max_area_enable, max_area, parent)
        self.change_z_axis(z_axis)
        if roi_enable:
            self.roi = pg.RectROI((0,0), (3,3))
            self.plot_widget.addItem(self.roi)

    def change_z_axis(self, axis):
        for item in self.plot.items:
            if isinstance(item, self.ResultsClass):
                item.z = axis
                item.update_data()
        label, units = self.parse_axis(axis)
        if units is not None:
            self.plot.setTitle(label + ' (%s)' % units)
        else:
            self.plot.setTitle(label)
        self.z_axis = axis
        self.z_axis_changed.emit(axis)

class Image3DFrame(PlotFrame):
    """ Extends :class:`PlotFrame<pymeasure.display.widgets.plot_frame.PlotFrame>`
    to plot also axis Z and var using colors.
    """
    ResultsClass = Results3DImage
    var_axis_changed = QtCore.Signal(str)
    target_changed = QtCore.Signal(object)

    def __init__(self, x_axis, y_axis, z_axis, var_axis = None,
                 refresh_time=0.2, check_status=True, roi_enable = False, target_enable = False,
                max_area_enable = False, max_area = None, parent=None):
        super().__init__(x_axis, y_axis, refresh_time, check_status, target_enable, max_area_enable, max_area, parent)
        self.z_axis = z_axis
        self.change_var_axis(var_axis)
        if roi_enable:
            self.roi = pg.RectROI((0,0), (3,3))
            self.plot_widget.addItem(self.roi)

    def change_shown_zidx(self, zidx):
        index = 0
        if len(zidx) != 0:
            for item in self.plot.items:
                if isinstance(item, self.ResultsClass):
                    item.shown_zidx = zidx[index]
                    item.update_data()
                    index += 1

    def change_var_axis(self, axis):
        for item in self.plot.items:
            if isinstance(item, self.ResultsClass):
                item.var = axis
                item.update_data()
        label, units = self.parse_axis(axis)
        if units is not None:
            self.plot.setTitle(label + ' (%s)' % units)
        else:
            self.plot.setTitle(label)
        self.var_axis = axis
        self.var_axis_changed.emit(axis)

    def change_target(self, x, y):
        super().change_target(x, y)
        closest_points = []
        for item in self.plot.items:
            if isinstance(item, self.ResultsClass):
                if self.check_status:
                    xid, yid, _  = item.find_img_index(x,y,0)
                    closest_points.append((xid, yid))
        self.target_changed.emit(closest_points)