from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tabulous.widgets import TableViewerBase


def show_keymap(viewer: TableViewerBase):
    """Show key map widget"""
    viewer._qwidget.showKeyMap()


def close_window(viewer: TableViewerBase):
    """Close window"""
    viewer._qwidget.close(ask=None)


def new_window(viewer: TableViewerBase):
    """Create a new window"""
    new = viewer.__class__()
    pos = viewer._qwidget.pos()
    pos.setX(pos.x() + 20)
    pos.setY(pos.y() + 20)
    new._qwidget.move(pos)
    return new._qwidget.activateWindow()


def toggle_toolbar(viewer: TableViewerBase):
    """Toggle toolbar visibility"""
    viewer._qwidget.toggleToolBarVisibility()


def toggle_console(viewer: TableViewerBase):
    """Toggle QtConsole visibility"""
    return viewer._qwidget.toggleConsoleVisibility()


def toggle_fullscreen(viewer: TableViewerBase):
    """Toggle fullscreen"""
    viewer._qwidget.toggleWindowState()


def show_command_palette(viewer: TableViewerBase):
    """Show the command palette."""
    viewer._qwidget.showCommandPalette()


def focus_table(viewer: TableViewerBase):
    """Move focus to the table."""
    viewer.native.setCellFocus()


def toggle_focus(viewer: TableViewerBase):
    """Toggle focus between table and command palette."""
    table = viewer.current_table
    qviewer = viewer._qwidget
    if table is None:
        return
    if table._qwidget._qtable_view.hasFocus():
        console = qviewer._console_widget
        if console is not None and console.isActive():
            console.setFocus()
    else:
        qviewer.setCellFocus()
    return


def add_text_edit(viewer: TableViewerBase):
    """Add a note (text edit) dock widget."""
    from tabulous import TableViewer, TableViewerWidget
    from tabulous._qt._qt_const import MonospaceFontFamily
    from qtpy import QtWidgets as QtW, QtGui

    txt_edit = QtW.QTextEdit()
    txt_edit.setWordWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
    txt_edit.setFont(QtGui.QFont(MonospaceFontFamily, 10))

    metrics = txt_edit.fontMetrics()
    txt_edit.setTabStopWidth(4 * metrics.width(" "))

    if isinstance(viewer, TableViewer):
        viewer.add_dock_widget(txt_edit, name="Note")
    elif isinstance(viewer, TableViewerWidget):
        viewer.add_widget(txt_edit, name="Note")
    else:
        raise TypeError(f"Cannot add widget to {type(viewer)}")
    return None


def add_file_explorer(viewer: TableViewerBase):
    """Add a file explorer dock widget."""
    from tabulous import TableViewer, TableViewerWidget
    from tabulous._qt._filetree import QFileExplorer

    tree_view = QFileExplorer()
    if isinstance(viewer, TableViewer):
        viewer.add_dock_widget(
            tree_view, name="File Explorer", area="left", allowed_areas=["left"]
        )
    elif isinstance(viewer, TableViewerWidget):
        viewer.add_widget(tree_view, name="File Explorer")
    else:
        raise TypeError(f"Cannot add widget to {type(viewer)}")
    return None


def show_preference(viewer: TableViewerBase):
    """Show preference dialog"""
    viewer._qwidget.showPreferenceDialog()
