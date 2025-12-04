/*
resource "google_org_policy_policy" "restrictregions" {
  name   = "projects/${var.Policies.policy1target}/policies/gcp.resourceLocations"
  parent = "projects/${var.Policies.policy1target}"

  spec {
    rules {
      values {
        allowed_values = ["us-east1", "us-east4"]
      }
    }
  }
}
*/