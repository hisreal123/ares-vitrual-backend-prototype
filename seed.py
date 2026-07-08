import os
from app import app
from models import db, Video

with app.app_context():
    db.create_all()

    for filename in os.listdir('videos'):
        existing = Video.query.filter_by(filename=filename).first()
        if not existing:
            video = Video(filename=filename, title=filename)
            db.session.add(video)

    db.session.commit()