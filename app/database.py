from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

def fetch_locations() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Locations;").fetchall()
    conn.close()
    res = []
    for result in query_results:
        item = {
            "location_id": result[0],
            "loc_name": result[1],
            "business_type": result[2],
            "phys_address": result[3]
        }
    res.append(item)
    return res

def fetch_logins() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Login;").fetchall()
    conn.close()
    res = []
    for result in query_results:
        item = {
            "user_id": result[0],
            "username": result[1],
            "user_password": result[2],
        }
    res.append(item)
    return res

def fetch_reviews() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Reviews;").fetchall()
    conn.close()
    res = []
    for result in query_results:
        item = {
            "location_id": result[0],
            "review_id": result[1],
            "review": result[2],
        }
    res.append(item)
    return res

@app.route("/delete_/<int:task_id>", methods=['POST'])
def delete(task_id):
    try:
        # db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)

@app.route("/search/<string:name>", methods=['POST'])
def update(task_id):
    data = request.get_json()
    print(data)
    try:
        if "status" in data:
            # db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            # db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)

@app.route("/create_review/<string:review>", methods=['POST'])
def create():
    data = request.get_json()
    # db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/")
def homepage():
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items)