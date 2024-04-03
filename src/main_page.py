from pathlib import Path
from dash import html, Dash, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from PIL import Image
import ids

def layout_home(app: Dash) -> html.Div:
    img = Image.open('assets/Picture1.png')
    
    
    @app.callback(Output(ids.PATH_SURVEY, 'data'),
                  Input(ids.SURVEY_NUMBER, 'value'))
    def store_path(value: str) -> list[str]:
        files = Path(value).glob('*.tsv')
        files = sorted(files, key=lambda x: x.name) 
        files = [value + f.name for f in files]
       #  print(files)
        return files
    
    
    return html.Div([
        # html.H4('Background'),
        html.P("""
               Deep generative models (DGMs) are neural networks capable of generating realistic
                samples and learning hidden information. Most popular developments in this area 
                include GPT, Dall-E and Midjourney applied to generate text and images. DGMs have 
                been employed in fields such as drug discovery to generate new drug candidates with 
                desirable biological and chemical properties. Nonetheless, their applications in 
                pharmaceutical manufacturing have not been fully explored. 
               """),
        html.P("""
               In primary manufacturing domain, we have developed deep generative models to create sequences of unit operations tailored 
               for the production of specific products. These models leverage information about process materials and target product 
               to generate a suitable chain of operations.
               """),
        html.Div(
            [html.Img(src=img,
                      style={
                'height': '40%',
                'width': '40%'})],
            style={'textAlign': 'center'}
            ),
        html.P("""
               This survey aims to explore the plausibility of the generated sequences to be executed in a laboratory environment and their comparability to actual manufacturing 
               procedures through the review of experts. In the following pages, you will find 25 manufacturing procedures generated using DGMs, alongside the 
               corresponding actual procedures for various substances, including the processing materials. Please compare the sequences and indicate which is more 
               likely to be executed in a lab.
               """),
        html.P('\nPlease select survey number: '),
        dcc.Dropdown(options={f'data/0{v}/': v for v in range(1, 5)}, id=ids.SURVEY_NUMBER, value='src/data/01/', persistence=True),
        dcc.Link([
                    dbc.Button('Next', className='me-1', id=ids.HOME_BUTTON, disabled=False),
                    ], href=f'/question-1',
                         refresh=True)
    ])