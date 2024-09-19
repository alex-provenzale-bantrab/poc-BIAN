from flask import (
    Blueprint, request, jsonify
)
from prp.services.party_state_service import PartyStateService

party_state_bp = Blueprint('party_state', __name__, url_prefix='/PartyRoutingProfile')
party_state_service = PartyStateService()

@party_state_bp.route('/Initiate', methods=['POST'])
def initiate_party_state():
    body = request.get_json()
    return party_state_service.initiate_profile_state_monitoring(body)

@party_state_bp.route('/<int:party_state_id>/Update', methods=['PUT'])
def update_party_state(party_state_id):
    body = request.get_json()
    return party_state_service.update_party_state(body, party_state_id)

@party_state_bp.route('/<int:party_state_id>/Execute', methods=['PUT'])
def execute_party_state(party_state_id):
    body = request.get_json()
    return 'Execute'

@party_state_bp.route('/<int:party_state_id>/Request', methods=['PUT'])
def request_party_state(party_state_id):
    body = request.get_json()
    return 'Request'

@party_state_bp.route('/<int:party_state_id>/Retrieve', methods=['GET'])
def retrieve_party_state(party_state_id):
    return party_state_service.retrieve_party_state(party_state_id)
