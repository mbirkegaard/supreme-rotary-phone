from flask import Flask
from flask_graphql import GraphQLView
from document_manager.document_manager import DocumentManager

document_manager = DocumentManager()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

from graphql_api import make_schema


app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view(
                     'graphql',
                     schema=make_schema(document_manager),
                     graphiql=True
                 ))