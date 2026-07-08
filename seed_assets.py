import os
from app import app
from models import db, Asset

with app.app_context():
    db.create_all()

    for filename in os.listdir('videos'):
        path = f"/videos/{filename}"
        existing = Asset.query.filter_by(path=path).first()
        if not existing:
            asset = Asset(
                asset_type='video',
                path=path,
                owner='Unknown',
                role=None,
                description=None,
            )
            db.session.add(asset)

    db.session.commit()
