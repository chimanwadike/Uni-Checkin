from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_code = db.Column(db.String(10))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    status = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    lecture_sessions_attended = db.relationship('LectureSessionAttendance', back_populates='user')

    def __repr__(self) -> str:
        return 'User>>> {self.id}'

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.first_name + ' ' + self.last_name,
            'code': self.user_code,
            'email': self.email
        }


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')

    def __repr__(self) -> str:
        return 'Role>>> {self.id}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime)
    lecture_schedules = db.relationship('LectureSchedule', back_populates='semester')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    def __repr__(self) -> str:
        return 'Semester>>> {self.id}'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    building = db.Column(db.String(45))
    lecture_schedules = db.relationship('LectureSchedule', back_populates='venues')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'building': self.building
        }

    def __repr__(self) -> str:
        return 'Venue>>> {self.id}'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now())
    lecture_schedules = db.relationship('LectureSchedule', back_populates='course')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self) -> str:
        return 'Course>>> {self.id}'


class LectureSchedule(db.Model):
    __tablename__ = 'lecture_schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    day = db.Column(db.String(10))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    one_off_date = db.Column(db.DateTime)
    is_recurring = db.Column(db.Boolean)
    is_online = db.Column(db.Boolean, nullable=False, default=False)

    course = db.relationship('Course', back_populates='lecture_schedules')
    semester = db.relationship('Semester', back_populates='lecture_schedules')
    venues = db.relationship('Venue', back_populates='lecture_schedules')
    lecture_sessions = db.relationship('LectureSession', back_populates='lecture_schedule')

    def to_dict(self):
        return {
            'id': self.id,
            'course': self.course.to_dict(),
            'venue': self.venues.to_dict(),
            'semester': self.semester.to_dict(),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'day': self.day,
            'is_recurring': self.is_recurring,
            'is_online': self.is_online
        }

    def __repr__(self) -> str:
        return 'LectureSchedule>>> {self.id}'


class LectureSession(db.Model):
    __tablename__ = 'lecture_sessions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lecture_schedule_id = db.Column(db.Integer, db.ForeignKey('lecture_schedules.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    allow_self_registration = db.Column(db.Boolean, default=True)
    check_in_code = db.Column(db.String(10))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime)

    lecture_schedule = db.relationship('LectureSchedule', back_populates='lecture_sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'course': self.lecture_schedule.course.to_dict(),
            'venue': self.lecture_schedule.venues.to_dict(),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'check_in_code': self.check_in_code,
            'day': self.lecture_schedule.day
        }

    def __repr__(self) -> str:
        return 'LectureSession>>> {self.id}'


class LectureSessionAttendance(db.Model):
    __tablename__ = 'lecture_session_attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lecture_session_id = db.Column(db.Integer, db.ForeignKey('lecture_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_status_code = db.Column(db.String(5))
    user = db.relationship('User', back_populates='lecture_sessions_attended')
    lecture_session = db.relationship('LectureSession')

    def to_dict(self):
        return {
            'id': self.id,
            'lecture_session_id': self.lecture_session_id,
            'status': self.attendance_status_code,
            'user_id': self.user_id,
            'course_info': self.lecture_session.to_dict()["course"]
        }


class LectureScheduleUserEnrolment(db.Model):
    __tablename__ = 'lecture_schedule_user_enrolment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lecture_schedule_id = db.Column(db.Integer, db.ForeignKey('lecture_schedules.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_type = db.Column(db.String(10), default='student')

    lecture_schedule = db.relationship('LectureSchedule')
    user = db.relationship('User')


class StudentCourseEnrolment(db.Model):
    __tablename__ = 'student_course_enrolment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))


class TutorCourseAssignment(db.Model):
    __tablename__ = 'tutor_course_assignment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
