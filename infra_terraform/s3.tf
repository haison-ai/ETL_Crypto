# Create an S3 bucket for the data landing zone
resource "aws_s3_bucket" "data_landing_zone" {
  bucket        = "data-landing-etl"
  force_destroy = true

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "data_staging_zone" {
  bucket        = "data-staging-etl"
  force_destroy = true

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}




# Create an S3 bucket for the data curated zone
resource "aws_s3_bucket" "data_curated_zone" {
  bucket        = "data-curated-etl"
  force_destroy = true

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}


