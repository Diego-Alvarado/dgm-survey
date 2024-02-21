import pandas as pd
from dash import Dash, html, dash_table
from rdkit.Chem import MolFromInchi, Draw 

def render(app: Dash, df_materials: pd.DataFrame) -> html.Div:
    
    df_materials['index'] = range(df_materials.shape[0])
    img = Draw.MolsToGridImage([MolFromInchi(inchi) for inchi in df_materials['inchi']], 
                     legends=[f"{role} ({i})" for i, role in enumerate(df_materials['role'])],
                     molsPerRow=4, subImgSize=(200, 200))
    df_materials = df_materials.drop(columns=['inchi'])
    
    return html.Div(
        children=[
            dash_table.DataTable(
                data=df_materials.to_dict('records'), 
                columns=[
                    {'id': 'index', 'name': ''},
                    {'id': 'role', 'name': 'Role'},
                    {'id': 'name', 'name': 'Name'},
                    ],
                editable=False,
                markdown_options={'html': True},
                # row_selectable='multi',
                # page_size=10,
                style_cell={
                    'whiteSpace': 'normal', 'height': 'auto'
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'index'},
                     'width': '5%', 'textAlign': 'center'},
                    {'if': {'column_id': 'role'},
                     'width': '5%', 'textAlign': 'left'},
                    {'if': {'column_id': 'name'},
                      'textAlign': 'left'},
                ],
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                    } ,
                virtualization=False,
                # page_action='none',
            ),
            html.Img(src=img)
        ]
    )
