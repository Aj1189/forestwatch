resource "aws_s3_bucket" "complaint_images" {
  bucket        = "${var.student_id}-complaints-images"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket                  = aws_s3_bucket.complaint_images.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_notification" "image_upload_trigger" {
  bucket = aws_s3_bucket.complaint_images.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.image_moderation.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "complaints/"
  }

  depends_on = [aws_lambda_permission.allow_s3_trigger]
}
