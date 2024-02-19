from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids

def render(app: Dash) -> html.Div:
    return html.Div(
        html.Button(
            className='next-button',
            children=['Next Page'],
            id=ids.NEXT_PAGE,
        )
    )