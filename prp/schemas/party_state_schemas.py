from marshmallow import Schema, fields

class PartyState(Schema):
    CustomerReference = fields.Str(required=True)
