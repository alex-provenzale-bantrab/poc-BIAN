from flask import (
    Blueprint, request, jsonify
)
from prp.services.alert_service import AlertService

alert_bp = Blueprint('alert', __name__, url_prefix='/<int:party_state_id>/Alert')
alert_service = AlertService()

@alert_bp.route('/<int:alert_id>/Update', methods=['PUT'])
def update_alert(party_state_id, alert_id):
    body = request.get_json()
    return alert_service.update_alert(body.get('Alert'), party_state_id, alert_id)

@alert_bp.route('/<int:alert_id>/Capture', methods=['PUT'])
def capture_alert(party_state_id, alert_id):
    body = request.get_json()
    return 'Capture'

@alert_bp.route('/<int:alert_id>/Retrieve', methods=['GET'])
def retrieve_alert(party_state_id, alert_id):
    return alert_service.retrieve_alert(party_state_id, alert_id)