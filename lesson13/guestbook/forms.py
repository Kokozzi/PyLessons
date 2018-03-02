from wtforms_alchemy import ModelForm
from models import GuestBookItem


class GuestBookForm(ModelForm):
    class Meta:
        model = GuestBookItem