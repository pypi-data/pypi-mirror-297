from typing import Callable, Iterable

from qtpy import QtWidgets as QtW, QtGui
from superqt import QEnumComboBox

from magicgui import magic_factory
from ._distribution import Distributions
from ._latex import QLatexLabel
from tabulous._selection_op import SelectionOperator
from tabulous._magicgui import find_table_viewer_ancestor


class QScipyStatsWidget(QtW.QWidget):
    def __init__(self, parent: QtW.QWidget | None = None):
        super().__init__(parent)
        _layout = QtW.QVBoxLayout()
        self._dist = QEnumComboBox(enum_class=Distributions)
        self._dist.setCurrentEnum(Distributions.norm)
        self._latex_label = QLatexLabel(Distributions.norm.latex)
        if parent is not None:
            self._latex_label.setTextColor(
                parent.palette().color(QtGui.QPalette.ColorRole.Text)
            )
        self._params = QStatsParameterWidget(Distributions.norm.params)
        _layout.addWidget(self._dist)
        _layout.addWidget(self._latex_label)
        _area = QtW.QScrollArea()
        _area.setContentsMargins(0, 0, 0, 0)
        _area.setWidget(self._params)
        _area.setFixedHeight(68)
        _layout.addWidget(_area)
        _layout.addWidget(_button("Fit", self.fit))
        _layout.addWidget(_button("Random sampling", self.sample))
        _layout.addWidget(_button("Calculate PDF", self.pdf))
        _layout.addWidget(_button("Calculate CDF", self.cdf))

        self.setLayout(_layout)
        self._dist.currentEnumChanged.connect(self._dist_changed)

    def _dist_changed(self, dist: Distributions):
        self._latex_label.setLatex(dist.latex)
        self._params.set_labels(dist.params)

    def get_instance(self, frozen: bool = True):
        dist: Distributions = self._dist.currentEnum()
        if frozen:
            return dist.dist(*self._params.get_params())
        return dist.dist

    def get_viewer(self):
        return find_table_viewer_ancestor(self)

    def fit(self):
        viewer = self.get_viewer()
        mgui = get_selection()
        mgui.native.setParent(self, mgui.native.windowFlags())
        mgui.show()

        @mgui.called.connect
        def _on_called(sel: SelectionOperator):
            dist = self.get_instance(frozen=False)
            df = sel.operate(viewer.current_table.data_shown)
            params_fit = dist.fit(df.values)
            self._params.set_params(params_fit)
            mgui.close()

    def sample(self):
        """Generate random samples from the distribution."""
        viewer = self.get_viewer()
        mgui = get_selection(selection={"allow_out_of_bounds": True})
        mgui.native.setParent(self, mgui.native.windowFlags())
        mgui.show()

        @mgui.called.connect
        def _on_called(sel: SelectionOperator):
            dist = self.get_instance()
            rsel, csel = sel.as_iloc(None)
            if rsel.stop is None or csel.stop is None:
                raise ValueError(
                    "Unknown shape of selection. You must specify the stop values "
                    "of the slices."
                )
            if rsel.step is not None or csel.step is not None:
                raise ValueError("Step values are not allowed.")
            rsize = rsel.stop - (rsel.start or 0)
            csize = csel.stop - (csel.start or 0)
            out = dist.rvs(rsize * csize).reshape((rsize, csize))
            viewer.current_table.cell[rsel, csel] = out
            mgui.close()

    def cdf(self):
        """Calculate the Cumulative Distribution Function (CDF)."""
        viewer = self.get_viewer()
        df = viewer.current_table.data_shown
        mgui = get_xy_selections(y={"allow_out_of_bounds": True})
        mgui.native.setParent(self, mgui.native.windowFlags())
        mgui.show()

        @mgui.called.connect
        def _on_called(xy: tuple[SelectionOperator, SelectionOperator]):
            xsel, ysel = xy
            dist = self.get_instance()
            ds = xsel.operate(df)
            out = dist.cdf(ds.values.ravel())
            viewer.current_table.cell[ysel.as_iloc(df)] = out
            mgui.close()

    def pdf(self):
        """Calculate the Probability Density Function (PDF)."""
        viewer = self.get_viewer()
        df = viewer.current_table.data_shown
        mgui = get_xy_selections(y={"allow_out_of_bounds": True})
        mgui.native.setParent(self, mgui.native.windowFlags())
        mgui.show()

        @mgui.called.connect
        def _on_called(xy: tuple[SelectionOperator, SelectionOperator]):
            xsel, ysel = xy
            dist = self.get_instance()
            ds = xsel.operate(df)
            out = dist.pdf(ds.values.ravel())
            viewer.current_table.cell[ysel.as_iloc(df)] = out
            mgui.close()


class QStatsParameterWidget(QtW.QWidget):
    def __init__(
        self, labels: Iterable[str], parent: QtW.QWidget | None = None
    ) -> None:
        super().__init__(parent)
        _layout = QtW.QFormLayout()
        self._widgets: list[QtW.QLineEdit] = []
        self.setLayout(_layout)
        self.set_labels(labels)

    def get_params(self) -> list[float]:
        return [float(wdt.text()) for wdt in self._widgets]

    def set_params(self, param: Iterable[float]) -> None:
        for wdt, p in zip(self._widgets, param):
            wdt.setText(str(p))

    def set_labels(self, labels: Iterable[str]) -> None:
        layout: QtW.QFormLayout = self.layout()
        while layout.rowCount() > 0:
            layout.removeRow(0)
        self._widgets: list[QtW.QLineEdit] = []
        for label in labels:
            wdt = QtW.QLineEdit()
            self._widgets.append(wdt)
            layout.addRow(label, wdt)


def _button(text: str, slot: Callable) -> QtW.QPushButton:
    btn = QtW.QPushButton(text)
    btn.clicked.connect(slot)
    btn.setToolTip(slot.__doc__)
    return btn


@magic_factory
def get_selection(selection: SelectionOperator):
    return selection


@magic_factory
def get_xy_selections(
    x: SelectionOperator,
    y: SelectionOperator,
):
    return x, y
