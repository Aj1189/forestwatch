import uuid
from flask import Blueprint, request, jsonify
from models import db, Complaint, User
from utils.auth_helper import token_required
from utils.image_helper import upload_to_s3, delete_from_s3
from datetime import datetime

complaint_bp = Blueprint('complaints', __name__)

# Create new complaint (Citizen)
@complaint_bp.route('/complaints', methods=['POST'])
@token_required
def create_complaint(current_user):
    if current_user.role != 'citizen':
        return jsonify({'message': 'Only citizens can file complaints'}), 403

    if 'image' not in request.files:
        return jsonify({'message': 'Image is required'}), 400

    image = request.files['image']
    description = request.form.get('description')
    category = request.form.get('category')
    location = request.form.get('location')
    complaint_id = uuid.uuid4()

    if not all([description, category, location]):
        return jsonify({'message': 'All fields are required'}), 400

    image_url = upload_to_s3(image)

    complaint = Complaint(
        user_id=current_user.id,
        complaint_id=complaint_id,
        description=description,
        category=category,
        location=location,
        image_url=image_url,
        created_at=datetime.utcnow()
    )
    db.session.add(complaint)
    db.session.commit()

    return jsonify({'message': 'Complaint submitted successfully'}), 201

# View complaints (Forest Dept)
@complaint_bp.route('/complaints', methods=['GET'])
@token_required
def get_all_complaints(current_user):
    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    results = []
    for c in complaints:
        results.append({
            'id': c.id,
            'user': c.user.name,
            'description': c.description,
            'category': c.category,
            'location': c.location,
            'image_url': c.image_url,
            'status': c.status,
            'rejection_reason': c.rejection_reason,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return jsonify(results), 200

# View citizen's own complaints
@complaint_bp.route('/complaints/user', methods=['GET'])
@token_required
def get_user_complaints(current_user):
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    results = []
    for c in complaints:
        results.append({
            'id': c.id,
            'description': c.description,
            'category': c.category,
            'location': c.location,
            'image_url': c.image_url,
            'status': c.status,
            'rejection_reason': c.rejection_reason,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return jsonify(results), 200

# Update complaint status (Forest Dept)
@complaint_bp.route('/complaints/<int:complaint_id>/status', methods=['PUT'])
@token_required
def update_complaint_status(current_user, complaint_id):
    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    new_status = data.get('status')
    if not new_status:
        return jsonify({'message': 'Status field is required'}), 400

    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify({'message': 'Complaint not found'}), 404

    complaint.status = new_status
    db.session.commit()

    return jsonify({'message': 'Complaint status updated'}), 200

# Withdraw complaint (Soft Delete)
@complaint_bp.route('/complaints/<int:complaint_id>', methods=['DELETE'])
@token_required
def withdraw_complaint(current_user, complaint_id):
    complaint = Complaint.query.get(complaint_id)

    if not complaint:
        return jsonify({'message': 'Complaint not found'}), 404

    # Only the owner or forest_dept can withdraw
    if current_user.role != 'forest_dept' and complaint.user_id != current_user.id:
        return jsonify({'message': 'Permission denied'}), 403

    # Mark status instead of deleting
    complaint.status = 'Withdrawn'
    db.session.commit()

    return jsonify({'message': 'Complaint withdrawn (soft deleted) successfully'}), 200
