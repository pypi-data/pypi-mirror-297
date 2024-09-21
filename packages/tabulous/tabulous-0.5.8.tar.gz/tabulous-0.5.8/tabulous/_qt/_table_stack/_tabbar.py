from __future__ import annotations
from typing import TYPE_CHECKING
from qtpy import QtWidgets as QtW, QtGui, QtCore
from qtpy.QtCore import Qt

if TYPE_CHECKING:
    from ._tabwidget import QTabbedTableStack

# https://stackoverflow.com/questions/50578661/how-to-implement-vertical-tabs-in-qt


class QTabulousTabBar(QtW.QTabBar):
    def __init__(self, parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    # fmt: off
    if TYPE_CHECKING:
        def parentWidget(self) -> QTabbedTableStack: ...
    # fmt: on


class _QSideBar(QTabulousTabBar):
    _ROTATION_DEGREE: int

    def tabSizeHint(self, index: int) -> QtCore.QSize:
        s = super().tabSizeHint(index)
        s.transpose()
        s.setWidth(120)
        return s

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtW.QStylePainter(self)
        opt = QtW.QStyleOptionTab()

        TabBarTabShape = QtW.QStyle.ControlElement.CE_TabBarTabShape
        TabBarTabLabel = QtW.QStyle.ControlElement.CE_TabBarTabLabel
        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(TabBarTabShape, opt)

            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            tab_rect = self.tabRect(i)
            c = tab_rect.center()
            painter.translate(c)
            painter.rotate(self._ROTATION_DEGREE)
            painter.translate(-c)
            painter.drawControl(TabBarTabLabel, opt)
            painter.restore()

        QtW.QWidget.paintEvent(self, event)
        return None


class QLeftSideBar(_QSideBar):
    _ROTATION_DEGREE = 90


class QRightSideBar(_QSideBar):
    _ROTATION_DEGREE = 270
