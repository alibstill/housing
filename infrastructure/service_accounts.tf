
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account
resource "google_service_account" "kestra_service_account" {
  account_id                   = "sa-dezc-housing-kestra-dev"
  display_name                 = "DEV Kestra Service Account"
  description                  = "Kestra Service Account for dev environment"
  create_ignore_already_exists = true
}

# Creation of service accounts is eventually consistent, and that can lead to errors when you try to apply ACLs to service accounts immediately after creation
resource "null_resource" "delay" {
  provisioner "local-exec" {
    command = "sleep 10"
  }
  triggers = {
    "before" = "${google_service_account.kestra_service_account.id}"
  }
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_iam#google_project_iam_member-1
resource "google_project_iam_member" "kestra_gcs_admin" {
  project    = var.project_id
  role       = "roles/storage.admin"
  member     = google_service_account.kestra_service_account.member
  depends_on = [null_resource.delay]
}
