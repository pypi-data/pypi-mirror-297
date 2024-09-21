from functools import partial
from typing import List, Union, TYPE_CHECKING, Tuple

import logging
import ast
import numpy as np

# NOTE: Axes should be imported here!
from tabulous.widgets import TableBase, TableViewerBase
from tabulous.types import TableData
from tabulous.exceptions import SelectionRangeError
from tabulous._selection_op import SelectionOperator
from tabulous._magicgui import dialog_factory, dialog_factory_mpl, Axes, ToggleSwitch
from typing_extensions import Annotated

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)
_bool = Annotated[bool, {"widget_type": ToggleSwitch}]


@dialog_factory
def summarize_table(
    table: TableBase,
    methods: List[str],
    new_table: _bool = False,
    at_selection: _bool = False,
):
    if len(methods) == 0:
        raise ValueError("Select at least one method.")
    df = table.data
    if at_selection:
        sels = table.selections
        if len(sels) != 1:
            raise SelectionRangeError("Only single selection is allowed.")
        sel = sels[0]
        df = df.iloc[sel]
    return df.agg(methods), new_table


@dialog_factory
def cut(df: TableData, column: str, bins: str, close_right: _bool = True) -> TableData:
    import pandas as pd

    bins = ast.literal_eval(bins)
    ds = pd.cut(df[column], bins=bins, right=close_right)
    return ds


@dialog_factory
def concat(
    viewer: TableViewerBase,
    names: List[str],
    axis: int,
    ignore_index: _bool = False,
) -> TableData:
    import pandas as pd

    if len(names) < 2:
        raise ValueError("At least two tables are required.")
    dfs = [viewer.tables[name].data for name in names]
    out: pd.DataFrame = pd.concat(dfs, axis=axis, ignore_index=ignore_index)
    if out.index.duplicated().any():
        out.index = range(out.index.size)
    if out.columns.duplicated().any():
        from tabulous._pd_index import char_range_index

        out.columns = char_range_index(out.columns.size)
    return out


@dialog_factory
def merge(
    merge: TableBase,
    with_: TableBase,
    how: str = "inner",
    on: List[str] = (),
) -> TableData:
    if merge is with_:
        raise ValueError("Cannot merge a table with itself.")
    df0 = merge.data
    df1 = with_.data
    if len(on) == 0:
        on = None
    return df0.merge(df1, how=how, on=on)


@dialog_factory
def fillna(df: TableData, method: str, value) -> TableData:
    if method != "value":
        value = None
    else:
        method = None
    return df.fillna(value=value, method=method)


@dialog_factory
def dropna(df: TableData, axis: int, how: str) -> TableData:
    return df.dropna(axis=axis, how=how, inplace=False)


@dialog_factory
def pivot(df: TableData, index: str, columns: str, values: str) -> TableData:
    return df.pivot(index=index, columns=columns, values=values)


@dialog_factory
def sort(df: TableData, by: List[str], ascending: _bool = True) -> TableData:
    return df.sort_values(by=by, ascending=ascending)


@dialog_factory_mpl
def plot(
    ax: Axes,
    x: SelectionOperator,
    y: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
    retain_reference: _bool = False,
):
    from ._plot_models import PlotModel

    model = PlotModel(ax, x, y, table=table, alpha=alpha, ref=retain_reference)
    model.add_data(table)
    table.plt.draw()
    return True


@dialog_factory_mpl
def bar(
    ax: Axes,
    x: SelectionOperator,
    y: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
    retain_reference: _bool = False,
):
    from ._plot_models import BarModel

    model = BarModel(ax, x, y, table=table, alpha=alpha, ref=retain_reference)
    model.add_data(table)
    table.plt.draw()
    return True


@dialog_factory_mpl
def scatter(
    ax: Axes,
    x: SelectionOperator,
    y: SelectionOperator,
    label: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
    retain_reference: _bool = False,
):
    from ._plot_models import ScatterModel

    model = ScatterModel(
        ax, x, y, table=table, label_selection=label, alpha=alpha, ref=retain_reference
    )
    model.add_data(table)
    table.plt.draw()
    return True


@dialog_factory_mpl
def errorbar(
    ax: Axes,
    x: SelectionOperator,
    y: SelectionOperator,
    xerr: SelectionOperator,
    yerr: SelectionOperator,
    label: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
):
    data = table.data
    ydata = _operate_column(y, data)

    xerrdata = _operate_column(xerr, data, default=None)
    yerrdata = _operate_column(yerr, data, default=None)
    if xerrdata is None and yerrdata is None:
        raise ValueError("Either x-error or y-error must be set.")

    labeldata = _operate_column(label, data, default=None)
    if x is None:
        import pandas as pd

        xdata = pd.Series(np.arange(len(ydata)), name="X")
    else:
        xdata = _operate_column(x, data)

    _errorbar = partial(ax.errorbar, alpha=alpha, fmt="o", picker=True)
    if labeldata is None:
        _errorbar(xdata, ydata, xerr=xerrdata, yerr=yerrdata, label=y)
    else:
        unique = labeldata.unique()
        for label_ in unique:
            spec = labeldata == label_
            if xerrdata is not None:
                xerr_ = xerrdata[spec]
            else:
                xerr_ = None
            if yerrdata is not None:
                yerr_ = yerrdata[spec]
            else:
                yerr_ = None
            _errorbar(
                xdata[spec],
                ydata[spec],
                xerr=xerr_,
                yerr=yerr_,
                label=label_,
            )

    table.plt.draw()
    return True


@dialog_factory_mpl
def fill_between(
    ax: Axes,
    x: SelectionOperator,
    y0: SelectionOperator,
    y1: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
    retain_reference: _bool = False,
):
    from ._plot_models import FillBetweenModel

    model = FillBetweenModel(
        ax, x, y0, y1, table=table, alpha=alpha, ref=retain_reference
    )
    model.add_data(table)
    table.plt.draw()
    return True


@dialog_factory_mpl
def fill_betweenx(
    ax: Axes,
    y: SelectionOperator,
    x0: SelectionOperator,
    x1: SelectionOperator,
    table: TableBase,
    alpha: float = 1.0,
    retain_reference: _bool = False,
):
    from ._plot_models import FillBetweenXModel

    model = FillBetweenXModel(
        ax, y, x0, x1, table=table, alpha=alpha, ref=retain_reference
    )
    model.add_data(table)
    table.plt.draw()
    return True


@dialog_factory_mpl
def hist(
    ax: Axes,
    y: SelectionOperator,
    label: SelectionOperator,
    table: TableBase,
    bins: int = 10,
    range: Tuple[str, str] = ("", ""),
    alpha: float = 1.0,
    density: _bool = False,
    histtype: str = "bar",
):
    from ._plot_models import HistModel

    r0, r1 = range
    if r0 or r1:
        _range = float(r0), float(r1)
    else:
        _range = None
    model = HistModel(
        ax,
        y,
        bins=bins,
        table=table,
        range=_range,
        label_selection=label,
        alpha=alpha,
        density=density,
        histtype=histtype,
    )
    model.add_data(table)
    ax.axhline(0, color="gray", lw=0.5, alpha=0.5, zorder=-1)
    table.plt.draw()
    return True


@dialog_factory_mpl
def swarmplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
    alpha: Annotated[float, {"min": 0.0, "max": 1.0}] = 1.0,
):
    import seaborn as sns

    data = table.data[csel]
    sns.swarmplot(
        x=x, y=y, data=data, hue=hue, dodge=dodge, alpha=alpha, ax=ax, picker=True
    )
    table.plt.draw()
    return True


@dialog_factory_mpl
def barplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
    alpha: Annotated[float, {"min": 0.0, "max": 1.0}] = 1.0,
):
    import seaborn as sns

    data = table.data[csel]
    sns.barplot(
        x=x, y=y, data=data, hue=hue, dodge=dodge, alpha=alpha, ax=ax, picker=True
    )
    ax.axhline(0, color="gray", lw=0.5, alpha=0.5, zorder=-1)
    table.plt.draw()
    return True


@dialog_factory_mpl
def boxplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
):
    import seaborn as sns

    data = table.data[csel]
    sns.boxplot(x=x, y=y, data=data, hue=hue, dodge=dodge, ax=ax)
    table.plt.draw()
    return True


@dialog_factory_mpl
def boxenplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
):
    import seaborn as sns

    data = table.data[csel]
    sns.boxenplot(x=x, y=y, data=data, hue=hue, dodge=dodge, ax=ax, picker=True)
    table.plt.draw()
    return True


@dialog_factory_mpl
def violinplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
):
    import seaborn as sns

    data = table.data[csel]
    sns.violinplot(x=x, y=y, data=data, hue=hue, dodge=dodge, ax=ax, picker=True)
    table.plt.draw()
    return True


@dialog_factory_mpl
def stripplot(
    ax: Axes,
    x: str,
    y: str,
    table: TableBase,
    csel,
    hue: str = None,
    dodge: _bool = False,
):
    import seaborn as sns

    data = table.data[csel]
    sns.stripplot(x=x, y=y, data=data, hue=hue, dodge=dodge, ax=ax, picker=True)
    table.plt.draw()
    return True


@dialog_factory
def choose_one(choice: str):
    return choice


@dialog_factory
def choose_multiple(choices: List):
    return choices


@dialog_factory
def get_value(x):
    return x


@dialog_factory
def spinbox(min: str = "0", max: str = "1000", step: str = "") -> dict:
    min = int(min)
    max = int(max)
    step = int(step) if step != "" else None
    return dict(min=min, max=max, step=step)


@dialog_factory
def float_spinbox(min: str = "0.0", max: str = "1000.0", step: str = "") -> dict:
    min = float(min)
    max = float(max)
    step = float(step) if step != "" else None
    return dict(min=min, max=max, step=step)


@dialog_factory
def slider(min: str = "0", max: str = "1000", step: str = "") -> dict:
    min = int(min)
    max = int(max)
    step = int(step) if step != "" else None
    return dict(min=min, max=max, step=step)


@dialog_factory
def float_slider(min: str = "0.0", max: str = "1000.0", step: str = "") -> dict:
    min = float(min)
    max = float(max)
    step = float(step) if step != "" else None
    return dict(min=min, max=max, step=step)


@dialog_factory
def checkbox(text: str, checked: _bool = True) -> dict:
    return dict(text=text, value=checked)


@dialog_factory
def radio_button(text: str, checked: _bool = True) -> dict:
    return dict(text=text, value=checked)


__void = object()


def _operate_column(
    op: Union[SelectionOperator, None],
    data: "pd.DataFrame",
    default=__void,
) -> Union["pd.Series", None]:
    if op is None:
        if default is __void:
            raise ValueError("Wrong selection.")
        return default
    import pandas as pd

    ds = op.operate(data)
    if isinstance(ds, pd.DataFrame):
        if len(ds.columns) != 1:
            raise ValueError("Operation must return a single column.")
        ds = ds.iloc[:, 0]
    return ds
