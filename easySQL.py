from __future__ import annotations
from lib.queries import SQLQueryBuilder
from lib.connections import EasySQLConnector
import pandas as pd

class EasySQL(SQLQueryBuilder, EasySQLConnector):

    def __init__(self, env_path: str, tunnel: bool = False) -> EasySQL:
        SQLQueryBuilder.__init__(self)
        EasySQLConnector.__init__(self, env_path, tunnel)
        self._data = None

    def request_results_df(self) -> None:

        self._connect()
        query = self.query
        self._data = self.data_frame_query(query)
        self._disconnect()
    
    @property
    def execute(self) -> pd.DataFrame:

        self.request_results_df()
        return self._data
