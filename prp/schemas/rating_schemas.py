from marshmallow import Schema, fields
from . import PartyState

class CustomerRelationshipRatingValidFromToDate(Schema):
    DateContent = fields.Str(required=True)

class Rating(Schema):
    CustomerRelationshipRatingType = fields.Str(required=True)
    CustomerRelationshipRatingNarrative = fields.Str(required=True)
    CustomerRelationshipRatingValidFromToDate = fields.Nested(CustomerRelationshipRatingValidFromToDate, required=True)
    PartyStateId = fields.Nested(PartyState, load_only=True)
