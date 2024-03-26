import pandas as pd
from pathlib import Path
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from PIL import Image
from data_processing import load_df, load_mats, load_seqs
import dash_bootstrap_components as dbc
import ids, materials_table, sequence_table, radio_items

q = 25

def render(app: Dash, 
           current_question: int,
           ) -> html.Div:
    
    
    radio = radio_items.render(app, current_question)
    
    @app.callback(Output(ids.MATERIAL_DATAFRAME + str(current_question), 'children'),
                  Input(ids.PATH_SURVEY, 'data'),
                #   prevent_initial_callbacks=True,
                #   allow_duplicate=True
                  )
    def update_materials(files: str) -> html.Div:
        if not files:
            raise PreventUpdate
        q = 2 * current_question
        df = load_mats(files[q])
        # print(df)
        return materials_table.render(app, df)
    
    @app.callback(Output(ids.SEQUENCE_DATAFRAME + str(current_question), 'children'),
                  Input(ids.PATH_SURVEY, 'data'))
    def update_sequences(files: str) -> html.Div:
        if not files:
            raise PreventUpdate
        q = 2 * current_question + 1
        df, actual = load_seqs(files[q], seed=q)
        # print(df)
        return sequence_table.render(app, df)
        
    @app.callback([Output(ids.INPUT_STORE, 'data', allow_duplicate=True),
                   Output(ids.NEXT_PAGE + str(current_question), 'disabled')],
                  [Input(ids.RESPONSE_RADIO + str(current_question), 'value')],
                  [State(ids.INPUT_STORE, 'data'),
                   State(ids.LOCATION, 'pathname')], 
                  prevent_initial_call=True)
    def store_response(input_value: str, data: dict, pathname: str) -> dict:
        # print(f"This is the answer {input_value}")
        if input_value != '':
            # print(type(data))
            if not data:
                data = {}
            data[pathname] = input_value
            # print(data)
            return data, False
        else:
            raise PreventUpdate
    
    return html.Div(
        className='app-div',
        children=[
            html.H4(f'Procedure No. {current_question + 1}'), 
            html.Br(),
            html.Div("""
                     Consider the following list of reactants and two sequences, "A" and "B," to manufacture a product ('TARGET'). Choose the appropriate sequence of operations that can be executed between "A" and "B" based on the given materials. If it's unclear, you can also choose "Both" or "None".
                     """) ,
            html.Br(),
            html.H6('1. Materials:'),
            html.Div(
                children='',
                style={'padding': '10px'},
                id=ids.MATERIAL_DATAFRAME + str(current_question)
            ),
            html.Br(),
            html.H6('2. Procedures:'),
            html.Div(
                children='',
                style={'padding': '10px'},
                id=ids.SEQUENCE_DATAFRAME + str(current_question)
            ),
            html.Br(),
            html.Div(radio),
            html.Div(id='test' + str(current_question)),
            html.Br(),
            html.Div([
                dcc.Link([
                    dbc.Button('Back', className='me-1', id=ids.NEXT_PAGE + str(current_question)),
                    ], href=f'/question-{current_question}' if current_question > 0 else f'/',
                         refresh=True),
                dcc.Link([
                    dbc.Button('Next', className='me-1', id=ids.NEXT_PAGE + str(current_question), disabled=True),
                    ], href=f'/question-{current_question + 2}' if current_question < 24 else f'/submit',
                         refresh=True),
                
                ])
            
        ],
        
    )