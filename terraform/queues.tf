resource "aws_sqs_queue" "audit_queue" {
  name = "${var.student_id}-audit-queue"
}

resource "aws_lambda_event_source_mapping" "sqs_to_lambda" {
  event_source_arn = aws_sqs_queue.audit_queue.arn
  function_name    = aws_lambda_function.audit_logger.function_name
  batch_size       = 1
  enabled          = true
}
