from prp.repositories import AlertRepository
from prp.schemas import (CustomerRelationshipAlertValidFromToDate, Alert)
from prp.utils import format_error_response

class AlertService:
    def __init__(self):
        self.customer_relationship_alert_valid_from_to_date_schema = CustomerRelationshipAlertValidFromToDate()
        self.alert_schema = Alert()
        self.alert_repository = AlertRepository()
        
    def format_alert(self, alert, alert_valid_from_to_date):
        formatted_alert = {
            'CustomerRelationshipAlertType': alert['CustomerRelationshipAlertType'],
            'CustomerRelationshipAlertNarrative': alert['CustomerRelationshipAlertNarrative'],
            'CustomerRelationshipAlertValidFromToDate': {
                'DateContent': alert_valid_from_to_date['DateContent']
            },
        }
        return formatted_alert
        
    def format_alert2(alert):
        formatted_alert = {
            'CustomerRelationshipAlertType': alert['CustomerRelationshipAlertType'],
            'CustomerRelationshipAlertNarrative': alert['CustomerRelationshipAlertNarrative'],
            'CustomerRelationshipAlertValidFromToDate': {
                'DateContent': alert['DateContent']
            },
            'PartyStateId': alert['PartyStateId']
        }
        return formatted_alert
        
    def initiate_alert_monitoring(self, party_state_id):
        verify_alert = self.alert_repository.selectAlertByPartyStateIdAll(party_state_id)
        if verify_alert:
            return format_error_response(message=f"Alert for party state {party_state_id} already monitored"), 400
        alert_valid_from_to_date = self.alert_repository.insertAlertValidFromToDate()
        alert = self.alert_repository.insertAlert({
            'CustomerRelationshipAlertValidFromToDateId': alert_valid_from_to_date.get('CustomerRelationshipAlertValidFromToDateId'),
            'PartyStateId': party_state_id
        })
        return alert
    
    def update_alert(self, body, party_state_id, alert_id):
        errors = self.alert_schema.validate(body)
        if errors:
            return format_error_response(message=errors), 400
        verify_alert = self.alert_repository.selectAlertByPartyStateIdAndId(party_state_id, alert_id)
        if not verify_alert:
            return format_error_response(message=f"Alert Monitoring with id {alert_id} not found"), 404
        
        customer_relationship_alert_valid_from_to_date = verify_alert['CustomerRelationshipAlertValidFromToDateId']
        
        verify_alert_valid_from_to_date = self.alert_repository.selectAlertValidFromToDateById(customer_relationship_alert_valid_from_to_date)
        if not verify_alert_valid_from_to_date:
            return format_error_response(message=f"Alert Valid From to Date register with id {customer_relationship_alert_valid_from_to_date} not found"), 404
        
        alert_valid_from_to_date_id = verify_alert_valid_from_to_date['CustomerRelationshipAlertValidFromToDateId']
        
        # Modify alert valid from to date first
        alert_valid_from_to_date = self.alert_repository.updateAlertValidFromToDate(alert_valid_from_to_date_id, body.get('CustomerRelationshipAlertValidFromToDate'))
        # Modify alert
        alert = self.alert_repository.updateAlert(alert_id, body)
        
        alert_response = self.format_alert(alert, alert_valid_from_to_date)
        
        return {'Alert': self.alert_schema.dump(alert_response)}, 200
        
        
    
    def retrieve_alert(self, party_state_id, alert_id):
        verify_alert = self.alert_repository.selectAlertByPartyStateIdAndId(party_state_id, alert_id)
        if not verify_alert:
            return format_error_response(message=f"Alert Monitoring with id {alert_id} not found"), 404
        
        customer_relationship_alert_valid_from_to_date = verify_alert['CustomerRelationshipAlertValidFromToDateId']
        
        verify_alert_valid_from_to_date = self.alert_repository.selectAlertValidFromToDateById(customer_relationship_alert_valid_from_to_date)
        if not verify_alert_valid_from_to_date:
            return format_error_response(message=f"Alert Valid From to Date register with id {customer_relationship_alert_valid_from_to_date} not found")
        
        alert_response = self.format_alert(verify_alert, verify_alert_valid_from_to_date)
        
        return {'Alert': self.alert_schema.dump(alert_response)}, 200