resource "aws_lambda_function" "image_moderation" {
  function_name = "${var.student_id}-image-moderation"
  handler       = "moderation.lambda_handler"
  runtime       = "python3.12"
  timeout       = 10
  memory_size   = 128
  filename      = "lambda/moderation.zip"

  role = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      SNS_TOPIC_ARN     = aws_sns_topic.alert_topic.arn
      SQS_QUEUE_URL     = aws_sqs_queue.audit_queue.id
      REJECTION_API_URL = "http://${aws_lb.combined_alb.dns_name}/complaint/moderation-callback"
    }
  }
}

resource "aws_lambda_function" "audit_logger" {
  function_name = "${var.student_id}-audit-logger"
  handler       = "logger.lambda_handler"
  runtime       = "python3.12"
  timeout       = 5
  memory_size   = 128
  filename      = "lambda/logger.zip"
  role          = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      AUDIT_TABLE = aws_dynamodb_table.audit_logs.name
    }
  }
}

resource "aws_lambda_permission" "allow_s3_trigger" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_moderation.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.complaint_images.arn
}