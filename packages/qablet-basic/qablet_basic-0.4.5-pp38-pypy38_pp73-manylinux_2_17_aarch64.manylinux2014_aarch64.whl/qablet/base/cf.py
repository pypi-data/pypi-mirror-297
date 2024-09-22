# Define Base Class for Cashflow Models
from abc import ABC, abstractmethod

import polars as pl

from .._qablet import backtest_csv, backtest_py

MS_IN_DAY = 1000 * 3600 * 24


class CFModelPyBase(ABC):
    """Base class for all Cashflow models delegating data to py class."""

    def __init__(self, base):
        self.base = base
        self.stats = {}

    def set_stat(self, key: str, val):
        self.stats[key] = val

    @abstractmethod
    def get_value(self, unit, ts):
        """Return value for given unit on given ts."""
        ...

    def cashflow(self, timetable):
        backtest_py(
            timetable["events"],
            self,
            timetable.get("expressions", {}),
            self.base,
        )

        return self.stats["CASHFLOW"][0].sort_by("index")

    def cashflow_by_ts(self, timetable):
        cf = self.cashflow(timetable)

        # convert to polars dataframe
        cf_df = pl.from_arrow(cf)
        ts_col = pl.from_arrow(
            timetable["events"]["time"], schema={"time": pl.Int64}
        )[cf_df["index"]]
        return cf_df.with_columns(ts=ts_col)


class CFModelCSV:
    """A cashflow model using backtest_csv (currently trivially implemented)"""

    def __init__(self, filename, base):
        self.base = base
        self.filename = filename
        self.stats = {}

    def set_stat(self, key: str, val):
        self.stats[key] = val

    def cashflow(self, timetable):
        backtest_csv(
            timetable["events"],
            self,
            self.filename,
            self.base,
            timetable.get("expressions", {}),
        )

        return self.stats["CASHFLOW"][0].sort_by("index")
