import re
import json
import pandas as pd
import dash_bootstrap_components as dbc
from data_processing import load_df
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import sidebar, layout_question, ids, main_page, close_page

file_names = {i+1: {'materials': str(i).zfill(4) + '_materials.tsv', 'sequences': str(i).zfill(4) + '_sequences.tsv'} for i in range(50)}

def create_layout(app: Dash) -> dbc.Container:
    # Set styles
    SIDEBAR_STYLE = {
        'position': 'fixed',
                    'top': 0,
                    'left': 0,
                    'width': '20%',  # Adjust the width as needed
                    'height': '100vh',
                    'overflowY': 'auto',
                    'backgroundColor': '#f8f9fa',  # Adjust the background color as needed
                    'padding': '10px',
                    'zIndex': 1,
    }
    MAINBODY_STYLE={'marginLeft': '20%', 'height': '100%', 'overflowY': 'auto'}
    
    # Load layouts
    home = main_page.layout_home(app)
    end = close_page.layout_final_page(app)
    layout_tables = []
    actual_values = {}
    for key in range(1, 51):
        df_materials, df_sequences, actual = load_df(file_names, key)
        ly = layout_question.render(app, df_materials, df_sequences, key)
        actual_values[key] = actual
        layout_tables.append(ly)
    
    # Set callbacks
    @app.callback(Output(ids.PAGE_CONTENT, 'children'), 
                  Input(ids.LOCATION, 'pathname'),
                  prevent_initial_call=True,
                  allow_duplicate=True
                  )
    def render_page_content(pathname: str) -> html.Div:
        if pathname == '/':
            return home
        elif key := re.search(r'\d+', pathname):
            idx = int(key.group()) - 1
            return layout_tables[idx]
        elif pathname == '/submit':
            return end
        else:
            raise PreventUpdate
        
    return dbc.Container([
        dcc.Location(id=ids.LOCATION, refresh=False),
        dcc.Store(id=ids.INPUT_STORE, storage_type='local', data={}),
        dcc.Store(id=ids.GROUND_TRUTH, storage_type='local', data=actual_values),
        dbc.Row([
            dbc.Col(
                html.H1(
                    app.title,
                    style={'fontSize': 36, 'textAlign': 'center'},
                    # className='fixed-title'
                ), width={'size': 8, 'offset': 3}
            ), 
        ], ),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                sidebar.render(app)
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, 
                    style=SIDEBAR_STYLE,
                    ),
            dbc.Col([
            ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, style=MAINBODY_STYLE,
                    id=ids.PAGE_CONTENT
                    ),
        ]),
        
    ], fluid=True)
