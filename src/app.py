import pymongo
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from layout import create_layout
import database_access

app = Dash(__name__, external_stylesheets=[BOOTSTRAP],
               suppress_callback_exceptions=True,
               assets_folder='./src/assets')
server = app.server

client = pymongo.MongoClient(database_access.LINK)
db = client.get_database('dgm_validation')

app.title = 'Deep Generative Models for Pharmaceutical Process Design - Survey'
app.layout = create_layout(app, db)
    
if __name__ == '__main__':
    app.run_server(debug=True)
