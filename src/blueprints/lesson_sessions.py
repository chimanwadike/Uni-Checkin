from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.lesson_session_service import get_students_enrolled_in_lesson_session, register_session_attendance, \
    update_session_attendance
from src.utils.auth_decorators import tutor_required
from src.services.checkin_code_service import generate_check_in_code, get_check_in_code

lesson_sessions = Blueprint("lesson_sessions", __name__, url_prefix="/api/v1/lesson_sessions")


@lesson_sessions.get('/<int:session_id>/students')
@tutor_required()
def students_by_lesson_session(session_id):
    return get_students_enrolled_in_lesson_session(request.args, session_id=session_id)


@lesson_sessions.post('/<int:session_id>/attendance')
@tutor_required()
def register_lesson_session_attendance(session_id):
    return register_session_attendance(request, session_id=session_id)


@lesson_sessions.put('/<int:session_id>/update_attendance')
@tutor_required()
def update_lesson_session_attendance(session_id):
    return update_session_attendance(request, session_id=session_id)


@lesson_sessions.post('/<int:id>/check_in_code')
@tutor_required()
def generate_checkin_code(id):
    return generate_check_in_code(lecture_session_id=id)


@lesson_sessions.get('/<int:id>/view_check_in_code')
@tutor_required()
def get_checkin_code(id):
    return get_check_in_code(lecture_session_id=id)
