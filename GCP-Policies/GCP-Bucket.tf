/*
resource "google_storage_bucket" "restricted_bucket" {
  name          = "${var.Policies.policy1target}-restricted-bucket"
  location      = "us-east1"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
*/