from guestbook_app import db
from wtforms.validators import Length
from datetime import datetime

class GuestBookItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(140), nullable=False)
    text = db.Column(db.String(500), nullable=False, info={"validators": Length(min=5)})
    time_created = db.Column(db.DateTime, default=datetime.now())
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def as_dict(self):
        return {
            "author": self.author,
            "text": self.text,
            "time_created": self.time_created.isoformat(),
        }