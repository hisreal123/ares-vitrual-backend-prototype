from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(20), nullable=False)  # 'video' or 'image'
    path = db.Column(db.String(255), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_type': self.asset_type,
            'path': self.path,
            'owner': self.owner,
            'role': self.role,
            'description': self.description,
        }


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.String(100), nullable=False, unique=True)
    passcode = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    host_name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_ended = db.Column(db.Boolean, nullable=False, default=False)
    is_expired = db.Column(db.Boolean, nullable=False, default=False)

    assets = db.relationship('MeetingAsset', backref='meeting', order_by='MeetingAsset.slot_number')

    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'passcode': self.passcode,
            'title': self.title,
            'host_name': self.host_name,
            'size': self.size,
            'current_participants': self.current_participants,
            'created_at': self.created_at.isoformat(),
            'is_ended': self.is_ended,
            'is_expired': self.is_expired,
            'assets': [ma.asset.to_dict() for ma in self.assets],
        }


class MeetingAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    slot_number = db.Column(db.Integer, nullable=False)

    asset = db.relationship('Asset')