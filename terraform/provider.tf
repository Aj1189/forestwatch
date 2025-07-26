provider "aws" {
  region     = var.aws_region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "20216777-terraform-bucket"
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}
