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


def update_password(username: str, new_password: str) -> None:
    conn = db.connect()
    query = 'Update Login set user_password = "{}" where username = {};'.format(new_password, username)
    conn.execute(query)
    conn.close()


def insert_new_review(text: str, loc_id: int) ->  int:

    conn = db.connect()
    review_id = np.random.randint(1000,2000)
    user_id = np.random.randint(0,1000)
    query = 'Insert Into Reviews (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id

def insert_new_review(text: str, location_id:int, review_id:int) ->  int:

    conn = db.connect()
    query = 'Insert Into Reviews (location_id, review_id, review) VALUES ("{}", "{}", "{}");'.format(location_id, review_id, text)
    conn.execute(query)
    conn.close()


def remove_review_by_id(review_id: int) -> None:
    """ remove entries based on review ID """
    conn = db.connect()
    query = 'Delete From Review where review_id={};'.format(review_id)
    conn.execute(query)
    conn.close()

def search_location_name(loc_name: str)  -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Locations Where Locations.loc_name is {};".format(loc_name)).fetchall()
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
