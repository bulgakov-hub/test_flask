from marshmallow import Schema, validate, fields


class TaskSchema(Schema):
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=250))
    email = fields.Email(required=True)
    text = fields.String(required=True, validate=validate.Length(max=250))
    # status = fields.Boolean(required=True)
    # admin_edit = fields.Boolean(required=True)


class AdminUserSchema(Schema):

    name = fields.String(required=True, validate=[validate.Length(max=250)])
    password = fields.String(required=True, validate=[validate.Length(max=100)], load_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)