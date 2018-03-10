from flask import Flask, request, abort, Response
from flask_sqlalchemy import SQLAlchemy

import json
from datetime import datetime

import app_config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route("/items", methods=["GET", "POST", "PUT"])
def items():
    from models import GuestBookItem
    from forms import GuestBookForm
    if request.method == "GET":
        guest_posts = GuestBookItem.query.all()
        if len(guest_posts) == 0:
            return "Guestbook is empty"
        posts_list = []
        for post in guest_posts:
            posts_list.append(post.as_dict())
        return json.dumps(posts_list)
    elif request.method == "POST":
        form = GuestBookForm(request.form)
        if form.validate():
            guest_post = GuestBookItem(**form.data)
            db.session.add(guest_post)
            print(form.data)
            db.session.commit()
            response = Response(json.dumps(guest_post.as_dict()))
            response.headers["Location"] = "/items/{}".format(guest_post.id)
            return response, 201
        else:
            return "Invalid form"
    elif request.method == "PUT":
        if len(request.form) == 0:
            db.session.query(GuestBookItem).delete()
            db.session.commit()
            return (json.dumps(GuestBookItem.query.all()))
        return "Error", 400
    else:
        return "Error", 400


@app.route("/items/<item_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def item_detail(item_id):
    from models import GuestBookItem
    if request.method == "GET":
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        if guest_post is None:
            abort(404)
        return json.dumps(guest_post.as_dict())
    elif request.method == "PATCH":
        post_id = request.form.get("id")
        if post_id is None:
            abort(404)
        update_dict = {}
        author = request.form.get("author")
        if author is not None:
            update_dict["author"] = author
        text = request.form.get("text")
        if text is not None and len(text) >= 5:
            update_dict["text"] = text
        if len(update_dict) == 0:
            return "Empty update", 400
        update_dict["updated_at"] = datetime.now()
        db_update = db.session.query(GuestBookItem).filter_by(id=post_id)
        if db_update.first() is None:
            abort(404)
        else:
            db_update.update(update_dict)
        db.session.commit()
        guest_post = GuestBookItem.query.filter_by(id=post_id).first()
        return json.dumps(guest_post.as_dict_updated())
    elif request.method == "PUT":
        from forms import GuestBookForm
        post_id = request.form.get("id")
        if post_id is None:
            abort(404)
        form = GuestBookForm(request.form)
        if form.validate():
            db_update = db.session.query(GuestBookItem).filter_by(id=post_id)
            if db_update.first() is None:
                abort(404)
            else:
                db_update.update(form.data)
            db.session.commit()
            guest_post = GuestBookItem.query.filter_by(id=post_id).first()
            return json.dumps(guest_post.as_dict_updated())
        else:
            return "Invalid form", 400
    elif request.method == "DELETE":
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        if guest_post is None:
            return "Unknown number", 204
        else:
            db.session.query(GuestBookItem).filter_by(id=item_id).update({"is_visible": False})
            db.session.commit()
            return "Deleted", 200
    else:
        return "Error", 400


if __name__ == "__main__":
    from models import *
    db.create_all()
    app.run()