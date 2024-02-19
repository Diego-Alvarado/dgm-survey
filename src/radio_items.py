from dash import html, Dash, dcc
import ids

counter = 0

def render(app: Dash, current_question: int) -> html.Div:
    global counter
    counter += 1
    responses = ['A', 'B', 'Both', 'None']
    # @app.callback(
    #     Output(ids.OUTPUT_RESPONSE, 'children'),
    #     Input(ids.RESPONSE_RADIO, 'value'),
    #     prevent_initial_call=True,
    #     allow_duplicate=True,
    # )
    # def show_response(value: str) -> html.Div:
    #     if value == '':
    #         return html.Div('')
    #     return f'{value} OK'
   
    return html.Div(
        children=[
            html.H6('Response: '),
            dcc.RadioItems(
                responses,
                value='',
                id=ids.RESPONSE_RADIO + str(current_question),
            ),
            html.Div(
                id=ids.OUTPUT_RESPONSE + str(current_question),
            )
            
        ]
    )
