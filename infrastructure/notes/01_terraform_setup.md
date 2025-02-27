# Terraform setup

Before setting up terraform, make sure that you have performed the necessary manual setup see [essential_manual_setup](./00_essential_manual_setup.md).

## Quickstart

1. Check terraform is installed

```bash
terraform -v
# Terraform v1.10.5
```

2. Create Infrastructure

Your should have saved your terraform service account credentials securely locally. Pass the path to these credentials when you run terraform:

```bash
# Make sure you are in the correct folder
cd infrastructure

terraform init

# Create infrastructure on google cloud
GOOGLE_APPLICATION_CREDENTIALS="/path/to/terraform-service-account-key.json" terraform apply

```
Example:
```bash
GOOGLE_APPLICATION_CREDENTIALS=".credentials/tf-dev.json" terraform apply
```


## Default Configuration

For bespoke variables, you can see the defaults in `variables.tf`.

Many of the resources have been set up with default configuration e.g. you can specify the `storage_class` when you create a `google_storage_bucket` but the default is 'STANDARD', which is suitable for us. See [storage class definitions](https://cloud.google.com/storage/docs/storage-classes). 

To understand more about the default resource configurations check out the [Google Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)