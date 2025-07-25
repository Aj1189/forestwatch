from flask import Blueprint, jsonify
from utils.auth_helper import token_required
from models import Complaint, db
from sqlalchemy.orm import joinedload
from report_analyzer.analyzer import ReportAnalyzer

report_bp = Blueprint("report_bp", __name__)

@report_bp.route("/reports", methods=["GET"])
@token_required
def generate_report(current_user):

    if current_user.role != 'forest_dept':
        return jsonify({'message': 'Permission denied'}), 403

    complaints = Complaint.query.options(joinedload(Complaint.user)).all()

    analyzer = ReportAnalyzer()
    analyzer.load_complaints(complaints)

    return jsonify({
        "by_category": [{"type": t, "count": c} for t, c in analyzer.count_by_category()],
        "by_region": [{"region": r, "count": c} for r, c in analyzer.count_by_region()],
        "by_month": [{"month": m, "count": c} for m, c in analyzer.count_by_month()],
        "hot_zones": [{"region": r, "count": c} for r, c in analyzer.frequent_regions(threshold=3)]
    }), 200
