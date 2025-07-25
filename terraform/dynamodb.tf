resource "aws_dynamodb_table" "audit_logs" {
  name         = "${var.student_id}-audit-logs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = "ForestWatch"
  }
}
