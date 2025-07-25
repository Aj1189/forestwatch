from flask import Blueprint, request, jsonify
from models import db, Project
from utils.auth_helper import token_required

project_bp = Blueprint('project', __name__)

# Get all projects
@project_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    result = []
    for proj in projects:
        result.append({
            'id': proj.id,
            'name': proj.name,
            'region': proj.region,
            'status': proj.status,
            'start_date': proj.start_date.strftime('%Y-%m-%d'),
            'trees_target': proj.trees_target,
            'trees_planted': proj.trees_planted
        })
    return jsonify(result), 200

# Get project by ID
@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    proj = Project.query.get_or_404(project_id)
    return jsonify({
        'id': proj.id,
        'name': proj.name,
        'region': proj.region,
        'status': proj.status,
        'start_date': proj.start_date.strftime('%Y-%m-%d'),
        'trees_target': proj.trees_target,
        'trees_planted': proj.trees_planted
    }), 200

# Create project (Forest Dept only)
@project_bp.route('/projects', methods=['POST'])
@token_required
def create_project(current_user):
    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    new_proj = Project(
        name=data['name'],
        region=data['region'],
        status=data['status'],
        start_date=data['start_date'],
        trees_target=data['trees_target'],
        trees_planted=data['trees_planted']
    )
    db.session.add(new_proj)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

# Update project
@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
@token_required
def update_project(current_user, project_id):
    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    proj = Project.query.get_or_404(project_id)
    data = request.get_json()

    proj.name = data['name']
    proj.region = data['region']
    proj.status = data['status']
    proj.start_date = data['start_date']
    proj.trees_target = data['trees_target']
    proj.trees_planted = data['trees_planted']

    db.session.commit()
    return jsonify({'message': 'Project updated successfully'}), 200

# Delete project
@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@token_required
def delete_project(current_user, project_id):
    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    proj = Project.query.get_or_404(project_id)
    db.session.delete(proj)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200
