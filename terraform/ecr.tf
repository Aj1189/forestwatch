resource "aws_ecr_repository" "combined_repo" {
  name = "${var.student_id}-combined"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {
    Name = "Combined Frontend + Backend Repo"
  }
}
