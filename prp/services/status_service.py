from prp.repositories import StatusRepository
from prp.schemas import (CustomerRelationshipStatusValidFromToDate, Status)
from prp.utils import format_error_response

class StatusService:
    def __init__(self):
        self.customer_relationship_status_valid_from_to_date_schema = CustomerRelationshipStatusValidFromToDate()
        self.status_schema = Status()
        self.status_repository = StatusRepository()
        
    def format_status(self, status, status_valid_from_to_date):
        formatted_status = {
            'CustomerRelationshipStatusType': status['CustomerRelationshipStatusType'],
            'CustomerRelationshipStatusNarrative': status['CustomerRelationshipStatusNarrative'],
            'CustomerRelationshipStatusValidFromToDate': {
                'DateContent': status_valid_from_to_date['DateContent']
            },
        }
        return formatted_status
        
    def format_status2(status):
        formatted_status = {
            'CustomerRelationshipStatusType': status['CustomerRelationshipStatusType'],
            'CustomerRelationshipStatusNarrative': status['CustomerRelationshipStatusNarrative'],
            'CustomerRelationshipStatusValidFromToDate': {
                'DateContent': status['DateContent']
            },
            'PartyStateId': status['PartyStateId']
        }
        return formatted_status
        
    def initiate_status_monitoring(self, party_state_id):
        verify_status = self.status_repository.selectStatusByPartyStateIdAll(party_state_id)
        if verify_status:
            return format_error_response(message=f"Status for party state {party_state_id} already monitored"), 400
        status_valid_from_to_date = self.status_repository.insertStatusValidFromToDate()
        status = self.status_repository.insertStatus({
            'CustomerRelationshipStatusValidFromToDateId': status_valid_from_to_date.get('CustomerRelationshipStatusValidFromToDateId'),
            'PartyStateId': party_state_id
        })
        return status
    
    def update_status(self, body, party_state_id, status_id):
        errors = self.status_schema.validate(body)
        if errors:
            return format_error_response(message=errors), 400
        verify_status = self.status_repository.selectStatusByPartyStateIdAndId(party_state_id, status_id)
        if not verify_status:
            return format_error_response(message=f"Status Monitoring with id {status_id} not found"), 404
        
        customer_relationship_status_valid_from_to_date = verify_status['CustomerRelationshipStatusValidFromToDateId']
        
        verify_status_valid_from_to_date = self.status_repository.selectStatusValidFromToDateById(customer_relationship_status_valid_from_to_date)
        if not verify_status_valid_from_to_date:
            return format_error_response(message=f"Status Valid From to Date register with id {customer_relationship_status_valid_from_to_date} not found"), 404
        
        status_valid_from_to_date_id = verify_status_valid_from_to_date['CustomerRelationshipStatusValidFromToDateId']
        
        # Modify status valid from to date first
        status_valid_from_to_date = self.status_repository.updateStatusValidFromToDate(status_valid_from_to_date_id, body.get('CustomerRelationshipStatusValidFromToDate'))
        # Modify status
        status = self.status_repository.updateStatus(status_id, body)
        
        status_response = self.format_status(status, status_valid_from_to_date)
        
        return {'Status': self.status_schema.dump(status_response)}, 200
        
        
    
    def retrieve_status(self, party_state_id, status_id):
        verify_status = self.status_repository.selectStatusByPartyStateIdAndId(party_state_id, status_id)
        if not verify_status:
            return format_error_response(message=f"Status Monitoring with id {status_id} not found"), 404
        
        customer_relationship_status_valid_from_to_date = verify_status['CustomerRelationshipStatusValidFromToDateId']
        
        verify_status_valid_from_to_date = self.status_repository.selectStatusValidFromToDateById(customer_relationship_status_valid_from_to_date)
        if not verify_status_valid_from_to_date:
            return format_error_response(message=f"Status Valid From to Date register with id {customer_relationship_status_valid_from_to_date} not found")
        
        status_response = self.format_status(verify_status, verify_status_valid_from_to_date)
        
        return {'Status': self.status_schema.dump(status_response)}, 200