from flask import (
    Blueprint, request, jsonify
)
from prp.services.status_service import StatusService

status_bp = Blueprint('status', __name__, url_prefix='/<int:party_state_id>/Status')
status_service = StatusService()

@status_bp.route('/<int:status_id>/Update', methods=['PUT'])
def update_status(party_state_id, status_id):
    body = request.get_json()
    return status_service.update_status(body.get('Status'), party_state_id, status_id)

@status_bp.route('/<int:status_id>/Capture', methods=['PUT'])
def capture_status(party_state_id, status_id):
    body = request.get_json()
    return 'Capture'

@status_bp.route('/<int:status_id>/Retrieve', methods=['GET'])
def retrieve_status(party_state_id, status_id):
    return status_service.retrieve_status(party_state_id, status_id)