from __future__ import annotations
from typing import Any, NamedTuple
from functools import lru_cache
import colorsys
from tabulous.types import ColorType, ColorMapping

import numpy as np


class ColorTuple(NamedTuple):
    """8-bit color tuple."""

    r: int
    g: int
    b: int
    a: int = 255

    @property
    def opacity(self) -> float:
        """Return the opacity as a float between 0 and 1."""
        return self.a / 255.0

    @property
    def html(self) -> str:
        """Return a HTML color string."""
        if self.a == 255:
            return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}{self.a:02X}"

    @property
    def hlsa(self) -> tuple[float, float, float, float]:
        """Return the color as HSLA."""
        hlsa_float = colorsys.rgb_to_hls(
            self.r / 255.0, self.g / 255.0, self.b / 255.0
        ) + (self.opacity,)
        return tuple(int(round(c * 255)) for c in hlsa_float)

    @property
    def hsva(self) -> tuple[float, float, float, float]:
        """Return the color as HSVA."""
        hsva_float = colorsys.rgb_to_hsv(
            self.r / 255.0, self.g / 255.0, self.b / 255.0
        ) + (self.opacity,)
        return tuple(int(round(c * 255)) for c in hsva_float)

    @classmethod
    def from_html(cls, html: str) -> ColorTuple:
        """Create a ColorTuple from a HTML color string."""
        if html.startswith("#"):
            html = html[1:]
        if len(html) == 6:
            html += "FF"
        return cls(*[int(html[i : i + 2], 16) for i in range(0, 8, 2)])

    @classmethod
    def from_hlsa(cls, *hlsa) -> ColorTuple:
        """Create a ColorTuple from HSLA."""
        if len(hlsa) == 1:
            hlsa = hlsa[0]
        if len(hlsa) == 3:
            hls = hlsa
            alpha = 255
        hls = tuple(c / 255.0 for c in hls)
        return cls(*[int(round(c * 255)) for c in colorsys.hls_to_rgb(*hls)], alpha)

    @classmethod
    def from_hsva(cls, *hsva) -> ColorTuple:
        """Create a ColorTuple from HSVA."""
        if len(hsva) == 1:
            hsva = hsva[0]
        if len(hsva) == 3:
            hsv = hsva
            alpha = 255
        hsv_float = tuple(c / 255.0 for c in hsv)
        return cls(
            *[int(round(c * 255)) for c in colorsys.hsv_to_rgb(*hsv_float)], alpha
        )

    def equals(self, other):
        other = normalize_color(other)
        return self == other

    def brighten(self, ratio: float) -> ColorTuple:
        """Set the saturation of the color."""
        hsv = self.hsva[:3]
        val = round(hsv[2] * (1 + ratio))
        val = min(255, max(0, val))
        hsv = (hsv[0], hsv[1], val)
        return ColorTuple.from_hsva(hsv)

    def mix(self, other, ratio: float = 0.5, alpha: bool = False) -> ColorTuple:
        """Mix the color with another color."""
        other = normalize_color(other)
        if alpha:
            _alpha = _8bit(self.a * (1 - ratio) + other.a * ratio)
        else:
            _alpha = self.a
        return ColorTuple(
            _8bit(self.r * (1 - ratio) + other.r * ratio),
            _8bit(self.g * (1 - ratio) + other.g * ratio),
            _8bit(self.b * (1 - ratio) + other.b * ratio),
            _alpha,
        )


def _8bit(x: float) -> int:
    return max(min(int(round(x)), 255), 0)


def normalize_color(color: ColorType) -> ColorTuple:
    """Normalize a color-like object to a ColorTuple."""
    if isinstance(color, str):
        return ColorTuple(*_str_color_to_tuple(color))
    if hasattr(color, "__iter__"):
        out = [int(c) for c in color]
        if len(out) == 3:
            out += [255]
        elif len(out) == 4:
            pass
        else:
            raise ValueError(f"Invalid color: {color!r}")
        return ColorTuple(*out)
    raise ValueError(f"Invalid color: {color!r}")


def rgba_to_str(rgba: tuple[int, int, int, int]) -> str:
    color_name = COLORS_BY_VALUE.get(rgba, None)
    if color_name is None:
        code = "#" + "".join(hex(c)[2:].upper().zfill(2) for c in rgba)
        if code.endswith("FF"):
            code = code[:-2]
        return code
    return color_name


class ConvertedColormap:
    def __init__(self, func: ColorMapping):
        self.func = func
        self.__name__ = f"{type(self).__name__}<{func.__name__}>"
        self.__annotations__ = func.__annotations__

    def __repr__(self):
        return f"{type(self).__name__}<{self.func!r}>"


class InvertedColormap(ConvertedColormap):
    @classmethod
    def from_colormap(cls, cmap: ColorMapping) -> ColorMapping:
        """Convert a colormap into return an inverted one."""
        if isinstance(cmap, cls):
            return cmap.func
        return cls(cmap)

    def __call__(self, x: Any) -> ColorType:
        color = self.func(x)
        if color is None:
            return color
        color = np.array(normalize_color(color), dtype=np.uint8)
        color[:3] = 255 - color[:3]
        return color


class OpacityColormap(ConvertedColormap):
    def __init__(self, func: ColorMapping, opacity: float):
        super().__init__(func)
        if opacity < 0 or 1 < opacity:
            raise ValueError(f"Opacity must be between 0 and 1, got {opacity}")
        self._alpha = int(opacity * 255)

    @classmethod
    def from_colormap(cls, cmap: ColorMapping, opacity: float) -> ColorMapping:
        """Convert a colormap into an new one with given alpha channel."""
        if isinstance(cmap, cls):
            return cls(cmap.func, opacity)
        return cls(cmap, opacity)

    def __call__(self, x: Any) -> ColorType:
        color = self.func(x)
        if color is None:
            return color
        color = np.array(normalize_color(color), dtype=np.uint8)
        color[3] = self._alpha
        return color


class BrightenedColormap(ConvertedColormap):
    def __init__(self, func: ColorMapping, factor: float):
        super().__init__(func)
        if factor < -1:
            raise ValueError(f"Brightening factor fell below -1.0: {factor}")
        if 1 < factor:
            raise ValueError(f"Brightening factor exceeded 1.0: {factor}")
        self._factor = factor

    @classmethod
    def from_colormap(cls, cmap: ColorMapping, factor: float) -> ColorMapping:
        """Convert a colormap into an new one with given brightening factor."""
        if isinstance(cmap, cls):
            return cls(cmap.func, cmap._factor + factor)
        return cls(cmap, factor)

    def __call__(self, x: Any) -> ColorType:
        color = self.func(x)
        if color is None:
            return color
        color = np.array(normalize_color(color), dtype=np.float64)
        factor = self._factor
        if factor > 0:
            extreme = np.array([255, 255, 255, 255], dtype=np.float64)
        else:
            extreme = np.array([0, 0, 0, 255], dtype=np.float64)
        color = color * (1 - factor) + extreme * factor
        return np.round(color).astype(np.uint8)


@lru_cache(maxsize=64)
def _str_color_to_tuple(color: str) -> tuple[int, int, int, int]:
    out = COLORS_BY_NAME.get(color, None)
    if out is not None:
        return out
    if color.startswith("#"):
        color = color[1:]
    if len(color) == 6:
        return int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255
    elif len(color) == 8:
        return (
            int(color[:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
            int(color[6:8], 16),
        )
    raise ValueError(f"Invalid color: {color!r}")


# This dict is modified from pydantic (MIT licence)
# See https://github.com/samuelcolvin/pydantic
COLORS_BY_NAME = {
    "aliceblue": (240, 248, 255, 255),
    "antiquewhite": (250, 235, 215, 255),
    "aqua": (0, 255, 255, 255),
    "aquamarine": (127, 255, 212, 255),
    "azure": (240, 255, 255, 255),
    "beige": (245, 245, 220, 255),
    "bisque": (255, 228, 196, 255),
    "black": (0, 0, 0, 255),
    "blanchedalmond": (255, 235, 205, 255),
    "blue": (0, 0, 255, 255),
    "blueviolet": (138, 43, 226, 255),
    "brown": (165, 42, 42, 255),
    "burlywood": (222, 184, 135, 255),
    "cadetblue": (95, 158, 160, 255),
    "chartreuse": (127, 255, 0, 255),
    "chocolate": (210, 105, 30, 255),
    "coral": (255, 127, 80, 255),
    "cornflowerblue": (100, 149, 237, 255),
    "cornsilk": (255, 248, 220, 255),
    "crimson": (220, 20, 60, 255),
    "cyan": (0, 255, 255, 255),
    "darkblue": (0, 0, 139, 255),
    "darkcyan": (0, 139, 139, 255),
    "darkgoldenrod": (184, 134, 11, 255),
    "darkgray": (169, 169, 169, 255),
    "darkgreen": (0, 100, 0, 255),
    "darkgrey": (169, 169, 169, 255),
    "darkkhaki": (189, 183, 107, 255),
    "darkmagenta": (139, 0, 139, 255),
    "darkolivegreen": (85, 107, 47, 255),
    "darkorange": (255, 140, 0, 255),
    "darkorchid": (153, 50, 204, 255),
    "darkred": (139, 0, 0, 255),
    "darksalmon": (233, 150, 122, 255),
    "darkseagreen": (143, 188, 143, 255),
    "darkslateblue": (72, 61, 139, 255),
    "darkslategray": (47, 79, 79, 255),
    "darkslategrey": (47, 79, 79, 255),
    "darkturquoise": (0, 206, 209, 255),
    "darkviolet": (148, 0, 211, 255),
    "deeppink": (255, 20, 147, 255),
    "deepskyblue": (0, 191, 255, 255),
    "dimgray": (105, 105, 105, 255),
    "dimgrey": (105, 105, 105, 255),
    "dodgerblue": (30, 144, 255, 255),
    "firebrick": (178, 34, 34, 255),
    "floralwhite": (255, 250, 240, 255),
    "forestgreen": (34, 139, 34, 255),
    "fuchsia": (255, 0, 255, 255),
    "gainsboro": (220, 220, 220, 255),
    "ghostwhite": (248, 248, 255, 255),
    "gold": (255, 215, 0, 255),
    "goldenrod": (218, 165, 32, 255),
    "gray": (128, 128, 128, 255),
    "green": (0, 128, 0, 255),
    "greenyellow": (173, 255, 47, 255),
    "grey": (128, 128, 128, 255),
    "honeydew": (240, 255, 240, 255),
    "hotpink": (255, 105, 180, 255),
    "indianred": (205, 92, 92, 255),
    "indigo": (75, 0, 130, 255),
    "ivory": (255, 255, 240, 255),
    "khaki": (240, 230, 140, 255),
    "lavender": (230, 230, 250, 255),
    "lavenderblush": (255, 240, 245, 255),
    "lawngreen": (124, 252, 0, 255),
    "lemonchiffon": (255, 250, 205, 255),
    "lightblue": (173, 216, 230, 255),
    "lightcoral": (240, 128, 128, 255),
    "lightcyan": (224, 255, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210, 255),
    "lightgray": (211, 211, 211, 255),
    "lightgreen": (144, 238, 144, 255),
    "lightgrey": (211, 211, 211, 255),
    "lightpink": (255, 182, 193, 255),
    "lightsalmon": (255, 160, 122, 255),
    "lightseagreen": (32, 178, 170, 255),
    "lightskyblue": (135, 206, 250, 255),
    "lightslategray": (119, 136, 153, 255),
    "lightslategrey": (119, 136, 153, 255),
    "lightsteelblue": (176, 196, 222, 255),
    "lightyellow": (255, 255, 224, 255),
    "lime": (0, 255, 0, 255),
    "limegreen": (50, 205, 50, 255),
    "linen": (250, 240, 230, 255),
    "magenta": (255, 0, 255, 255),
    "maroon": (128, 0, 0, 255),
    "mediumaquamarine": (102, 205, 170, 255),
    "mediumblue": (0, 0, 205, 255),
    "mediumorchid": (186, 85, 211, 255),
    "mediumpurple": (147, 112, 219, 255),
    "mediumseagreen": (60, 179, 113, 255),
    "mediumslateblue": (123, 104, 238, 255),
    "mediumspringgreen": (0, 250, 154, 255),
    "mediumturquoise": (72, 209, 204, 255),
    "mediumvioletred": (199, 21, 133, 255),
    "midnightblue": (25, 25, 112, 255),
    "mintcream": (245, 255, 250, 255),
    "mistyrose": (255, 228, 225, 255),
    "moccasin": (255, 228, 181, 255),
    "navajowhite": (255, 222, 173, 255),
    "navy": (0, 0, 128, 255),
    "oldlace": (253, 245, 230, 255),
    "olive": (128, 128, 0, 255),
    "olivedrab": (107, 142, 35, 255),
    "orange": (255, 165, 0, 255),
    "orangered": (255, 69, 0, 255),
    "orchid": (218, 112, 214, 255),
    "palegoldenrod": (238, 232, 170, 255),
    "palegreen": (152, 251, 152, 255),
    "paleturquoise": (175, 238, 238, 255),
    "palevioletred": (219, 112, 147, 255),
    "papayawhip": (255, 239, 213, 255),
    "peachpuff": (255, 218, 185, 255),
    "peru": (205, 133, 63, 255),
    "pink": (255, 192, 203, 255),
    "plum": (221, 160, 221, 255),
    "powderblue": (176, 224, 230, 255),
    "purple": (128, 0, 128, 255),
    "red": (255, 0, 0, 255),
    "rosybrown": (188, 143, 143, 255),
    "royalblue": (65, 105, 225, 255),
    "saddlebrown": (139, 69, 19, 255),
    "salmon": (250, 128, 114, 255),
    "sandybrown": (244, 164, 96, 255),
    "seagreen": (46, 139, 87, 255),
    "seashell": (255, 245, 238, 255),
    "sienna": (160, 82, 45, 255),
    "silver": (192, 192, 192, 255),
    "skyblue": (135, 206, 235, 255),
    "slateblue": (106, 90, 205, 255),
    "slategray": (112, 128, 144, 255),
    "slategrey": (112, 128, 144, 255),
    "snow": (255, 250, 250, 255),
    "springgreen": (0, 255, 127, 255),
    "steelblue": (70, 130, 180, 255),
    "tan": (210, 180, 140, 255),
    "teal": (0, 128, 128, 255),
    "thistle": (216, 191, 216, 255),
    "tomato": (255, 99, 71, 255),
    "turquoise": (64, 224, 208, 255),
    "violet": (238, 130, 238, 255),
    "wheat": (245, 222, 179, 255),
    "white": (255, 255, 255, 255),
    "whitesmoke": (245, 245, 245, 255),
    "yellow": (255, 255, 0, 255),
    "yellowgreen": (154, 205, 50, 255),
}

COLORS_BY_VALUE = {v: k for k, v in COLORS_BY_NAME.items()}
