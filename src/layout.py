import re
import json
import random
import pandas as pd
import dash_bootstrap_components as dbc
from pathlib import Path
from data_processing import load_df, load_mats
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import sidebar, layout_question, ids, main_page, close_page, materials_table


def create_layout(app: Dash) -> dbc.Container:
    
    
    files = Path('data/01/').glob('*tsv')
    files = sorted(files, key=lambda x: x.name) 
    files = {(i + 2)//2: {'materials': files[i].absolute().as_posix(), 'sequences': files[i + 1]} for i in range(0, len(files), 2)}
    
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
    PROGRESS_STYLE={'marginLeft': '20%'}
    
    # Load layouts
    home = main_page.layout_home(app)
    end = close_page.layout_final_page(app)
    layout_tables = []
    actual_values = {}
    for key in range(25):
        ly = layout_question.render(app, key)
        cols = ['A', 'B']
        random.seed(2*key + 1)
        random.shuffle(cols)
        actual_values[key + 1] = {'actual': cols[0], 'generated': cols[1]}
        layout_tables.append(ly)
        
    @app.callback(Output(ids.PAGE_CONTENT, 'children'), 
                  [Input(ids.LOCATION, 'pathname')],
                #   prevent_initial_call=True,
                  allow_duplicate=True
                  )
    def render_page_content(pathname: str) -> html.Div:
        # arrange survey layout
        if pathname == '/':
            return home
        elif key := re.search(r'\d+', pathname):
            idx = int(key.group()) - 1
            return layout_tables[idx]
        elif pathname == '/submit':
            return end
        else:
            raise PreventUpdate
        
        
    @app.callback([Output(ids.PROGRESS_BAR, 'label'), 
                   Output(ids.PROGRESS_BAR, 'value')],
                  Input(ids.INPUT_STORE, 'data'))
    def update_progress(data: dict):
        n = len(data)
        label = f'Progress: {n}/25'
        value = n/25*100
        return label, value
        
    return dbc.Container([
        dcc.Location(id=ids.LOCATION, refresh=False),
        dcc.Store(id=ids.INPUT_STORE, storage_type='local', data={}),
        dcc.Store(id=ids.PATH_SURVEY, storage_type='local', data=[]),
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
            dbc.Row([
                dbc.Col(dbc.Progress(value=75, label='Progress: 0/25', style={'height': '35px'}, id=ids.PROGRESS_BAR), 
                        xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, style=PROGRESS_STYLE),
                dbc.Col(html.Br()),
                dbc.Col([], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, style=MAINBODY_STYLE,
                    id=ids.PAGE_CONTENT),
            ])
            
        ]),
        
    ], fluid=True)
