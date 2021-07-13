from flask_restful import Api
from app.controllers import IndexView, StudentView, StudentDetailView

api = Api()

# Index route
api.add_resource(IndexView, '/')
api.add_resource(StudentView, '/student')
api.add_resource(StudentDetailView, '/student/<string:student_id>')