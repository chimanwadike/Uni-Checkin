from datetime import datetime

from flask import jsonify
from sqlalchemy import text, column, desc
from sqlalchemy.orm import load_only

from src.constants.http_status_codes import *
from src.database.database_context import db, Course, LectureSchedule, LectureSession, TutorCourseAssignment, \
    LectureScheduleUserEnrolment
from src.utils.utility_functions import get_current_semester


def get_course_schedules(args):
    page = args.get('page', 1, type=int)

    per_page = args.get('per_page', 5, type=int)

    course_schedules = LectureSchedule.query \
        .filter(LectureSchedule.semester_id == get_current_semester()) \
        .paginate(page=page, per_page=per_page)

    data = [schedule.to_dict() for schedule in course_schedules]

    meta = {
        'page': course_schedules.page,
        'pages': course_schedules.pages,
        'total_count': course_schedules.total,
        'prev_page': course_schedules.prev_num,
        'next_page': course_schedules.next_num,
        'has_next': course_schedules.has_next,
        'has_prev': course_schedules.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_student_course_sessions(args):
    student_id = 1  # TODO:: change hardcoded value
    return None


def get_logged_in_tutor_lesson_sessions(args):
    tutor_id = 1  # TODO:: change hardcoded value to logged user_id

    assigned_course_schedule_ids = db.session.query(LectureScheduleUserEnrolment.lecture_schedule_id) \
        .join(LectureScheduleUserEnrolment.lecture_schedule) \
        .filter(LectureScheduleUserEnrolment.user_id == tutor_id, LectureScheduleUserEnrolment.user_type == 'tutor',
                LectureSchedule.semester_id == get_current_semester())

    lecture_sessions = LectureSession \
        .query.order_by(desc(LectureSession.end_time)) \
        .filter(LectureSession.lecture_schedule_id.in_(assigned_course_schedule_ids),
                LectureSession.end_time <= datetime.now())

    data = [session.to_dict() for session in lecture_sessions]

    return jsonify({'data': data}), HTTP_200_OK


def get_enrolled_course_students(args):
    tutor_id = 1  # TODO:: change hardcoded value
    return None


def get_tutor_lesson_sessions_by_tutor_id(args, tutor_id):
    assigned_course_schedule_ids = db.session.query(LectureScheduleUserEnrolment.lecture_schedule_id) \
        .join(LectureScheduleUserEnrolment.lecture_schedule) \
        .filter(LectureScheduleUserEnrolment.user_id == tutor_id, LectureScheduleUserEnrolment.user_type == 'tutor',
                LectureSchedule.semester_id == get_current_semester())

    lecture_sessions = LectureSession \
        .query.order_by(desc(LectureSession.end_time)) \
        .filter(LectureSession.lecture_schedule_id.in_(assigned_course_schedule_ids),
                LectureSession.end_time <= datetime.now())

    data = [session.to_dict() for session in lecture_sessions]

    return jsonify({'data': data}), HTTP_200_OK