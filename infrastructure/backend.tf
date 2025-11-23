terraform {
  backend "s3" {
    bucket       = "all-terraform-backends"
    key          = "nomba-project/prod/tf.state"
    region       = "eu-central-1"
    use_lockfile = true
  }
}