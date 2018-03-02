from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
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
            return "Success"
        else:
            return "Invalid form"
    else:
        return "Error"


if __name__ == "__main__":
    from models import *
    db.create_all()
    app.run()