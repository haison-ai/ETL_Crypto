resource "aws_glue_crawler" "crypto_crawler" {
  database_name = aws_glue_catalog_database.crypto_db.name
  name          = "crypto-discovery-crawler"
  role          = aws_iam_role.glue_service_role.arn

  s3_target {
    path = "s3://data-landing-etl/"
  }

  configuration = jsonencode({
    Version = 1.0
    Grouping = {
      TableGroupingPolicy = "CombineCompatibleSchemas"
    }
  })
}
