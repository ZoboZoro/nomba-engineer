terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.21.0"
    }
  }
}

# Configure Providers
provider "aws" {
  profile = "taofeecoh"
  region  = "eu-central-1"
}