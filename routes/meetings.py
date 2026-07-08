from flask import Blueprint, request
from helpers import generate_meeting_id, generate_passcode
from models import Meeting, MeetingAsset, Asset, db

meetings_bp = Blueprint('meetings', __name__)  # constructor

@meetings_bp.route('/api/meetings/create', methods=['POST'])
def create_meeting_route():
    data = request.get_json()

    required_fields = ('title', 'host_name', 'size', 'asset_ids')
    if not data or any(field not in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400

    size = data.get('size')
    asset_ids = data.get('asset_ids')

    if len(asset_ids) != size:
        return {'error': 'Number of asset_ids must match size'}, 400

    found_assets = Asset.query.filter(Asset.id.in_(asset_ids)).all()
    if len(found_assets) != len(set(asset_ids)):
        return {'error': 'One or more asset_ids do not exist'}, 400

    meeting = Meeting(
        meeting_id=generate_meeting_id(),
        passcode=generate_passcode(),
        title=data.get('title'),
        host_name=data.get('host_name'),
        size=size,
    )
    db.session.add(meeting)
    db.session.flush()  # assign meeting.id before creating MeetingAsset rows

    for slot_number, asset_id in enumerate(asset_ids):
        db.session.add(MeetingAsset(meeting_id=meeting.id, asset_id=asset_id, slot_number=slot_number))

    db.session.commit()

    return meeting.to_dict(), 201
