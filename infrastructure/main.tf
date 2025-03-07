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

resource "google_storage_bucket" "default" {
  for_each                    = var.storage_bucket_names
  name                        = "${var.project_id}-${each.value}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  # It's possible that we may not be able to completely upload a 
  # file due to network issues, timeouts etc.
  # We will want to make sure that we delete any files that are incomplete. 
  # In our configuration we set `age` to be 1, which means GCS will delete 
  # an incomplete file 1 day after we first try to upload it.
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "housing" {
  dataset_id = "housing"
  # the default is the US, it is vital you set this to your region 
  # otherwise you won't be able to query data
  location                   = var.region
  delete_contents_on_destroy = true # while developing set to true
}


