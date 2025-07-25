import jwt
from flask import request, jsonify, current_app
from functools import wraps
from models import User

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
