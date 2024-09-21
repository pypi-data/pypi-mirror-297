from __future__ import annotations
from typing import Callable, TypeVar

_T = TypeVar("_T", bound=Callable)

# fmt: off
_PARAMETERS = dict(
    name="name : str, optional\n\tName of the table.",
    editable="editable : bool, default is False\n\tWhether the table is editable via UI.",
    copy="copy : bool, default is True\n\tWhether to copy the data before adding to avoid overwriting the original one.",
    metadata="metadata : dict, optional\n\tMetadata of the table.",
    update="update : bool, default is False\n\tIf True, update the table data if a table of same name exists.",
)
# fmt: on


def update_doc(f: _T) -> _T:
    """Update the docstring of the given object."""
    doc = f.__doc__
    if doc:
        doc_lines = doc.splitlines()
        indent = doc_lines[1][: -len(doc_lines[1].lstrip())]
        doc = doc.replace("}{", f"}}\n{indent}{{")
        params = {k: _expand_indent(v, indent) for k, v in _PARAMETERS.items()}
        doc = doc.format(**params)
    f.__doc__ = doc
    return f


def _expand_indent(s: str, indent: str) -> str:
    line0, line1 = s.split("\n")
    return f"{line0}\n{indent}{line1}"
