from __future__ import annotations

from qtpy import QtWidgets as QtW, QtCore
from qtpy.QtCore import Qt, Signal


class QTitleBar(QtW.QWidget):
    """A custom title bar for a QSplitterDockWidget"""

    closeSignal = Signal()

    def __init__(self, title: str = "", parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)
        _layout = QtW.QHBoxLayout()
        _layout.setContentsMargins(4, 0, 4, 0)
        _layout.setSpacing(0)

        self._title_label = QtW.QLabel()
        self._title_label.setContentsMargins(0, 0, 0, 0)

        _frame = QtW.QFrame()
        _frame.setFrameShape(QtW.QFrame.Shape.HLine)
        _frame.setFrameShadow(QtW.QFrame.Shadow.Sunken)
        _frame.setSizePolicy(
            QtW.QSizePolicy.Policy.Expanding, QtW.QSizePolicy.Policy.Fixed
        )
        self._close_button = QtW.QToolButton()
        self._close_button.setText("✕")
        self._close_button.setToolTip("Close the widget.")
        self._close_button.setFixedSize(QtCore.QSize(16, 16))
        self._close_button.setCursor(Qt.CursorShape.ArrowCursor)

        _layout.addWidget(self._title_label)
        _layout.addWidget(_frame)
        _layout.addWidget(self._close_button)
        _layout.setAlignment(self._close_button, Qt.AlignmentFlag.AlignRight)
        self.setLayout(_layout)

        self._close_button.clicked.connect(self.closeSignal.emit)

        self.setTitle(title)
        self.setFixedHeight(18)

    def title(self) -> str:
        """The title text."""
        return self._title_label.text()

    def setTitle(self, text: str):
        """Set the title text."""
        if text == "":
            self._title_label.setVisible(False)
        else:
            self._title_label.setVisible(True)
            self._title_label.setText(f"  {text}  ")

    def setBold(self, bold: bool):
        """Set the title text bold."""
        font = self._title_label.font()
        font.setBold(bold)
        self._title_label.setFont(font)
