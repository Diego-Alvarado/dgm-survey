import ids
import pandas as pd
import dash_bootstrap_components as dbc

from dash import Dash, html

def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H2('Questions'),
            html.Hr(),
            dbc.Nav(
                [dbc.NavLink([html.Div('Home')], href='/', active='exact')] +
                [
                    dbc.NavLink([html.Div(f'Procedure No. {n + 1}', id=ids.QUESTION_STATUS + str(n + 1))], href=f'/question-{n + 1}', active='exact') for n in range(25)                  
                ] + [dbc.NavLink([html.Div('Submit')], href='/submit')],
                vertical=True,
                pills=True,
                class_name='bg-light',
                # style=SIDEBAR_STYLE
            )
        ],
        
    )
