from guestbook_app import db
from wtforms.validators import Length
from datetime import datetime


class GuestBookItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(140), nullable=False)
    text = db.Column(db.String(500), nullable=False, info={"validators": Length(min=5)})
    time_created = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def as_dict(self, fields=[]):
        # Default behaviour - return predefined fields
        if len(fields) == 0:
            return {
                "author": self.author,
                "text": self.text,
                "time_created": self.time_created.isoformat(),
                "is_visible": self.is_visible,
            }
        # Return only requested fields
        else:
            result = {}
            for key in fields:
                # Check if key realy exists at Model
                if key not in [column.key for column in GuestBookItem.__table__.columns]:
                    continue
                # Special formatting for DateTime fields
                if key in ["time_created", "updated_at"]:
                    result[key] = getattr(self, key).isoformat()
                else:
                    result[key] = getattr(self, key)
            return result

    def as_dict_updated(self):
        return {
            "author": self.author,
            "text": self.text,
            "time_created": self.time_created.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }