from app import app
from flask import render_template
from app import database as db_helper
from flask import render_template, request, jsonify, url_for, flash, redirect, Flask
from app import forms as forms
from flaskblog.forms import SearchForm, LoginForm, UpdateAccountForm, PostForm
from app import db

@app.route('/')
@app.route("/home")
def login():
    return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/user_profile")
def user_profile():
    return render_template("user_profile.html")

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        conn = db.connect()
        conn.execute('Insert Into Reviews (location_id, user_id, review) VALUES ("{}", "{}", "{}", "{}");'.format(
            form.title.data, forms.LOGGED_USER, form.content.data))
        conn.close()
        flash('Your post has been created! Thank you for your review!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@app.route("/post/<int:review_id>/delete", methods=['POST'])
def delete_review(review_id):
    conn = db.connect()
    conn.execute(
        "DELETE FROM Reviews WHERE review_id = '{}';".format(review_id))
    conn.close()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/search", methods=['GET', 'POST'])
def search_review():
    form = forms.SearchForm()
    posts = []
    if form.validate_on_submit():
        conn = db.connect()
        results = conn.execute(
            "SELECT * FROM Reviews WHERE location_id = '{}';".format(form.loc_name.data)).fetchall()
        count = conn.execute("SELECT COUNT(location_id) FROM Reviews WHERE location_id = '{}' GROUP BY location_id;".format(
            form.loc_name.data)).fetchall()
        if len(results) == 0:
            flash('The restaurant you searched does not exist', 'danger')
            return redirect(url_for('search_review'))
        conn.close()
        for result in results:
            item = {
                "location_id": result[0],
                "review_id": result[1],
                "user_id": forms.LOGGED_USER,
                "review": result[3]
            }
            posts.append(item)
    return render_template('search.html', posts=posts, form=form)


@app.route("/post/<int:ReviewNumber>/update", methods=['GET', 'POST'])
def update_review(review_id):
    conn = db.connect()
    post = []
    result = conn.execute(
        "SELECT * FROM Reviews WHERE review_id = '{}';".format(review_id)).fetchall()
    item = {
        "location_id": result[0],
        "review_id": result[1],
        "user_id": forms.LOGGED_USER,
        "review": result[3]
    }
    post.append(item)
    form = forms.ReviewsForm()
    if form.validate_on_submit():
        post[0]["location_id"] = form.title.data
        post[0]["user_id"] = forms.LOGGED_USER
        post[0]["review"] = form.content.data
        commit = conn.execute("Update Reviews SET review = '{}', location_id = '{}' WHERE review_id = '{}';".format(
            form.content.data, form.title.data, review_id))
        flash('Your review has been updated!', 'success')
        return redirect(url_for('access_reviews', review_id=review_id))
    elif request.method == 'GET':
        form.title.data = post[0]["location_id"]
        form.content.data = post[0]["review"]
        forms.LOGGED_USER = post[0]["user_id"]
    conn.close()
    return render_template('create_review.html', title='Update Review',
                           form=form, legend='Update Review')

@app.route("/studyspaces", methods=['GET', 'POST'])
def studyspaces():
    advanced_query = db_helper.study_space()
    return render_template("index.html", query=advanced_query[0])

@app.route("/countReviews", methods=['GET', 'POST'])
def countReviews():
    advanced_query = db_helper.count_reviews()
    return render_template("index.html", query=advanced_query[0])