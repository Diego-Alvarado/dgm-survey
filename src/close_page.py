import re
import pymongo
import pandas as pd
import ids
import dash_bootstrap_components as dbc
import plotly.express as px
import database_access
from dash import Dash, dcc, html, dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State
import datetime as dt

client = pymongo.MongoClient(database_access.LINK)

def layout_final_page(app: Dash) -> html.Div:
    
    @app.callback(Output(ids.SUMMARY, 'children'),
                  Input(ids.INPUT_STORE, 'data'),
                #   prevent_initial_call=True, 
                  allow_duplicate=True)
    def show_store_data(data: dict) -> html.Div:
        print(f"This is the results{data}")
        if not data:
            raise PreventUpdate
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.reset_index()
        df.columns = ['Question', 'Answer']
        df['Question'] = df['Question'].apply(lambda x: int(s.group()) if (s:=re.search(r'\d+', x)) else None)
        df = df.sort_values(by='Question')
        df_values = df['Answer'].value_counts(normalize=True).reset_index()
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                    {'id': 'Question', 'name': 'Question'},
                    {'id': 'Answer', 'name': 'Answer'},
                    ],
                editable=False,
                markdown_options={'html': True},
                style_table={'height': '350px', 'overflowY': 'auto'},
                style_cell={
                    'whiteSpace': 'normal', 'height': 'auto'
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'Question'},
                     'width': '100px', 'textAlign': 'center'},
                    {'if': {'column_id': 'Answer'},
                     'width': '100px', 'textAlign': 'center'},
                ],
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                    } ,
                virtualization=True,
                page_action='none',
                fill_width=True,
                fixed_rows={'headers': True}
            )
        figure = px.pie(df_values, names='Answer', values='proportion', hole=0.3)
        return dbc.Container([
            dbc.Row([
                dbc.Col(table),
                dbc.Col(dcc.Graph(figure=figure))
            ])
        ])
    
    @app.callback(Output(ids.SUBMIT_OK, 'children'), 
                  Input(ids.SUBMIT_RESULTS, 'n_clicks'),
                  State(ids.INPUT_STORE, 'data'),
                  prevent_initial_call=True, 
                  allow_duplicate=True)
    def save_results(n_clicks: int, data: dict) -> str:
        if not data and not n_clicks:
            raise PreventUpdate
        db = client.get_database('dgm_validation')
        now = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        cll = db[now]
        cll.insert_one(data)
        print(data)
        return f'Your answers have been saved ({now}).'
    
    return html.Div([
        html.P('Thank you very much for your participation. Please find below your answers consolidated. Press "SUBMIT" to save the results.'),
        html.Div(id=ids.SUMMARY),
        html.Div(id=ids.SUBMIT_OK),
        dcc.Link([dbc.Button('Back', className='me-1',)], href='/question-50'),
        dbc.Button('Submit', className='me-1', id=ids.SUBMIT_RESULTS)
    ])

