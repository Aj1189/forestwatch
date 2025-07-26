from models import db, Complaint

def mark_complaint_as_rejected(complaint_id, reason):
    complaint = Complaint.query.get(complaint_id)
    if complaint:
        complaint.status = "Rejected"
        complaint.rejection_reason = reason
        complaint.image_url = "https://20216777-complaints-images.s3.us-east-1.amazonaws.com/complaints/restricted_logo.png"
        db.session.commit()
        return "success"
    else:
        return "fail"
