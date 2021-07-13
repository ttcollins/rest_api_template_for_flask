from sqlalchemy.orm import relationship, backref
from ..models import db
from app.models.root_model import RootModel


class Student(RootModel):
    """ user table definition """

    _tablename_ = "students"

    # fields of the user table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    fname = db.Column(db.String(256), nullable=False, default="")
    lname = db.Column(db.String(256), nullable=False, default="")
    course = db.Column(db.String(256), nullable=False, default="")
    password = db.Column(db.String(256), nullable=False, default="")

