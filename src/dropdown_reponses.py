import csv
from dash import html, Dash, dcc
from dash.dependencies import Input, Output

from . import ids

def render(app: Dash, current_question: int) -> html.Div:
    responses = ['A', 'B', 'Both', 'None']
    my_dict = {'question': current_question, 'answer': None}
    @app.callback(
        Output(ids.OUTPUT_RESPONSE, 'children'),
        [Input(ids.RESPONSE_DROPDOWN, 'value')]
    )
    def show_response(response: str) -> html.Div:
        if response == '':
            return html.Div('')
        # my_dict['answer'] = response
        # with open('assets/collected_data/results.csv', 'a+') as f:
        #     writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
        #     writer.writeheader()
        #     writer.writerow(my_dict)
        return html.Div(f"You have chosen '{response}'")
   
    return html.Div(
        children=[
            html.H6('Response: '),
            dcc.Dropdown(
                id=ids.RESPONSE_DROPDOWN,
                options=[{'label': response, 'value': response} for response in responses],
                value='',
                multi=False,
            ),
            html.Div(
                'No reponse yet',
                id=ids.OUTPUT_RESPONSE,
            )
            
        ]
    )
