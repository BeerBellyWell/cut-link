from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def from_dict(self, data: dict) -> None:
        field_name = {'url': 'original', 'custom_id': 'short', }
        for field, name in field_name.items():
            if field in data:
                setattr(self, name, data[field])
