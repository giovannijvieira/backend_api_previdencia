from flask import Flask, jsonify
from app.models import db, ma
from app.routes import api
from flask_apispec import FlaskApiSpec, use_kwargs, marshal_with
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flasgger import Swagger


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

app.config['SWAGGER'] = {
    'title': 'API Docs',
    'uiversion': 3,
    'specs_route': '/apidocs/',
    'openapi': '3.0.2'
}

swagger = Swagger(app, template_file='./openapi.yaml')

app.register_blueprint(api, url_prefix="/api")

@app.route('/')
def health_check():
    return jsonify(status="OK"), 200

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
