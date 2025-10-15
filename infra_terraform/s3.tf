resource "aws_s3_bucket" "example" {
  bucket = "data-landing-etl"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

