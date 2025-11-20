resource "aws_iam_user" "snowflake_user" {
  name          = "snowflake_user"
  force_destroy = true
  path          = "/prod/"

  tags = merge(local.common_tags, { Name = "snowflake_user" })
}

resource "aws_iam_access_key" "snowflake" {
  user = aws_iam_user.snowflake_user.name
}

resource "aws_ssm_parameter" "snowflake_user_secret" {
  name        = "/nomba-project/production/snowflake/access_key_secret"
  description = "Credentials for snowflake user"
  type        = "SecureString"
  value       = aws_iam_access_key.snowflake.secret

  tags = local.common_tags
}

resource "aws_ssm_parameter" "snowflake_user_key_id" {
  name        = "/nomba-project/production/snowflake/access_key_id"
  description = "Credentials for snowflake user"
  type        = "String"
  value       = aws_iam_access_key.snowflake.id

  tags = local.common_tags
}


resource "aws_iam_policy" "snowflake_s3_access_policy" {
  name        = "snowflake_s3_access_policy"
  description = "Policy to allow Snowflake read from a specific S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListAllMyBuckets"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:GetBucketLocation",
          "s3:GetObjectVersion"
        ]
        Resource = [
          "arn:aws:s3:::nomba-dumpss",
          "arn:aws:s3:::nomba-dumpss/*"
        ]
      },
    ]
  })
}

resource "aws_iam_user_policy_attachment" "snowflake_attachment" {
  user       = aws_iam_user.snowflake_user.name
  policy_arn = aws_iam_policy.snowflake_s3_access_policy.arn
}