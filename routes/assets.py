from flask import Blueprint, request, send_from_directory
from models import db, Asset

assets_bp = Blueprint('assets', __name__)


@assets_bp.route('/api/admin/assets', methods=['POST'])
def register_asset():
    data = request.get_json()

    required_fields = ('asset_type', 'path', 'owner')
    if not data or any(field not in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400

    asset = Asset(
        asset_type=data.get('asset_type'),
        path=data.get('path'),
        owner=data.get('owner'),
        role=data.get('role'),
        description=data.get('description'),
    )
    db.session.add(asset)
    db.session.commit()

    return asset.to_dict(), 201


@assets_bp.route('/api/admin/assets/<int:asset_id>', methods=['PATCH'])
def update_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return {'error': 'Asset not found'}, 404

    data = request.get_json()
    if not data:
        return {'error': 'No data provided'}, 400

    for field in ('asset_type', 'path', 'owner', 'role', 'description'):
        if field in data:
            setattr(asset, field, data[field])

    db.session.commit()

    return asset.to_dict()


@assets_bp.route('/api/assets', methods=['GET'])
def list_assets():
    assets = Asset.query.all()
    return {'assets': [asset.to_dict() for asset in assets]}


@assets_bp.route('/videos/<path:filename>')
def serve_asset(filename):
    return send_from_directory('videos', filename)
