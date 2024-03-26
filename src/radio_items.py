from dash import html, Dash, dcc, no_update
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import ids


def render(app: Dash, current_question: int) -> html.Div:
    responses = ['A', 'B', 'Both', 'None']
   
    return html.Div(
        children=[
            html.H6('Response: '),
            dcc.RadioItems(
                options= [{'label': i, 'value': i } for i in responses] ,
                value='',
                id=ids.RESPONSE_RADIO + str(current_question),
                persistence=True,
                persistence_type='session'
            ),
            html.Div(
                id=ids.OUTPUT_RESPONSE + str(current_question),
            )
            
        ]
    )
