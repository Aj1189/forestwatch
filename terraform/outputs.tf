# Combined ECR Repo
output "combined_ecr_repo_url" {
  value = aws_ecr_repository.combined_repo.repository_url
}

# Combined ECS Service
output "combined_service_name" {
  value = aws_ecs_service.combined.name
}

# ECS Cluster
output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

# S3 Bucket for complaint images
output "s3_bucket_name" {
  value = aws_s3_bucket.complaint_images.bucket
}

# SQS Queue
output "sqs_queue_url" {
  value = aws_sqs_queue.audit_queue.id
}

# SNS Topic
output "sns_topic_arn" {
  value = aws_sns_topic.alert_topic.arn
}

# Dynamo DB
output "dynamodb_table_name" {
  value = aws_dynamodb_table.audit_logs.name
}

# Moderation Lambda
output "lambda_moderation_name" {
  value = aws_lambda_function.image_moderation.function_name
}
