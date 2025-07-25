resource "aws_ecs_cluster" "main" {
  name = "${var.student_id}-ecs-cluster"
}
