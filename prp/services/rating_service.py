from prp.repositories import RatingRepository
from prp.schemas import (CustomerRelationshipRatingValidFromToDate, Rating)
from prp.utils import format_error_response

class RatingService:
    def __init__(self):
        self.customer_relationship_rating_valid_from_to_date_schema = CustomerRelationshipRatingValidFromToDate()
        self.rating_schema = Rating()
        self.rating_repository = RatingRepository()
        
    def format_rating(self, rating, rating_valid_from_to_date):
        formatted_rating = {
            'CustomerRelationshipRatingType': rating['CustomerRelationshipRatingType'],
            'CustomerRelationshipRatingNarrative': rating['CustomerRelationshipRatingNarrative'],
            'CustomerRelationshipRatingValidFromToDate': {
                'DateContent': rating_valid_from_to_date['DateContent']
            },
        }
        return formatted_rating
        
    def format_rating2(rating):
        formatted_rating = {
            'CustomerRelationshipRatingType': rating['CustomerRelationshipRatingType'],
            'CustomerRelationshipRatingNarrative': rating['CustomerRelationshipRatingNarrative'],
            'CustomerRelationshipRatingValidFromToDate': {
                'DateContent': rating['DateContent']
            },
            'PartyStateId': rating['PartyStateId']
        }
        return formatted_rating
        
    def initiate_rating_monitoring(self, party_state_id):
        verify_rating = self.rating_repository.selectRatingByPartyStateIdAll(party_state_id)
        if verify_rating:
            return format_error_response(message=f"Rating for party state {party_state_id} already monitored"), 400
        rating_valid_from_to_date = self.rating_repository.insertRatingValidFromToDate()
        rating = self.rating_repository.insertRating({
            'CustomerRelationshipRatingValidFromToDateId': rating_valid_from_to_date.get('CustomerRelationshipRatingValidFromToDateId'),
            'PartyStateId': party_state_id
        })
        return rating
    
    def update_rating(self, body, party_state_id, rating_id):
        errors = self.rating_schema.validate(body)
        if errors:
            return format_error_response(message=errors), 400
        verify_rating = self.rating_repository.selectRatingByPartyStateIdAndId(party_state_id, rating_id)
        if not verify_rating:
            return format_error_response(message=f"Rating Monitoring with id {rating_id} not found"), 404
        
        customer_relationship_rating_valid_from_to_date = verify_rating['CustomerRelationshipRatingValidFromToDateId']
        
        verify_rating_valid_from_to_date = self.rating_repository.selectRatingValidFromToDateById(customer_relationship_rating_valid_from_to_date)
        if not verify_rating_valid_from_to_date:
            return format_error_response(message=f"Rating Valid From to Date register with id {customer_relationship_rating_valid_from_to_date} not found"), 404
        
        rating_valid_from_to_date_id = verify_rating_valid_from_to_date['CustomerRelationshipRatingValidFromToDateId']
        
        # Modify rating valid from to date first
        rating_valid_from_to_date = self.rating_repository.updateRatingValidFromToDate(rating_valid_from_to_date_id, body.get('CustomerRelationshipRatingValidFromToDate'))
        # Modify rating
        rating = self.rating_repository.updateRating(rating_id, body)
        
        rating_response = self.format_rating(rating, rating_valid_from_to_date)
        
        return {'Rating': self.rating_schema.dump(rating_response)}, 200
        
        
    
    def retrieve_rating(self, party_state_id, rating_id):
        verify_rating = self.rating_repository.selectRatingByPartyStateIdAndId(party_state_id, rating_id)
        if not verify_rating:
            return format_error_response(message=f"Rating Monitoring with id {rating_id} not found"), 404
        
        customer_relationship_rating_valid_from_to_date = verify_rating['CustomerRelationshipRatingValidFromToDateId']
        
        verify_rating_valid_from_to_date = self.rating_repository.selectRatingValidFromToDateById(customer_relationship_rating_valid_from_to_date)
        if not verify_rating_valid_from_to_date:
            return format_error_response(message=f"Rating Valid From to Date register with id {customer_relationship_rating_valid_from_to_date} not found")
        
        rating_response = self.format_rating(verify_rating, verify_rating_valid_from_to_date)
        
        return {'Rating': self.rating_schema.dump(rating_response)}, 200