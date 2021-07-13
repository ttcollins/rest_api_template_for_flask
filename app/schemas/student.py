from marshmallow import Schema, fields


class StudentSchema(Schema):

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    fname = fields.String(required=True)
    lname = fields.String(required=True)
    course = fields.String(required=True)
    password = fields.String(load_only=True)