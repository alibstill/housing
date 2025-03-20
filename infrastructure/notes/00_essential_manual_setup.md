# Google Cloud Platform Initial setup

Before deploying any infrastructure with terraform you will need to setup your google account with billing, download terraform and `gcloud` (Google Cloud's CLI) and create a service account for terraform.  

## Create a project on the console

Projects are the organising entity/container for all your resources. 

Navigate to [google cloud](https://console.cloud.google.com/) and create a project. Enter the Project Name.

Google will autogenerate a project id which you need for CLI authentication later. You can edit this if you want.

You can then navigate to the dashboard. In Project Info you will see your Project name, Project number and Project ID.

For more details see [google docs](https://cloud.google.com/docs/overview).

## Enable APIs

Navigate to APIs & Services > Enabled APIs & Services on your console after creating your project and you will notice that some are already enabled by default [see docs](https://cloud.google.com/service-usage/docs/enabled-service).

To allow Terraform to create a service account for Kestra and provide it with permissions, you need to also enable:

- `iam.googleapis.com`: Identity and Access Management (IAM) API
- `cloudresourcemanager.googleapis.com`: Cloud Resource Manager API

## CLI configuration

To deploy infrastructure and generally manage our gcloud project, we need to use the gcloud CLI.

Make sure [gcloud cli](https://cloud.google.com/sdk/docs/install) is installed `gcloud -v`. Download if not.

#### Running init

- `gcloud init`

This command can be used to setup gcloud cli or add a configuration.

Follow instructions to set a configuration for your newly created project. 

The configuration is made up of
- your project id
- your preferred google account

With this, commands that require authentication will automatically use your preferred google account and commands that reference project, will automatically use the project with project id you have set here.

As part of this flow, a login page will open on your browser. This flow will not only configure your CLI but also log you in so you can start running commands against your project.

**Permissions**

By default, the gmail account you used to create the project has "Owner" privileges (full access) so you can configure the CLI with these credentials.

**More info about configuration**

These configurations are likely stored in `.config/gcloud/configurations` but you can double check the path with `gcloud info --format="get(config.paths.active_config_path)"`

- help with config: `gcloud help config`
- details of configurations: `gcloud topic configurations`
- useful commands: `gcloud cheat-sheet`
- list all your configurations: `gcloud config configurations list`

### Logging in to gcloud

#### User account login

- `gcloud auth login`

This command will redirect you to a webpage to login to your google account (remember to login to the one you setup this project in!). 

This flow obtains your credentials and stores them in `~/.config/gcloud/`. Now anytime you run a gcloud command from the terminal, it will find these credentials automatically.

Note that the credentials obtained here are tied to your google user account.

As a dev, you can now use the CLI to run gcloud commands from your terminal. These credentials will not, however, be used by any code or SDK e.g. terraform commands will not be able to run with just this authentication.


## Terraform setup

1. Install terraform

You can find details of the terraform website. We are using v1.10.5.

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform -v
```

2. Login to gcloud with your user account

```bash
gcloud auth login
```

Make sure that your active configuration is the one you setup for this project. You can double check by running, `gcloud config list`

3. Create a service account for terraform with the CLI

name: `sa-{short-project-name}-tf-{environment}`

e.g. "sa-dezc-housing-tf-dev"

```bash
gcloud iam service-accounts create sa-dezc-housing-tf-dev \
--description="Terraform Service Account for dev environment" \
--display-name="DEV Terraform Service Account"
```

Navigate to your GCP console > project > IAM & Admin > Service Accounts and you should see a new service account with email `sa-dezc-housing-tf-dev@dezc-housing.iam.gserviceaccount.co

4. Add roles and permissions for the service account

This command adds IAM policy bindings at the project level. Here we are using it to grant a role to the new service account we have just created. Note that we are giving broad access here, which is not ideal or best practice.

This `editor` role allows you to create and delete resources for most cloud services but it doesn't allow you to set up the Kestra service account and assign it permissions so you need to give terraform the `resourcemanager.projectIamAdmin` role too.

```bash
## general
gcloud projects add-iam-policy-binding PROJECT_ID \
--member="serviceAccount:sa-dezc-housing-tf-dev@{PROJECT_ID}.iam.gserviceaccount.com" \
--role="roles/editor"

## specific
gcloud projects add-iam-policy-binding dezc-housing \
--member="serviceAccount:sa-dezc-housing-tf-dev@dezc-housing.iam.gserviceaccount.com" \
--role="roles/editor"

gcloud projects add-iam-policy-binding dezc-housing \
--member="serviceAccount:sa-dezc-housing-tf-dev@dezc-housing.iam.gserviceaccount.com" \
--role="roles/resourcemanager.projectIamAdmin"
```

Now if you navigate to GCP console > project > IAM & Admin > IAM, you will see two Prinicipals, you and the terraform service account. You have owner access while the terraform account has editor and projectIamAdmin access.

5. Generate and download keys for your service account

It is not ideal to have static keys like this but this is a simpler approach so we will use it for now.

```bash
# update path and project id
gcloud iam service-accounts keys create ~/path/to/key.json \
  --iam-account=your-service-account@{PROJECT_ID}.iam.gserviceaccount.com

gcloud iam service-accounts keys create ./infrastructure/.credentials/tf-dev.json \
  --iam-account=sa-dezc-housing-tf-dev@dezc-housing.iam.gserviceaccount.com
```

6. Create the remote backend (optional)

Terraform state is stored locally but I wanted to try storing it in a remote backend for practice e.g. in a Google Cloud Storage bucket. This involves creating a bucket in GCS and updating the terraform configuration with its name:

```
terraform {
  # add this backend section
  backend "gcs" {
    bucket = "960e97d6ed3a95bd-terraform-remote-backend"  
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.23.0"
    }
  }
}
```

**Creating a bucket: Manual approach**

The simplest way to do this is to manually create a bucket. Navigate to your GCP console > project > Cloud Storage > Buckets. The defaults are fine but I opted to have buckets in a single region:

- Location: choose the region where you are hosting your project e.g. "europe-west2".

You need to copy the name of the bucket and update the `terraform` block.

**Script**

You can also use the script in the [scripts folder](../scripts/) to create the bucket. It will output the name of the newly created bucket which you can then use to update the `terraform` block.


**Deletion**

If you are destroying the whole project, remember to delete this bucket too!

## Getting credentials for other service accounts

### Kestra/ Workflow
I have created the workflow (Kestra) service account with terraform. 

After you have completed the steps above to create the infrastructure on GCP, you can run the following to save the kestra GCP credentials to the workflow directory.

```bash
gcloud auth login

# update path and project id
gcloud iam service-accounts keys create ../01_workflow/.credentials/kestra-dev.json \
  --iam-account=sa-dezc-housing-kestra-dev@dezc-housing.iam.gserviceaccount.com
```

### Dbt
I have created a dbt service account with terraform. 

After you have completed the steps above to create the infrastructure on GCP, you can run the following to save the dbt GCP credentials to the analytics directory.

```bash
gcloud auth login

# update path and project id
gcloud iam service-accounts keys create ../02_analytics/housing/.credentials/dbt-dev.json \
  --iam-account=sa-dezc-housing-dbt-dev@dezc-housing.iam.gserviceaccount.com
```

### Metabase

I have created a metabase service account with terraform. 

After you have completed the steps above to create the infrastructure on GCP, you can run the following to save the metabase GCP credentials to the workflow directory.

```bash
gcloud auth login

# update path and project id
gcloud iam service-accounts keys create ../02_analytics/visualisation/.credentials/metabase-dev.json \
  --iam-account=sa-dezc-housing-metabase-dev@dezc-housing.iam.gserviceaccount.com
```


## A note on overall approach

Since this project is a demo project I have built resources in my own google account to limit costs and complexity. User management options in particular are constrained and not ideal for a professional context: you will notice  if you navigate to IAM & Admin how many features expect an `organization`.

If you wanted to create resources for an organisation and manage users more effectively, you would need to have a Google Workspace (paid service) or Cloud Identity (requires a domain). See [Resource Hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#resource-hierarchy-detail).