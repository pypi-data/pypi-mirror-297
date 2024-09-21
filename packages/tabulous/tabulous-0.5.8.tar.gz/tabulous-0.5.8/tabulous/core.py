from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from tabulous.widgets import TableViewer

if TYPE_CHECKING:
    from .widgets._mainwindow import TableViewerBase

CURRENT_VIEWER: TableViewerBase | None = None


def current_viewer() -> TableViewerBase:
    """Get the current table viewer widget."""
    global CURRENT_VIEWER
    if CURRENT_VIEWER is None:
        CURRENT_VIEWER = TableViewer()
    return CURRENT_VIEWER


def set_current_viewer(viewer: TableViewerBase) -> TableViewerBase:
    """Set a table viewer as the current one."""
    global CURRENT_VIEWER
    from .widgets._mainwindow import TableViewerBase

    if not isinstance(viewer, TableViewerBase):
        raise TypeError(f"Cannot set {type(viewer)} as the current viewer.")
    CURRENT_VIEWER = viewer
    return viewer


def read_csv(path: str | Path, *args, **kwargs) -> TableViewerBase:
    """Read CSV file and add it to the current viewer."""
    import pandas as pd

    df = pd.read_csv(path, *args, **kwargs)
    name = Path(path).stem
    viewer = current_viewer()
    viewer.add_table(df, name=name)
    viewer.show(run=False)
    return viewer


def read_excel(path: str | Path, *args, **kwargs) -> TableViewerBase:
    """Read Excel file and add all the sheets to the current viewer."""
    import pandas as pd

    df_dict: dict[str, pd.DataFrame] = pd.read_excel(
        path, *args, sheet_name=None, **kwargs
    )

    viewer = current_viewer()
    for sheet_name, df in df_dict.items():
        viewer.add_table(df, name=sheet_name)
    viewer.show(run=False)
    return viewer


def view_table(
    data,
    *,
    name: str | None = None,
    editable: bool = False,
    copy: bool = True,
) -> TableViewerBase:
    """View a table in the current viewer."""
    viewer = current_viewer()
    viewer.add_table(data, name=name, editable=editable, copy=copy)
    viewer.show(run=False)
    return viewer


def view_spreadsheet(
    data,
    *,
    name: str | None = None,
    editable: bool = True,
    copy: bool = True,
) -> TableViewerBase:
    """View a table as a spreadsheet in the current viewer."""
    viewer = current_viewer()
    viewer.add_spreadsheet(data, name=name, editable=editable, copy=copy)
    viewer.show(run=False)
    return viewer


def open_sample(
    sample_name: str,
    plugin_name: str = "seaborn",
) -> TableViewerBase:
    """Open a sample data."""
    viewer = current_viewer()
    viewer.open_sample(sample_name, plugin_name)
    viewer.show(run=False)
    return viewer
