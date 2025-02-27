terraform {
  # backend "gcs" {
  #   bucket = "b3912f2a-3d89-46fb-806a-f4510a61ad30-tf-remote-backend"
  # }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.23.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}


