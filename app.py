import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

import numpy as np
import dashutils.utils as utils

from api.kdb import kdbConn

# Create the app itself
app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = False

# Initiate the kdbConn
kdb = kdbConn(
    host="localhost",
    port=5050,
)


def query_kdb_process_info(submit_entry, exception):
    if submit_entry:
        result, exception_msg = kdb.query_kdb_process(
            """
            {[exception]
                if[exception=`Yes; '"Error"];
                :([] a:10?`3);
            }
            """,
            np.string_(exception),
            pandas=True,
        )
        return result, exception_msg
    raise dash.exceptions.PreventUpdate


@app.callback(
    [
        Output("app-entry-table", "columns"),
        Output("app-entry-table", "data"),
        Output("app-tabs-info", "value"),
        Output("app-confirm-dialog", "displayed"),
    ],
    [
        Input("app-submit-entry", "n_clicks"),
    ],
    [
        State("app-select-exception", "value"),
    ],
)
def get_kdb_process_info(submit_entry, exception):
    return utils.parse_query_results_for_callbacks(
        *query_kdb_process_info(submit_entry, exception),
        pandas=True,
    )


@app.callback(
    Output("app-dataframe-csv", "data"),
    Input("app-download-data", "n_clicks"),
    State("app-select-exception", "value"),
)
def download_kdb_process_info(submit_entry, exception):
    return utils.parse_query_results_for_download_callbacks(
        *query_kdb_process_info(submit_entry, exception),
        filename=f"app_{exception}.csv",
    )


# Layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/dash-logo.png", className="app__logo"),
                html.H4("Query KDB Database", className="header__text"),
            ],
            className="app__header",
        ),
        html.Div(
            [
                dcc.ConfirmDialog(
                    id="app-confirm-dialog",
                    message="Error when querying",
                    displayed=False,
                ),
                dcc.Tabs(
                    id="app-tabs-info",
                    value="data-entry",
                    children=[
                        dcc.Tab(
                            label="DATA ENTRY",
                            value="data-entry",
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Throw Exception:",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="app-select-exception",
                                                    options=utils.create_dropdowns_for_dash(
                                                        ["Yes", "No"]
                                                    ),
                                                    value="Yes",
                                                    className="dropdown__select",
                                                ),
                                            ],
                                            className="dropdown__container",
                                        ),
                                        html.Div(
                                            [
                                                html.Button(
                                                    "SUBMIT ENTRY",
                                                    id="app-submit-entry",
                                                    className="submit__button",
                                                ),
                                                html.Button(
                                                    "DOWNLOAD DATA",
                                                    id="app-download-data",
                                                    className="download__button",
                                                ),
                                            ]
                                        ),
                                        dcc.Download(id="app-dataframe-csv"),
                                    ],
                                    className="container__1",
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="VIEW DATA ENTRY",
                            value="view-entry",
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="app-entry-table",
                                                    style_cell=dict(
                                                        minWidth="0px",
                                                        maxWidth="180px",
                                                        whiteSpace="normal",
                                                    ),
                                                    style_as_list_view=True,
                                                    filter_action="native",
                                                    page_size=20,
                                                    export_format="csv",
                                                    style_table={
                                                        "min-height": "500px",
                                                    },
                                                )
                                            ],
                                            className="table__1",
                                        )
                                    ],
                                    className="table__container",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            className="tabs__container",
        ),
    ],
    className="app__container",
)

if __name__ == "__main__":
    app.run_server(debug=False)
