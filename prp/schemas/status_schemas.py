from marshmallow import Schema, fields
from . import PartyState

class CustomerRelationshipStatusValidFromToDate(Schema):
    DateContent = fields.Str(required=True)

class Status(Schema):
    CustomerRelationshipStatusType = fields.Str(required=True)
    CustomerRelationshipStatusNarrative = fields.Str(required=True)
    CustomerRelationshipStatusValidFromToDate = fields.Nested(CustomerRelationshipStatusValidFromToDate, required=True)
    PartyStateId = fields.Nested(PartyState, load_only=True)