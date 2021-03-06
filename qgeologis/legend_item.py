#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright (C) 2018 Oslandia <infos@oslandia.com>
#
#   This file is a piece of free software; you can redistribute it and/or
#   modify it under the terms of the GNU Library General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#   
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Library General Public License for more details.
#   You should have received a copy of the GNU Library General Public
#   License along with this library; if not, see <http://www.gnu.org/licenses/>.
#

from qgis.PyQt.QtCore import Qt, QRectF
from qgis.PyQt.QtGui import QFont, QFontMetrics

from .common import LogItem

class LegendItem(LogItem):
    # margin all around the whole legend item
    LEGEND_ITEM_MARGIN = 5
    # margin between title and legend line
    LEGEND_LINE_MARGIN = 4

    def __init__(self, width, title, min_value=None, max_value=None,
                 unit_of_measure=None, is_vertical=False, parent=None):
        LogItem.__init__(self, parent)
        self.__width = width
        self.__title = title
        self.__min_value = min_value
        self.__max_value = max_value
        self.__uom = unit_of_measure
        self.__is_vertical = is_vertical

        self.__selected = False

        # title font
        self.__font1 = QFont()
        self.__font1.setBold(True)
        self.__font1.setPointSize(10)

        # value font
        self.__font2 = QFont()
        self.__font2.setPointSize(9)

        fm1 = QFontMetrics(self.__font1)
        fm2 = QFontMetrics(self.__font2)
        self.__height = self.LEGEND_LINE_MARGIN * 3 + fm1.height() + fm2.height() + 10 + self.LEGEND_ITEM_MARGIN

    def set_scale(self, min_value, max_value):
        self.__min_value = min_value
        self.__max_value = max_value

    def boundingRect(self):
        if self.__is_vertical:
            return QRectF(0, 0, self.__height, self.__width)
        else:
            return QRectF(0, 0, self.__width, self.__height)

    def selected(self):
        return self.__selected

    def paint(self, painter, option, widget):
        self.draw_background(painter, outline=False)

        painter.save()
        if self.__is_vertical:
            painter.translate(self.__height/2, self.__width/2)
            painter.rotate(-90.0)
            painter.translate(-self.__width/2, -self.__height/2)

        painter.setFont(self.__font1)
        fm = painter.fontMetrics()
        # add "..." if needed
        title = fm.elidedText(self.__title, Qt.ElideRight, self.__width)
        w1 = (self.__width - fm.width(title)) / 2
        y = self.LEGEND_ITEM_MARGIN + fm.ascent()
        painter.drawText(w1, y, title)
        y += fm.descent() + self.LEGEND_LINE_MARGIN

        # legend line
        xmin = 0
        xmax = self.__width
        ymax = self.__height
        painter.drawLine(xmin, y+5, xmax, y+5)
        painter.drawLine(xmin, y, xmin, ymax)
        painter.drawLine(xmax, y, xmax, ymax)
        y+= 10 + self.LEGEND_LINE_MARGIN

        painter.setFont(self.__font2)
        fm = painter.fontMetrics()
        y += fm.ascent()

        if self.__min_value is not None:
            min_str = format_number(float(self.__min_value))
        if self.__max_value is not None:
            max_str = format_number(float(self.__max_value))

        # make sure min and max have distinct values
        if self.__min_value is not None and self.__max_value is not None:
            num_decimals = 1
            while min_str == max_str and num_decimals < 4:
                num_decimals +=1
                min_str = format_number(float(self.__min_value), num_decimals)
                max_str = format_number(float(self.__max_value), num_decimals)

        if self.__min_value is not None:
            painter.drawText(self.LEGEND_ITEM_MARGIN, y, min_str)
        if self.__max_value is not None:
            painter.drawText(self.__width - self.LEGEND_ITEM_MARGIN - fm.width(max_str), y, max_str)
        if self.__uom is not None:
            t = self.__uom
            painter.drawText((self.__width - fm.width(t)) /2, y, t)
        painter.restore()

def format_number(f, num_decimals = 1):
    if f < 10000:
        fmt = "{:." + "{}".format(num_decimals) + "f}"
        return fmt.format(f)
    else:
        return "{:.1e}".format(f)
