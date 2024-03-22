# Importing the necessary modules and libraries
from flask import Flask
from flask_cors import CORS
from route.myroute import users,lapor
from flask_migrate import Migrate
from model.mymodel import db


app = Flask(__name__)
CORS(app)
app.json.sort_keys = False

#Migrate func
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#Regis route
app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(lapor, url_prefix='/api/lapor')



if __name__ == '__main__':
    app.debug = True
    app.run()