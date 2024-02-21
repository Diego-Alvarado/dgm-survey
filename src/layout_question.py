import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from PIL import Image
import dash_bootstrap_components as dbc
import ids, materials_table, sequence_table, radio_items


def render(app: Dash, 
           materials: pd.DataFrame, 
           sequences: pd.DataFrame, 
           current_question: int,
           ) -> html.Div:
    
    material = materials_table.render(app, materials)
    sequence = sequence_table.render(app, sequences)
    radio = radio_items.render(app, current_question)
    img_check = Image.open('assets/check.png')
    
    @app.callback(Output(ids.QUESTION_STATUS + str(current_question), 'children'),
                  Input(ids.RESPONSE_RADIO + str(current_question), 'value'))
    def check_questions(value: str) -> html.Div:
        if value == '':
            raise PreventUpdate
        return html.Div([
                html.P(f'Procedure No. {current_question}', style= {'float': 'right'}),
                html.I(html.Img(src=img_check, style={'height':'10%', 'width':'10%', 'display': 'inline'})),
            ],)
        
    @app.callback([Output(ids.INPUT_STORE, 'data', allow_duplicate=True),
                   Output(ids.NEXT_PAGE + str(current_question), 'disabled')],
                  [Input(ids.RESPONSE_RADIO + str(current_question), 'value')],
                  [State(ids.INPUT_STORE, 'data'),
                   State(ids.LOCATION, 'pathname')], 
                  prevent_initial_call=True)
    def store_response(input_value: str, data: dict, pathname: str) -> dict:
        print(f"This is the answer {input_value}")
        if input_value != '':
            print(type(data))
            if not data:
                data = {}
            data[pathname] = input_value
            print(data)
            return data, False
        else:
            raise PreventUpdate
    
    return html.Div(
        className='app-div',
        children=[
            html.H4(f'Procedure No. {current_question}'), 
            html.Br(),
            html.Div("""
                     Consider the following list of reactants and two sequences, "A" and "B," to manufacture a product ('TARGET'). Choose the appropriate sequence of operations that can be executed between "A" and "B" based on the given materials. If it's unclear, you can also choose "Both" or "None".
                     """) ,
            html.Br(),
            html.H6('1. Materials:'),
            html.Div(
                children=[material],
                style={'padding': '10px'}
            ),
            html.Br(),
            html.H6('2. Procedures:'),
            html.Div(
                children=[sequence],
                style={'padding': '10px'}
            ),
            html.Br(),
            html.Div(radio),
            html.Div(id='test' + str(current_question)),
            html.Br(),
            html.Div([
                dcc.Link([
                    dbc.Button('Back', className='me-1', id=ids.NEXT_PAGE + str(current_question)),
                    ], href=f'/question-{current_question - 1}' if current_question > 1 else f'/',
                         refresh=True),
                dcc.Link([
                    dbc.Button('Next', className='me-1', id=ids.NEXT_PAGE + str(current_question), disabled=True),
                    ], href=f'/question-{current_question + 1}' if current_question < 50 else f'/submit',
                         refresh=True),
                
                ])
            
        ],
        
    )