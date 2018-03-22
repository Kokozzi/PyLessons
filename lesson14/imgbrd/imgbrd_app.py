from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import json
import app_config as config

# Create Flask Application
app = Flask(__name__, template_folder='templates')
app.config.from_object(config)
# Create database object
db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def index():
    from models import Post, Comment
    from forms import PostForm, CommentForm
    # Retrieve all posts from DB
    if request.method == 'GET':
        posts = Post.query.all()
        result = []
        for post in posts:
            # Retrieve comments that belong to this post
            comments = Comment.query.filter_by(post_id = post.id)
            result.append({"post": post, "comments": comments})
        # Render Blog template
        return render_template('index.html', data=result)
    # Creating post or comment
    elif request.method == "POST":
        # 'request_type' is 'post' or 'comment'
        request_type = request.form.get("request_type")
        # Creating Post
        if request_type == "post":
            form = PostForm(request.form)
            if form.validate():
                post = Post(**form.data)
                db.session.add(post)
                db.session.commit()
                return "Post saved"
            else:
                return "Erorr", 400
        # Creating comment for post
        elif request_type == "comment":
            form = CommentForm(request.form)
            if form.validate():
                comment = Comment(**form.data)
                db.session.add(comment)
                db.session.commit()
                return "Comment saved"
            else:
                return "Erorr", 400
        else:
            return "Wrong request type", 400

if __name__ == "__main__":
    from models import *
    db.create_all()
    app.run()