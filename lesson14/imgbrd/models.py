from imgbrd_app import db
from wtforms.validators import Length
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(140), nullable=False, info={"validators": Length(min=1)})
    text = db.Column(db.String(500), nullable=False, info={"validators": Length(min=1)})
    header = db.Column(db.String(500), nullable=False, info={"validators": Length(min=1)})
    time_created = db.Column(db.DateTime, default=datetime.now())
    is_visible = db.Column(db.Boolean, default=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False,
        index=True
    )
    author = db.Column(db.String(140), nullable=False, info={"validators": Length(min=1)})
    text = db.Column(db.String(500), nullable=False, info={"validators": Length(min=1)})
    time_created = db.Column(db.DateTime, default=datetime.now())
    is_visible = db.Column(db.Boolean, default=True, nullable=False)