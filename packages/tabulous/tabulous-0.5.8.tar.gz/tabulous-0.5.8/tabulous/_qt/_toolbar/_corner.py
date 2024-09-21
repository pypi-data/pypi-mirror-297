from __future__ import annotations

from qtpy import QtWidgets as QtW, QtGui, QtCore
from qtpy.QtCore import Qt, Signal


class QIntOrNoneValidator(QtGui.QIntValidator):
    def validate(self, input: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
        if input == "":
            return QtGui.QValidator.State.Acceptable, input, pos
        return super().validate(input, pos)


class QIntOrNoneEdit(QtW.QLineEdit):
    def __init__(self, parent: QtW.QWidget | None = None):
        super().__init__(parent)
        self.setValidator(QIntOrNoneValidator())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textChanged.connect(self.ensureVisible)
        self.setSizePolicy(
            QtW.QSizePolicy.Policy.Minimum, QtW.QSizePolicy.Policy.Expanding
        )

    def value(self):
        return int(self.text()) if self.text() else None

    def setValue(self, val: int | None):
        self.setText(str(val) if val is not None else "")

    def increment(self):
        val = self.value()
        if val is not None:
            self.setValue(val + 1)

    def decrement(self):
        val = self.value()
        if val is not None:
            self.setValue(max(val - 1, 0))

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Type.KeyPress:
            event = QtGui.QKeyEvent(event)
            key = event.key()
            mod = event.modifiers()
            if mod != Qt.KeyboardModifier.NoModifier:
                return super().event(event)
            if key == Qt.Key.Key_Up:
                self.increment()
                return True
            elif key == Qt.Key.Key_Down:
                self.decrement()
                return True

        return super().event(event)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if a0.angleDelta().y() > 0:
            self.increment()
        else:
            self.decrement()
        return super().wheelEvent(a0)

    def ensureVisible(self, text: str) -> QtCore.QSize:
        metrics = QtGui.QFontMetrics(self.font())
        w = metrics.width("9") * len(text) + 6
        self.setFixedWidth(w)


class QSelectionRangeEdit(QtW.QWidget):
    sliceChanged = Signal(object)
    editingFinished = Signal()

    def __init__(self, parent: QtW.QWidget | None = None):
        super().__init__(parent)
        self.setLayout(QtW.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        inner = QtW.QWidget()
        self.layout().addWidget(inner)
        layout = QtW.QHBoxLayout()
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)
        inner.setLayout(layout)
        self._r_start = QIntOrNoneEdit()
        self._r_stop = QIntOrNoneEdit()
        self._c_start = QIntOrNoneEdit()
        self._c_stop = QIntOrNoneEdit()
        self._r_start.setToolTip("Row starting index")
        self._r_stop.setToolTip("Row stopping index")
        self._c_start.setToolTip("Column starting index")
        self._c_stop.setToolTip("Column stopping index")
        self._r_start.textChanged.connect(self._rstart_changed)
        self._r_colon = _label(":")
        self._r_stop.textChanged.connect(self._rstop_changed)
        self._c_start.textChanged.connect(self._cstart_changed)
        self._c_colon = _label(":")
        self._c_stop.textChanged.connect(self._cstop_changed)
        layout.addWidget(self._r_start)
        layout.addWidget(self._r_colon)
        layout.addWidget(self._r_stop)
        layout.addWidget(_label(", "))
        layout.addWidget(self._c_start)
        layout.addWidget(self._c_colon)
        layout.addWidget(self._c_stop)

        self._r_start.editingFinished.connect(self.editingFinished.emit)
        self._r_stop.editingFinished.connect(self.editingFinished.emit)
        self._c_start.editingFinished.connect(self.editingFinished.emit)
        self._c_stop.editingFinished.connect(self.editingFinished.emit)

    def slice(self) -> tuple[slice, slice]:
        rsl = slice(self._r_start.value(), self._r_stop.value())
        csl = slice(self._c_start.value(), self._c_stop.value())
        return rsl, csl

    def setSlice(self, sl: tuple[slice, slice]):
        rsl, csl = sl
        rstart, rstop = rsl.start, rsl.stop
        cstart, cstop = csl.start, csl.stop
        self._r_start.setValue(rstart)
        self._r_stop.setValue(rstop)
        self._c_start.setValue(cstart)
        self._c_stop.setValue(cstop)
        if rstart is not None and rstop is not None and rstop == rstart + 1:
            self._r_stop.hide()
            self._r_colon.hide()
        else:
            self._r_stop.show()
            self._r_colon.show()
        if cstart is not None and cstop is not None and cstop == cstart + 1:
            self._c_stop.hide()
            self._c_colon.hide()
        else:
            self._c_stop.show()
            self._c_colon.show()
        return None

    def _rstart_changed(self, txt: str):
        rstop = self._r_stop.text()
        if txt and rstop:
            if not self._r_stop.isVisible() or int(rstop) <= int(txt):
                self._r_stop.setText(str(int(txt) + 1))
        return self.sliceChanged.emit(self.slice())

    def _rstop_changed(self, txt: str):
        rstart = self._r_start.text()
        if txt and rstart and int(rstart) >= int(txt):
            int_rstop = int(txt)
            if int_rstop > 1:
                self._r_start.setText(str(int_rstop - 1))
            else:
                self._r_start.setText("0")
                self._r_stop.setText("1")
        return self.sliceChanged.emit(self.slice())

    def _cstart_changed(self, txt: str):
        cstop = self._c_stop.text()
        if txt and cstop:
            if not self._c_stop.isVisible() or int(cstop) <= int(txt):
                self._c_stop.setText(str(int(txt) + 1))
        return self.sliceChanged.emit(self.slice())

    def _cstop_changed(self, txt: str):
        cstart = self._c_start.text()
        if txt and cstart and int(cstart) >= int(txt):
            int_cstop = int(txt)
            if int_cstop > 1:
                self._c_start.setText(str(int_cstop - 1))
            else:
                self._c_start.setText("0")
                self._c_stop.setText("1")
        return self.sliceChanged.emit(self.slice())


def _label(text: str):
    label = QtW.QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label
