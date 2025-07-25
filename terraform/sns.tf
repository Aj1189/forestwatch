resource "aws_sns_topic" "alert_topic" {
  name = "${var.student_id}-moderation-alerts"
}

resource "aws_sns_topic_subscription" "forest_email" {
  topic_arn = aws_sns_topic.alert_topic.arn
  protocol  = "email"
  endpoint  = var.forest_department_email
}
