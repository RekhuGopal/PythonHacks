# terraform.tf
terraform {
  required_providers {
    oci = {
      source  = "hashicorp/oci"
      version = ">= 5.0.0"
    }
  }
}
