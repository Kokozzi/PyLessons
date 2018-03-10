from flask import Flask, request, abort, Response
from flask_sqlalchemy import SQLAlchemy

import json
from datetime import datetime

import app_config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route("/items", methods=["GET", "POST"])
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
            db.session.commit()
            response = Response(json.dumps(guest_post.as_dict()))
            response.headers["Location"] = "/items/{}".format(guest_post.id)
            return response, 201
        else:
            return "Invalid form"
    else:
        return "Error", 400


@app.route("/items/<item_id>", methods=["GET", "PATCH"])
def item_detail(item_id):
    from models import GuestBookItem
    if request.method == "GET":
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        if guest_post is None:
            abort(404)
        return json.dumps(guest_post.as_dict())
    elif request.method == "PATCH":
        from forms import GuestBookForm
        print(request.form)
        form = GuestBookForm(request.form)
        form.data["updated_at"] = datetime.now()
        print(form.data)
        db_update = db.session.query(GuestBookItem).filter_by(id=item_id).update(form.data)
        db.session.commit()
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        return json.dumps(guest_post.as_dict_updated())
    else:
        return "Error", 400


if __name__ == "__main__":
    from models import *
    db.create_all()
    app.run()