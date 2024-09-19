from flask import (
    Blueprint, request, jsonify
)
from prp.services.rating_service import RatingService

rating_bp = Blueprint('rating', __name__, url_prefix='/<int:party_state_id>/Rating')
rating_service = RatingService()

@rating_bp.route('/<int:rating_id>/Update', methods=['PUT'])
def update_rating(party_state_id, rating_id):
    body = request.get_json()
    return rating_service.update_rating(body.get('Rating'), party_state_id, rating_id)

@rating_bp.route('/<int:rating_id>/Capture', methods=['PUT'])
def capture_rating(party_state_id, rating_id):
    body = request.get_json()
    return 'Capture'

@rating_bp.route('/<int:rating_id>/Retrieve', methods=['GET'])
def retrieve_rating(party_state_id, rating_id):
    return rating_service.retrieve_rating(party_state_id, rating_id)