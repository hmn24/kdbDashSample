import pandas as pd
from functools import wraps
import dash
from dash import dcc


# To format df for dash plotly
def parse_df_for_dash(df):
    if df is None:
        df = pd.DataFrame()

    columns = [
        dict(
            name=i,
            id=i,
            hideable=True,
        )
        for i in df.columns
    ]
    data = df.to_dict("records")
    return columns, data


# To create dropdown for dash plotly
def create_dropdowns_for_dash(options):
    return [
        dict(
            label=i,
            value=i,
        )
        for i in options
    ]


# To create a wrapper to trap exception messages and return exception error in string
def trap_exception_message(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs), ""
        except Exception as e:
            print(exception_msg := f"Exception occured: {e}")
            return None, exception_msg

    return wrapper


# To print the message out with flag for ConfirmDialog
def parse_query_results_for_callbacks(result, throw_error, pandas=True):
    if pandas:
        if throw_error:
            return None, None, "data-entry", True
        else:
            columns, data = parse_df_for_dash(result)
            return columns, data, "view-entry", False
    else:
        if throw_error:
            return None, "data-entry", True
        else:
            return result, "view-entry", False


# To print the message out with flag for ConfirmDialog
def parse_query_results_for_download_callbacks(df, throw_error, filename="Data.csv"):
    if not throw_error:
        if isinstance(df, pd.DataFrame):
            return dcc.send_data_frame(df.to_csv, filename)
    raise dash.exceptions.PreventUpdate
