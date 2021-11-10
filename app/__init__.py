import os
import sqlalchemy
from yaml import load, Loader

from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQl_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )
    return pool

db = init_connect_engine()

conn = db.connect()
results = conn.execute("Select * from tasks;").fetchall()
print(x for x in results)
conn.close()

@app.route("/")
def homepage():
    return jsonify({"status": "OK"})
    return render_template("index.html", name = "Tara")

from app import routes
