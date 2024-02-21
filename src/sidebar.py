import ids
import pandas as pd
import dash_bootstrap_components as dbc

from dash import Dash, html

file_names = {i: {'materials': str(i).zfill(4) + '_materials.tsv', 'sequences': str(i).zfill(4) + '_sequences.tsv'} for i in range(50)}

def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H2('Questions'),
            html.Hr(),
            dbc.Nav(
                [dbc.NavLink([html.Div('Home')], href='/', active='exact')] +
                [
                    dbc.NavLink([html.Div(f'Procedure No. {n + 1}', id=ids.QUESTION_STATUS + str(n + 1))], href=f'/question-{n + 1}', active='exact') for n in file_names                  
                ] + [dbc.NavLink([html.Div('Submit')], href='/submit')],
                vertical=True,
                pills=True,
                class_name='bg-light',
                # style=SIDEBAR_STYLE
            )
        ],
        
    )
