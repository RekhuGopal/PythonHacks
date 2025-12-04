provider "google" {
    project =  var.General.TFBackend.project_id
    region = var.General.TFBackend.region
}

provider "google-beta" {
    project =  var.General.TFBackend.project_id
}