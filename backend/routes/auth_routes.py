from flask import Blueprint, request, jsonify
from models import db, User
from utils.auth_helper import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(
        name=data.get('name'),
        email=data['email'],
        phone=data.get('phone'),
        region=data.get('region'),
        role='citizen'
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id, user.role)
        return jsonify({
            'message': 'Login successful',
            'role': user.role,
            'token': token
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
