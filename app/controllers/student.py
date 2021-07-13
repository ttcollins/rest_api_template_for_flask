import json
from flask_restful import Resource, request

from app.schemas import StudentSchema
from app.models.student import Student
from flask_bcrypt import Bcrypt


class StudentView(Resource):

    def post(self):
        """
        Creating a Student Account
        """
        student_schema = StudentSchema()

        student_data = request.get_json()

        # .load validates and returns json data
        validated_student_data, errors = student_schema.load(student_data)

        if errors:
            return dict(status='fail', message=errors), 400

        existing_student = Student.find_first(email=validated_student_data["email"])

        if existing_student:
            return dict(status='fail',
                        message=f'Student email {validated_student_data["email"]} already exists'), 409

        student = Student(**validated_student_data)

        saved_student = student.save()

        if not saved_student:
            return dict(status='fail', message='Internal Server Error'), 500

        new_student_data, errors = student_schema.dumps(student)

        return dict(status='success', data=dict(user=json.loads(new_student_data))), 201

    # @jwt_required
    def get(self):
        """
        Getting All students
        """
        student_schema = StudentSchema(many=True)

        students = Student.find_all()

        # dump returns json data
        students_data, errors = student_schema.dumps(students)

        if errors:
            return dict(status="fail", message="Internal Server Error"), 500

        return dict(status="success", data=dict(users=json.loads(students_data))), 200
    

class StudentDetailView(Resource):

    def get(self, student_id):
        """
        Getting individual student
        """
        schema = StudentSchema()

        student = Student.get_by_id(student_id)

        if not student:
            return dict(status="fail", message=f"Student with id {student_id} not found"), 404

        student_data, errors = schema.dumps(student)

        if errors:
            return dict(status="fail", message=errors), 500

        return dict(status='success', data=dict(user=json.loads(student_data))), 200

    # @jwt_required
    def patch(self, student_id):
        """
        Update a single student
        """

        # To do check if student is admin
        schema = StudentSchema(partial=True)

        update_data = request.get_json()

        validated_update_data, errors = schema.load(update_data)

        if errors:
            return dict(status="fail", message=errors), 400

        student = Student.get_by_id(student_id)

        if not student:
            return dict(status="fail", message=f"User with id {student_id} not found"), 404

        updated_student = Student.update(student, **validated_update_data)

        if not updated_student:
            return dict(status='fail', message='Internal Server Error'), 500

        return dict(status="success", message="Student updated successfully"), 200
    
    
    def delete(self, student_id):
        """
        Delete a single student
        """

        student = Student.get_by_id(student_id)

        if not student:
            return dict(status="fail", message=f"User with id {student_id} not found"), 404

        deleted_student = student.delete()

        if not deleted_student:
            return dict(status='fail', message='Internal Server Error'), 500

        return dict(status='success', message="Successfully deleted"), 200