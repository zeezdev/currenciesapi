from flask import Flask, Blueprint
from flask_script import Manager
from flask_restplus import Api


app = Flask(__name__)
api = Api(version='1.0', title='Currencies API',
          description='Access to rates of currencies (current and historical) by means of Rest API.')
blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
app.register_blueprint(blueprint)
manager = Manager(app)

from app.create_app import create_app
