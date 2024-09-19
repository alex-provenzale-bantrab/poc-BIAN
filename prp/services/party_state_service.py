from prp.repositories import PartyStateRepository
from prp.schemas import PartyState
from prp.services.alert_service import AlertService
from prp.services.rating_service import RatingService
from prp.services.status_service import StatusService
from prp.utils import format_error_response

class PartyStateService:
    def __init__(self):
        self.schema = PartyState()
        self.party_state_repository = PartyStateRepository()
        self.alert_service = AlertService()
        self.rating_service = RatingService()
        self.status_service = StatusService()
    
    def initiate_profile_state_monitoring(self, body):
        errors = self.schema.validate(body)
        if errors:
            return format_error_response(message=errors), 400
        # TODO: Get here the db connection
        verify_party_state = self.party_state_repository.selectPartyStateByCustomerReference(body)
        if verify_party_state:
            return format_error_response(message=f"Customer reference {body.get('CustomerReference')} already monitored"), 400
        
        party_state = self.party_state_repository.insertPartyState(body)
        
        party_state_id = party_state.get('PartyStateId')
        
        alert = self.alert_service.initiate_alert_monitoring(party_state_id)
        rating = self.rating_service.initiate_rating_monitoring(party_state_id)
        status = self.status_service.initiate_status_monitoring(party_state_id)
        # TODO: Commit here the changes to the db. If error then rollbacks
        
        return {'PartyState': self.schema.dump(party_state)}, 201
    
    def update_party_state(self, body, party_state_id):
        errors = self.schema.validate(body)
        if errors:
            return format_error_response(message=errors), 400
        verify_party_state = self.party_state_repository.selectPartyStateById(party_state_id)
        if not verify_party_state:
            return format_error_response(message=f"Party State with id {party_state_id} not found"), 404
        party_state = self.party_state_repository.updatePartyState(body, party_state_id)
        return {'PartyState': self.schema.dump(party_state)}, 200

    def retrieve_party_state(self, party_state_id):
        verify_party_state = self.party_state_repository.selectPartyStateById(party_state_id)
        if not verify_party_state:
            return format_error_response(message=f"Party State with id {party_state_id} not found"), 404
        return {'PartyState': self.schema.dump(verify_party_state)}, 200