import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import ids, materials_table, sequence_table, radio_items


def render(app: Dash, 
           materials: pd.DataFrame, 
           sequences: pd.DataFrame, 
           current_question: int,
           collection
           ) -> html.Div:
    
    @app.callback(Output(ids.SAVE_BUTTON + str(current_question), 'disabled'), 
                  Input(ids.RESPONSE_RADIO + str(current_question), 'value'),
                  prevent_initial_call=True,
                  allow_duplicate=True
                  )
    def activate_save_button(value: str) -> bool:
        if value != '':
            return False
        else:
            raise PreventUpdate

    @app.callback([Output('my-test' + str(current_question), 'children'), 
                   Output(ids.SAVE_BUTTON + str(current_question), 'n_clicks')], 
                  [Input(ids.SAVE_BUTTON + str(current_question), 'n_clicks'), 
                   Input(ids.RESPONSE_RADIO + str(current_question), 'value')],
                  State(ids.SAVE_BUTTON + str(current_question), 'disabled'),
                  prevent_initial_call=True,
                  allow_duplicate=True)
    def save_result(n_clicks: int, value: 'str', disabled: bool) -> str:
        if not disabled and value != '' and n_clicks != None:
            collection.insert_one({
                'question': current_question,
                'reponse': value,
            })
            return f"Your response has been saved. ({value})", None
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
            html.H6('1. List of materials:'),
            html.Div(
                children=[
                    # ''
                    materials_table.render(app, materials),
                ],
                style={'padding': '10px'}, id=ids.MATERIAL_DATAFRAME 
            ),
            html.Br(),
            html.H6('2. Procedures:'),
            html.Div(
                children=[
                    # ''
                    sequence_table.render(app, sequences)
                ],
                style={'padding': '10px'}, id=ids.SEQUENCE_DATAFRAME
            ),
            html.Br(),
            html.Div(radio_items.render(app, current_question)),
            html.Br(),
            html.Div([
                dbc.Button('Save', className='me-1', disabled=True, id=ids.SAVE_BUTTON + str(current_question)),
                dcc.Link([
                    dbc.Button('Next', className='me-1', id=ids.NEXT_PAGE + str(current_question)),
                    ], href=f'/question-{current_question + 1}' if current_question < 50 else f'/question-{current_question}',
                         refresh=True),
                html.Div(id='my-test' + str(current_question))
                ])
            
        ],
        
    )