from flask import Flask 

app = Flask(__name__)

app.secret_key = app.config['SECRET_KEY']
app.config.from_object("config")

