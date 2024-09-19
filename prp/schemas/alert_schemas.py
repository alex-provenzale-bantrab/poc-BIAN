from marshmallow import Schema, fields
from . import PartyState

class CustomerRelationshipAlertValidFromToDate(Schema):
    DateContent = fields.Str(required=True)

class Alert(Schema):
    CustomerRelationshipAlertType = fields.Str(required=True)
    CustomerRelationshipAlertNarrative = fields.Str(required=True)
    CustomerRelationshipAlertValidFromToDate = fields.Nested(CustomerRelationshipAlertValidFromToDate, required=True)
    PartyStateId = fields.Nested(PartyState, load_only=True)
