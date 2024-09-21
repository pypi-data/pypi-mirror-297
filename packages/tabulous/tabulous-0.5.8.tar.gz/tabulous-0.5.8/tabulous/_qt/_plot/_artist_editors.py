from __future__ import annotations
from typing import Generic, Sequence, TypeVar
import weakref
from matplotlib.collections import PathCollection, LineCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.patches import Polygon

from matplotlib.artist import Artist

from magicgui.widgets import (
    ComboBox,
    Container,
    SpinBox,
    FloatSpinBox,
    LineEdit,
    Widget,
)

from ._artist_types import (
    LineStyle,
    Marker,
    HatchStyle,
    VerticalAlignment,
    HorizontalAlignment,
)

_A = TypeVar("_A", bound=Artist)
_T = TypeVar("_T")

_TYPE_MAP: dict[type[Artist], type[ArtistEditor]] = {}


def _register(artist: type[Artist]):
    def _wrapper(cls: _T) -> _T:
        _TYPE_MAP[artist] = cls
        return cls

    return _wrapper


class _Ref(Generic[_T]):
    """a non-weak reference type."""

    def __init__(self, seq: _T):
        self._seq = seq

    def __call__(self) -> _T:
        return self._seq


def _to_float_rgba(rgba: Sequence[int]) -> list[float]:
    return [c / 255 for c in rgba]


class ArtistEditor(Container, Generic[_A]):
    """Base class for artist editor containers."""

    def __init__(self, artist: _A):
        self.artist = artist
        widgets = self._create_widgets()
        super().__init__(widgets=widgets)

    def _create_widgets(self) -> list[Widget]:
        raise NotImplementedError()

    def get_label(self):
        """Get the label for the artist."""
        return self.artist.get_label()

    @property
    def artist(self) -> _A:
        """Return the Artist object."""
        out = self._artist()
        if out is None:
            raise ValueError("Artist object has been deleted.")
        return out

    @artist.setter
    def artist(self, artist: _A):
        if isinstance(artist, (tuple, list)):  # Collection type is a subclass of tuple
            self._artist = _Ref(artist)
        else:
            self._artist = weakref.ref(artist)
        return None


@_register(Line2D)
class Line2DEdit(ArtistEditor[Line2D]):
    def _create_widgets(self) -> None:
        from tabulous._magicgui import ColorEdit

        widgets = []
        line = self.artist

        # line color
        color = line.get_color()
        if not isinstance(color, str):
            color = [int(c * 255) for c in color]
        _color_edit = ColorEdit(name="color", value=color)
        _color_edit.changed.connect(self.set_color)
        widgets.append(_color_edit)

        # line style
        _ls_edit = ComboBox(
            choices=LineStyle, value=LineStyle(line.get_linestyle()), label="linestyle"
        )
        _ls_edit.changed.connect(self.set_linestyle)
        widgets.append(_ls_edit)

        # line width
        _lw_edit = FloatSpinBox(
            min=0.0, max=10.0, step=0.5, value=line.get_linewidth(), label="linewidth"
        )
        _lw_edit.changed.connect(self.set_linewidth)
        widgets.append(_lw_edit)

        _marker = ComboBox(
            choices=Marker, label="marker", value=Marker(line.get_marker())
        )
        _marker.changed.connect(self.set_marker)
        _markerfacecolor = ColorEdit(
            label="marker face color", value=fix_color(line.get_markerfacecolor())
        )
        _markerfacecolor.changed.connect(self.set_markerfacecolor)
        _markeredgecolor = ColorEdit(
            label="marker edge color", value=fix_color(line.get_markeredgecolor())
        )
        _markeredgecolor.changed.connect(self.set_markeredgecolor)
        _markeredgewidth = FloatSpinBox(
            min=0.0,
            max=10.0,
            step=0.5,
            label="marker edge width",
            value=line.get_markeredgewidth(),
        )
        _markeredgewidth.changed.connect(self.set_markeredgewidth)
        _markersize = FloatSpinBox(
            label="marker size",
            min=0.0,
            max=50.0,
            step=0.5,
            value=line.get_markersize(),
        )
        _markersize.changed.connect(self.set_markersize)

        self._marker_related: list[Widget] = [
            _markerfacecolor,
            _markeredgecolor,
            _markeredgewidth,
            _markersize,
        ]

        widgets.extend(
            [_marker, _markerfacecolor, _markeredgecolor, _markeredgewidth, _markersize]
        )

        # zorder
        _zorder = SpinBox(min=-10000, max=10000, value=line.get_zorder(), name="zorder")
        _zorder.changed.connect(self.set_zorder)
        widgets.append(_zorder)

        self.set_marker(_marker.value)
        return widgets

    def set_color(self, rgba: tuple[int, int, int, int]) -> None:
        """Set the line color."""
        self.artist.set_color(_to_float_rgba(rgba))

    def set_linestyle(self, ls: LineStyle):
        self.artist.set_linestyle(ls.value)

    def set_linewidth(self, lw: float):
        self.artist.set_linewidth(lw)

    def set_zorder(self, zorder: int):
        self.artist.set_zorder(zorder)

    def set_marker(self, marker: Marker):
        marker = Marker(marker)
        self.artist.set_marker(marker.value)
        has_marker = marker != Marker.none
        for wdt in self._marker_related:
            wdt.enabled = has_marker

    def set_markerfacecolor(self, rgba):
        self.artist.set_markerfacecolor(_to_float_rgba(rgba))

    def set_markeredgecolor(self, rgba):
        self.artist.set_markeredgecolor(_to_float_rgba(rgba))

    def set_markeredgewidth(self, width: float):
        self.artist.set_markeredgewidth(width)

    def set_markersize(self, size: float):
        self.artist.set_markersize(size)


@_register(PathCollection)
class ScatterEdit(ArtistEditor[PathCollection]):
    def _create_widgets(self) -> list[Widget]:
        from tabulous._magicgui._color_edit import ColorEdit

        scatter = self.artist

        # scatter color
        _facecolor = ColorEdit(
            name="face color", value=scatter.get_facecolor()[0] * 255
        )
        _facecolor.changed.connect(self.set_facecolor)

        _edgecolor = ColorEdit(
            name="edge color", value=scatter.get_edgecolor()[0] * 255
        )
        _edgecolor.changed.connect(self.set_edgecolor)

        # _edgewidth = FloatSpinBox(name="edge width", value=scatter.get_linewidth())

        # marker
        _marker_edit = ComboBox(choices=Marker, value=Marker.circle, name="marker")
        _marker_edit.changed.connect(self.set_marker)

        _size_edit = FloatSpinBox(
            min=0.0, max=500.0, step=1, value=scatter.get_sizes()[0], name="size"
        )
        _size_edit.changed.connect(self.set_size)

        # zorder
        _zorder = SpinBox(
            min=-10000, max=10000, value=scatter.get_zorder(), name="zorder"
        )
        _zorder.changed.connect(self.set_zorder)

        return [_facecolor, _edgecolor, _marker_edit, _size_edit, _zorder]

    def set_facecolor(self, rgba: tuple[int, int, int, int]) -> None:
        """Set face colors of the scatter."""
        self.artist.set_facecolor(_to_float_rgba(rgba))

    def set_edgecolor(self, rgba: tuple[int, int, int, int]) -> None:
        """Set edge colors of the scatter."""
        self.artist.set_edgecolors(_to_float_rgba(rgba))

    def set_marker(self, marker: Marker | str):
        import matplotlib.markers as mmarkers

        marker = Marker(marker)
        marker_obj = mmarkers.MarkerStyle(marker.value)

        path = marker_obj.get_path().transformed(marker_obj.get_transform())
        self.artist.set_paths((path,))

    def set_size(self, size: int) -> None:
        self.artist.set_sizes([size])

    def set_zorder(self, zorder: int):
        self.artist.set_zorder(zorder)


@_register(BarContainer)
class PatchContainerEdit(ArtistEditor[BarContainer]):
    def _create_widgets(self) -> list[Widget]:
        from ..._magicgui._color_edit import ColorEdit

        artist = self.artist
        _facecolor = ColorEdit(
            label="face color", value=fix_color(artist[0].get_facecolor())
        )
        _facecolor.changed.connect(self.set_facecolor)
        _edgecolor = ColorEdit(
            label="edge color", value=fix_color(artist[0].get_edgecolor())
        )
        _edgecolor.changed.connect(self.set_edgecolor)
        hatch = artist[0].get_hatch() or "None"
        _hatch = ComboBox(choices=HatchStyle, label="hatch", value=HatchStyle(hatch))
        _hatch.changed.connect(self.set_hatch)
        return [_facecolor, _edgecolor, _hatch]

    def set_facecolor(self, rgba):
        rgba = _to_float_rgba(rgba)
        for artist in self.artist:
            artist.set_facecolor(rgba)

    def set_edgecolor(self, rgba):
        rgba = _to_float_rgba(rgba)
        for artist in self.artist:
            artist.set_edgecolor(rgba)

    def set_hatch(self, hatch: HatchStyle):
        if hatch == HatchStyle.none:
            v = None
        else:
            v = hatch.value
        for artist in self.artist:
            artist.set_hatch(v)

    def get_label(self) -> str:
        return self.artist[0].get_label()


@_register(LineCollection)
class LineCollectionEdit(ArtistEditor[LineCollection]):
    def _create_widgets(self) -> list[Widget]:
        from tabulous._magicgui._color_edit import ColorEdit

        line = self.artist

        _color = ColorEdit(name="color", value=fix_color(line.get_color()[0]))
        _color.changed.connect(self.set_errorbar_color)

        # line width
        _lw_edit = FloatSpinBox(
            min=0.0, max=10.0, step=0.5, value=line.get_linewidth(), name="linewidth"
        )
        _lw_edit.changed.connect(self.set_linewidth)

        return [_color, _lw_edit]

    def set_errorbar_color(self, rgba):
        self.artist.set_color(_to_float_rgba(rgba))

    def set_linewidth(self, width: float):
        self.artist.set_linewidth(width)


@_register(PolyCollection)
class PolyCollectionEdit(ArtistEditor[PolyCollection]):
    def _create_widgets(self) -> list[Widget]:
        from tabulous._magicgui._color_edit import ColorEdit

        poly = self.artist

        ec = poly.get_edgecolors()
        if ec.shape[0] == 0:
            ec = (0, 0, 0, 0)
        else:
            ec = ec[0]

        _face_color = ColorEdit(
            name="facecolor", value=fix_color(poly.get_facecolors()[0])
        )
        _face_color.changed.connect(self.set_facecolor)
        _edge_color = ColorEdit(name="edgecolor", value=fix_color(ec))
        _edge_color.changed.connect(self.set_edgecolor)
        _hatch = ComboBox(choices=HatchStyle, name="hatch", value=HatchStyle.none)
        _hatch.changed.connect(self.set_hatch)
        _ls = ComboBox(choices=LineStyle, name="linestyle", value=LineStyle.solid)
        _ls.changed.connect(self.set_linestyle)

        # line width
        _lw_edit = FloatSpinBox(
            min=0.0, max=10.0, step=0.5, value=poly.get_linewidth(), name="linewidth"
        )
        _lw_edit.changed.connect(self.artist.set_linewidth)

        return [_face_color, _edge_color, _ls, _lw_edit]

    def set_facecolor(self, rgba):
        self.artist.set_facecolor(_to_float_rgba(rgba))

    def set_edgecolor(self, rgba):
        self.artist.set_edgecolor(_to_float_rgba(rgba))

    def set_hatch(self, hatch: HatchStyle):
        if hatch == HatchStyle.none:
            v = None
        else:
            v = hatch.value
        self.artist.set_hatch(v)

    def set_linestyle(self, ls: LineStyle):
        self.artist.set_linestyle(ls.value)


@_register(Polygon)
class PolygonEdit(ArtistEditor[Polygon]):
    def _create_widgets(self) -> list[Widget]:
        from tabulous._magicgui._color_edit import ColorEdit

        polygon = self.artist
        _facecolor = ColorEdit(
            label="face color", value=fix_color(polygon.get_facecolor())
        )
        _facecolor.changed.connect(self.set_facecolor)
        _edgecolor = ColorEdit(
            label="edge color", value=fix_color(polygon.get_edgecolor())
        )
        _edgecolor.changed.connect(self.set_edgecolor)

        _linewidth = FloatSpinBox(
            label="edge width",
            value=polygon.get_linewidth(),
            min=0.0,
            max=50.0,
            step=0.5,
        )
        _linewidth.changed.connect(self.set_linewidth)

        return [_facecolor, _edgecolor, _linewidth]

    def set_facecolor(self, rgba):
        rgba = _to_float_rgba(rgba)
        self.artist.set_facecolor(rgba)

    def set_edgecolor(self, rgba):
        rgba = _to_float_rgba(rgba)
        self.artist.set_edgecolor(rgba)

    def set_linewidth(self, width: float):
        self.artist.set_linewidth(width)


@_register(Text)
class TextEdit(ArtistEditor[Text]):
    def _create_widgets(self) -> list[Widget]:
        from tabulous._magicgui._color_edit import ColorEdit

        _color = ColorEdit(name="color", value=fix_color(self.artist.get_color()))
        _color.changed.connect(self.set_color)

        _font_size = SpinBox(
            name="font size", value=self.artist.get_fontsize(), min=1, max=180
        )
        _font_size.changed.connect(self.artist.set_fontsize)

        _text = LineEdit(name="text", value=self.artist.get_text())
        _text.changed.connect(self.artist.set_text)

        _va = ComboBox(
            name="vertical",
            choices=VerticalAlignment,
            value=VerticalAlignment(self.artist.get_verticalalignment()),
        )
        _ha = ComboBox(
            name="horizontal",
            choices=HorizontalAlignment,
            value=HorizontalAlignment(self.artist.get_horizontalalignment()),
        )
        _va.changed.connect(self.set_verticalalignment)
        _ha.changed.connect(self.set_horizontalalignment)

        _alignment = Container(widgets=[_va, _ha], name="alignment")
        return [_color, _font_size, _text, _alignment]

    def set_color(self, rgba):
        self.artist.set_color(_to_float_rgba(rgba))

    def set_verticalalignment(self, alignment: VerticalAlignment):
        self.artist.set_verticalalignment(alignment.value)

    def set_horizontalalignment(self, alignment: HorizontalAlignment):
        self.artist.set_horizontalalignment(alignment.value)


def pick_container(artist: Artist) -> ArtistEditor:
    """Return a proper container for the given artist."""
    for artist_cls, wdt_cls in _TYPE_MAP.items():
        if isinstance(artist, artist_cls):
            return wdt_cls(artist)
    raise ValueError(f"No container found for artist {type(artist).__name__}.")


def fix_color(color):
    if not isinstance(color, str):
        color = [int(c * 255) for c in color]
    return color
