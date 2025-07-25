# variables.tf

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "aws_region" {
  default = "us-east-1"
}

variable "student_id" {
  default = "20216777"
}

variable "forest_department_email" {
  description = "Email address to notify for moderation alerts"
  type        = string
  default     = "forest-dept@test.com"
}

variable "s3_access_key" {
  description = "S3 Access Key (injected via GitHub Actions)"
  type        = string
}

variable "AWS_ACCESS_KEY" {
  description = "Access key from GitHub Secrets"
  type        = string
}

variable "AWS_SECRET_KEY" {
  description = "Secret key from GitHub Secrets"
  type        = string
}

variable "rds_password" {
  description = "Database Password from GitHub Secrets"
  type        = string
}

variable "rds_username" {
  description = "Database Password from GitHub Secrets"
  type        = string
}
