from marshmallow import Schema, validate, fields


class TaskSchema(Schema):
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    text = fields.String(required=True)
    status = fields.Boolean(dump_only=True)
    admin_edit = fields.Boolean(dump_only=True)
    message = fields.String(dump_only=True)


class TaskSchemaUpdate(TaskSchema):
    
    status = fields.Boolean(required=False)
    admin_edit = fields.Boolean(required=False)


class AdminUserSchema(Schema):

    name = fields.String(required=True, validate=[validate.Length(max=250)])
    password = fields.String(required=True, validate=[validate.Length(max=100)], load_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)