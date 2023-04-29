provider "google" {
   credentials = "${file("./creds/serviceaccount.json")}"
   project     = "cloudquicklabs" # REPLACE WITH YOUR PROJECT ID
   region      = "US"
 }