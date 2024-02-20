from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from PIL import Image

def layout_home(app: Dash) -> html.Div:
    img = Image.open('assets/Picture1.png')
    return html.Div([
        # html.H4('Background'),
        html.P("""
               Deep generative models (DGMs) are neural networks capable of generating realistic
                samples and learning hidden information. Most popular developments in this area 
                include GPT, Dall-E and midjourney applied to generate text and images. DGMs have 
                been employed in fields such as drug discovery to generate new drug candidates with 
                desirable biological and chemical properties. Nonetheless, applications in 
                pharmaceutical manufacturing have not been fully explored. 
               """),
        html.P("""
               In primary manufacturing domain, we have developed deep generative models to create sequences 
               of unit operations tailored for the production of specific products. These models 
               leverage information about process materials and target product properties to 
               generate operation chains. 
               """),
        html.Div(
            [html.Img(src=img,
                      style={
                'height': '40%',
                'width': '40%'})],
            style={'textAlign': 'center'}
            ),
        html.P("""
               This survey aims to explore the feasibility of executing the generated sequences in a 
               laboratory environment and their comparability to actual manufacturing procedures through
               the review of experts. In the next pages, you will find 50 procedures of manufacturing 
               generated using DGMs and the actual procedure for different substance with the process 
               materials. Please compare the sequences and select which is more feasible to be
               executed in a lab.
               """),
        dcc.Link([
                    dbc.Button('Next', className='me-1'),
                    ], href=f'/question-1',
                         refresh=True)
    ])