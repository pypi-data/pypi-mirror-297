from __future__ import annotations
from typing import Any
import pandas as pd
from collections_undo import arguments

from tabulous.types import ItemInfo

from ._base import QMutableSimpleTable, DataFrameModel
from tabulous._dtype import get_converter


class QTableLayer(QMutableSimpleTable):
    def getDataFrame(self) -> pd.DataFrame:
        return self._data_raw

    @QMutableSimpleTable._mgr.interface
    def setDataFrame(self, data: pd.DataFrame) -> None:
        self._data_raw = data
        self.model().df = data
        self.setProxy(None)
        self._qtable_view.viewport().update()
        return

    @setDataFrame.server
    def setDataFrame(self, data):
        try:
            return arguments(self.getDataFrame())
        except Exception:
            return None

    @setDataFrame.set_formatter
    def _setDataFrame_fmt(self, data: pd.DataFrame):
        return f"set new data of shape {data.shape}"

    __delete = object()

    @QMutableSimpleTable._mgr.interface
    def assignColumns(self, serieses: dict[str, pd.Series]):
        to_delete = set()
        to_assign: dict[str, pd.Series] = {}
        for k, v in serieses.items():
            if v is self.__delete:
                to_delete.add(k)
            else:
                to_assign[k] = v
        old_value = self._data_raw
        self._data_raw: pd.DataFrame = self._data_raw.assign(**to_assign).drop(
            to_delete, axis=1
        )
        nr, nc = self._data_raw.shape
        self.model().df = self._data_raw
        self.model().setShape(nr, nc)
        self._set_proxy(None)
        self.refreshTable()

        # NOTE: ItemInfo cannot have list indices.
        self.itemChangedSignal.emit(
            ItemInfo(
                slice(None),
                slice(None),
                self._data_raw,
                old_value,
            )
        )
        return None

    @assignColumns.server
    def assignColumns(self, serieses: dict[str, pd.Series]):
        columns = self._data_raw.columns
        old_param: dict[str, pd.Series] = {}
        for k in serieses.keys():
            if k in columns:
                old_param[k] = self._data_raw[k]
            else:
                old_param[k] = self.__delete
        return arguments(old_param)

    def createModel(self):
        model = DataFrameModel(self)
        self._qtable_view.setModel(model)
        return None

    def convertValue(self, c: int, value: Any) -> Any:
        """Convert value to the type of the table."""
        dtype = self._data_raw.dtypes.iloc[c]
        return get_converter(dtype)(value)
