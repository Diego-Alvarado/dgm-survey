import pandas as pd
from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output

def render(app: Dash, df_sequence: pd.DataFrame) -> html.Div:
    return html.Div(
        children=[
            dash_table.DataTable(
                id='datatable-seq-id',
                data=df_sequence.to_dict('records'),
                markdown_options={'html': True}, 
                columns=[
                    {'name': '', 'id': 'index'},
                    {'name': 'A', 'id': 'A'},
                    {'name': 'B', 'id': 'B'},
                    ],
                editable=False,
                # row_selectable='multi',
                page_size=6,
                style_cell={
                    'whiteSpace': 'normal', 'height': 'auto'
                },
                virtualization=False,
                page_action='none',
                style_cell_conditional=[
                    {'if': {'column_id': 'index'},
                     'width': '25px', 'textAlign': 'center'},
                    {'if': {'column_id': 'A'},
                     'width': '75px', 'textAlign': 'left'},
                    {'if': {'column_id': 'B'},
                     'width': '75px', 'textAlign': 'left'},
                ],
                
                
            )
        ]
    )
