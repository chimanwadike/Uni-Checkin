import json
from datetime import datetime

from flask import jsonify
from sqlalchemy import extract

from src.constants.http_status_codes import *
from src.database.database_context import db, User

import validators
from werkzeug.security import check_password_hash, generate_password_hash


# get all users
def get_users(self):
    page = self.args.get('page', 1, type=int)

    per_page = self.args.get('per_page', 5, type=int)

    users = User.query.paginate(page=page, per_page=per_page)

    data = []
    for user in users.items:
        data.append({'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name,
                     'phone_number': user.phone_number})

    meta = {
        'page': users.page,
        'pages': users.pages,
        'total_count': users.total,
        'prev_page': users.prev_num,
        'next_page': users.next_num,
        'has_next': users.has_next,
        'has_prev': users.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


# get a single user using the user id
def get_user(self, id):
    # data = self.get_json()
    user = User.query \
        .filter(User.id == id) \
        .first()

    if not user:
        return jsonify({'error_message': 'User does not exist'}), HTTP_404_NOT_FOUND

    return jsonify(
        {'id': user.id,
         'first_name': user.first_name,
         'created_at': user.created_at,
         'status': user.status,
         }
    ), HTTP_200_OK


# edit a user details
def edit_user(self, id):
    data = self.get_json()
    user = User.query \
        .filter(User.id == id) \
        .first()
    if not user:
        return jsonify({'message': 'User does not exist'}), HTTP_404_NOT_FOUND

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.status = data['status']
    user.email = data['email']
    user.phone_number = data['phone_number']

    db.session.commit()

    return jsonify({'message': 'User Recorded Updated succesfully',
                    'user': {'id': user.id,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'status': user.status,
                             'phone_number': user.phone_number,
                             'email': user.email
                             }

                    }), HTTP_200_OK


def delete_user(self, id):
    user = User.query \
        .filter(User.id == id) \
        .first()
    if not user:
        return jsonify({'message': 'User does not exist'}), HTTP_400_BAD_REQUEST
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted succesfully'}), HTTP_204_NO_CONTENT
