resource "aws_s3_bucket" "nomba-dumps" {
  bucket        = "nomba-dumpss"
  force_destroy = true

  tags = merge({ Name = "nomba-dumpss" }, local.common_tags)
}

resource "aws_s3_bucket_versioning" "nomba_versioning" {
  bucket = aws_s3_bucket.nomba-dumps.id
  versioning_configuration {
    status = "Enabled"
  }
}