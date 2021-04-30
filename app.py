from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_heroku import Heroku 
from flask_cors import CORS 
from dotenv import load_dotenv
import os

load_dotenv
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://oswbbbewmzsplv:ab8361bd335dccc8c2044521343ffc255068681b5303481301bc6a7eabd2a1ac@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d5l46ejv73c68l"

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique = True, nullable=False)
    content = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, nullable=False)
    def __init__ (self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

class BlogSchema(ma.Schema):
    class Meta:
        feilds = ("id", "title", "content", "user_id")

blog_schema = BlogSchema()
many_blog_schema = BlogSchema(many=True)


@app.route("/blog/add", methods = ["POST"])
def add_blog():
    if request.content_type != "application/json":
        return jsonify("Error: Data needs to be sent as JSON object")

    post_data = request.get_json()
    title = post_data.get("title")
    content = post_data.get("content")
    user_id = post_data.get("user_id")

    record = Blog(title, content, user_id)
    db.session.add(record)
    db.session.commit()

    return jsonify("Congrats your blog has been posted.")

@app.route("/blog/get", methods=["GET"])
def get_all_blog():
    all_blog = db.session.query(Blog).all()
    return jsonify(many_blog_schema.dump(all_blog))

@app.route("/blog/get/title/<title>", methods=["GET"])
def get_blog_by_title(title):
    blog = db.session.query(Blog).filter(Blog.title == title).first()
    return jsonify(blog_schema.dump(blog))

@app.route("/blog/get/id/<id>", methods=["GET"])
def get_blog_by_id(id):
    blog = db.session.query(Blog).filter(Blog.id == id).first()
    return jsonify(blog_schema.dump(blog))

@app.route("/blog/update/<id>", methods = ["PUT"])
def update_blog(id):
    if request.content_type != "application/json":
        return jsonify("Error: Data needs to be sent as JSON object")
    
    put_data = request.get_json()
    title = put_data.get("title")
    content = put_data.get("content")
    user_id = put_data.get("user_id")

    record = db.session.query(Blog).filter(Blog.id == id).first()

    if record is None:
        return jsonify(f"Error: No matching blog with an ID of {id}.")
    if title is None:
        record.title = title
    if content is None:
        record.content = content
    if user_id is None:
        record.user_id = user_id
    
    db.session.commit()

    return jsonify("Blog has been updated")

@app.route("/blog/delete/<id>", methods = ["DELETE"])
def delete_blog(id):
    blog_to_delete = db.session.query(Blog).filter(Blog.id == id).first()
    db.session.delete(blog_to_delete)
    db.session.commit


if __name__ == '__main__':
    app.run(debug=True)