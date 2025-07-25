data "aws_iam_policy_document" "ecs_task_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.student_id}-ecs-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

# ECS Execution Role
resource "aws_iam_role" "ecs_execution" {
  name = "${var.student_id}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach default execution role policy
resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Additional: Allow ECR GetAuthorizationToken for image pulls
resource "aws_iam_role_policy_attachment" "ecs_execution_ecr_access" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.student_id}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name = "${var.student_id}-lambda-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["rekognition:*"],
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl"
        ],
        Resource = aws_sqs_queue.audit_queue.arn
      },
      {
        Effect   = "Allow",
        Action   = ["sns:Publish"],
        Resource = aws_sns_topic.alert_topic.arn
      },
      {
        Effect   = "Allow",
        Action   = ["dynamodb:PutItem"],
        Resource = aws_dynamodb_table.audit_logs.arn
      },
      {
        Effect   = "Allow",
        Action   = ["s3:*"],
        Resource = "${aws_s3_bucket.complaint_images.arn}/*"
      },
      {
        Effect   = "Allow",
        Action   = ["dynamodb:PutItem"],
        Resource = "arn:aws:dynamodb:*:*:table/ImageModerationLogs"
      },
      {
        Effect   = "Allow",
        Action   = ["logs:*"],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
