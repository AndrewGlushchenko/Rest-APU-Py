from marshmallow import Schema, validate, fields

class ElementSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    ip_address = fields.String(required=True, validate=[validate.Length(max=15)])
    name = fields.String(required=True, validate=[validate.Length(max=80)])
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    name = fields.String(required=True, validate=[validate.Length(max=80)])
    email = fields.String(required=True, validate=[validate.Length(max=40)])
    password = fields.String(required=True, validate=[validate.Length(max=100)], load_only=True)
    elements = fields.Nested(ElementSchema, many=True, dump_only=True)

class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
