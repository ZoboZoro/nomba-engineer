locals {
  Project_Name = "nombaa_project"
  Managed_by   = "terraform"
  Environment  = "production"
}

locals {
  common_tags = {
    Project_Name = "nombaa_project"
    Managed_by   = "terrfaorm"
    Owner        = "nomba"
    Github       = "github.com/zobozoro"
    Environment  = "production"
    Region       = "eu-central-1"
  }
}
