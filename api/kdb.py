from qpython import qconnection

import pandas as pd
import numpy as np
import pandas.api.types as pdat

import dashutils.utils as utils

from dataclasses import dataclass

@dataclass
class kdbConn(object):
    host: str
    port: int
    username: str = None
    password: str = None

    @utils.trap_exception_message
    def query_kdb_process(self, *args, **kwargs):
        with qconnection.QConnection(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        ) as q:
            res = q.sendSync(*args, **kwargs)
            if isinstance(res, pd.DataFrame):
                res = self.format_kdb_output_df(res)
            return res

    def format_kdb_output_df(self, df):
        if len(df):
            # Handle keyed tables
            df = df.reset_index()

            if "index" in df.columns:
                df = df.drop(columns="index")

            for k, v in df.dtypes.items():
                if k == "date":
                    dfk = df["date"]
                    if pdat.is_datetime64_ns_dtypes(dfk):
                        df["date"] = dfk.apply(lambda x: x.date())
                elif v == "object":
                    dfk = df[k]
                    df[k] = (
                        dfk.str.decode("utf-8")
                        if pdat.infer_dtype(dfk) == "bytes"
                        else dfk.astype(str)
                    )
        return df
