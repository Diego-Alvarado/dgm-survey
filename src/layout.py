import re
import dash_bootstrap_components as dbc
from data_processing import load_df
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import sidebar, layout_question, ids, materials_table, sequence_table

file_names = {i+1: {'materials': str(i).zfill(4) + '_materials.tsv', 'sequences': str(i).zfill(4) + '_sequences.tsv'} for i in range(50)}

def create_layout(app: Dash, database) -> dbc.Container:
    # Set styles
    SIDEBAR_STYLE = {
        'position': 'fixed',
                    'top': 0,
                    'left': 0,
                    'width': '20%',  # Adjust the width as needed
                    'height': '100vh',
                    'overflowY': 'auto',
                    'backgroundColor': '#f8f9fa',  # Adjust the background color as needed
                    'padding': '10px',
                    'zIndex': 1,
    }
    MAINBODY_STYLE={'marginLeft': '20%', 'height': '100%', 'overflowY': 'auto'}
    
    # Load layouts
    number_suvery = len(list(database.list_collections()))
    cll = database[f'survey_{number_suvery}']
    layout_tables = []
    for key in range(1, 51):
        df_materials, df_sequences = load_df(file_names, key)
        ly = layout_question.render(app, df_materials, df_sequences, key, cll)
        layout_tables.append(ly)
    
    # Set callbacks
    @app.callback(Output(ids.PAGE_CONTENT, 'children'), 
                  Input(ids.LOCATION, 'pathname'),
                  prevent_initial_call=True,
                  allow_duplicate=True
                  )
    def render_page_content(pathname: str) -> html.Div:
        if pathname == '/':
            return html.Div('Welcome!'), True, ''
        elif key := re.search(r'\d+', pathname):
            idx = int(key.group()) - 1
            return layout_tables[idx]
        else:
            raise PreventUpdate
        
    return dbc.Container([
        dcc.Location(id=ids.LOCATION, refresh=False),
        dbc.Row([
            dbc.Col(
                html.H1(
                    app.title,
                    style={'fontSize': 36, 'textAlign': 'center'},
                    # className='fixed-title'
                ), width={'size': 8, 'offset': 3}
            ), 
        ], ),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                sidebar.render(app)
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, 
                    style=SIDEBAR_STYLE,
                    ),
            dbc.Col([
                
                # html.Div('Welcome!')
            ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, style=MAINBODY_STYLE,
                    id=ids.PAGE_CONTENT
                    )
            
        ]),
        
        # dbc.Row([
        #     dbc.Col([html.Div([
        #         dbc.Button('Save', className='me-1', disabled=True, id=ids.SAVE_BUTTON),
        #         dbc.Button('Next', className='me-1', id=ids.NEXT_PAGE),
        #         html.Div(id='my-test')
        #         ])
        #     ], width={'offset': 3})
        # ])
        
    ], fluid=True)
