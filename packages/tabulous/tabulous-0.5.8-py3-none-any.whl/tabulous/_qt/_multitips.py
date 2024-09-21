from __future__ import annotations
from qtpy import QtWidgets as QtW, QtCore
from qtpy.QtCore import Qt


class QHasToolTip(QtW.QWidget):
    """A trait for a widget that has multiple tooltips."""

    _labels: list[QKeyComboTip] = []

    def toolTipPosition(self, index: int) -> QtCore.QPoint:
        """Return the position of the tooltip for the given index."""
        raise NotImplementedError()

    def toolTipText(self, index: int) -> str:
        """Return the text of the tooltip for the given index."""
        if 0 <= index < 9:
            return str(index + 1)
        elif index == 9:
            return "0"
        else:
            raise ValueError("Index must be between 0 and 9.")

    def toolTipCount(self) -> int:
        """Return the number of tooltips."""
        raise NotImplementedError()

    def showTabTooltips(self):
        """Show all the tooltips."""
        self._labels = []
        num = min(self.toolTipCount(), 10)
        for i in range(num):
            label = QKeyComboTip(self.toolTipText(i), self)
            pos = self.toolTipPosition(i)
            label.move(self.mapToGlobal(pos))
            label.show()
            self._labels.append(label)

    def hideTabTooltips(self):
        """Hide all the tooltips."""
        for label in self._labels:
            label.hide()
        self._labels = []


class QKeyComboTip(QtW.QLabel):
    def __init__(self, text: str, parent=None, size=14):
        super().__init__(text, parent, Qt.WindowType.ToolTip)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
        self.setFixedSize(size + 4, size + 4)
        self.setStyleSheet("border: 1px solid gray;")
        self.hide()
