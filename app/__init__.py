from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

# @app.route("/")
# def homepage():
#     return jsonify({"status": "OK"})
#     return render_template("index.html", name = "Tara")

from app import routes
