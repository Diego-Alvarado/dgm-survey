import pandas as pd
from dash import Dash, html, dash_table, dcc
from rdkit.Chem import MolFromInchi, Draw 

def get_image_file_url(inchi: str, id: str):
    mol = MolFromInchi(inchi)
    if mol:
        filename = f"assets/images/{id}.png"
        Draw.MolToFile(mol, filename, size=(150, 150))
        return f"![{id}]({filename})"

def render(app: Dash, df_materials: pd.DataFrame) -> html.Div:
    # structure = []
    # for inchi, id, name in df_materials[['inchi', 'index', 'name']].itertuples(False):
    #     structure.append(get_image_file_url(inchi, str(id).zfill(5)))

    # df_materials['structure'] = structure
    df_materials['index'] = range(df_materials.shape[0])
    return html.Div(
        children=[
            dash_table.DataTable(
                data=df_materials.to_dict('records'), 
                columns=[
                    {'id': 'index', 'name': ''},
                    {'id': 'role', 'name': 'Role'},
                    {'id': 'name', 'name': 'Name'},
                    {'id': 'inchi', 'name': 'InChi'},
                    # {'id': 'structure', 'name': 'Structure', 'presentation': 'markdown'},
                    ],
                editable=False,
                markdown_options={'html': True},
                # row_selectable='multi',
                page_size=10,
                style_cell={
                    'whiteSpace': 'normal', 'height': 'auto'
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'index'},
                     'width': '10%', 'textAlign': 'center'},
                    {'if': {'column_id': 'role'},
                     'width': '10%', 'textAlign': 'left'},
                    {'if': {'column_id': 'name'},
                     'width': '35%', 'textAlign': 'left'},
                    {'if': {'column_id': 'inchi'},
                     'width': '35%', 'textAlign': 'left'},
                    # {'if': {'column_id': 'structure'},
                    #  'textAlign': 'center', 'width': '10%'},
                ],
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                    } ,
                virtualization=False,
                page_action='none',
                
                
            )
        ]
    )
