# Google Cloud Platform Initial setup

Before deploying any infrastructure with terraform you will need to setup your google account with billing, download terraform and `gcloud` (Google Cloud's CLI) and create a service account for terraform  

## Create a project on the console

Projects are the organising entity/container for all your resources. 

Navigate to [google cloud](https://console.cloud.google.com/) and create a project. Enter the Project Name.

Google will autogenerate a project id which you need for CLI authentication later. You can edit this if you want.

You can then navigate to the dashboard. In Project Info you will see your Project name, Project number and Project ID.

For more details see [google docs](https://cloud.google.com/docs/overview).


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

### Logging in to gcloud

#### User account login

- `gcloud auth login`

This command will redirect you to a webpage to login to your google account (remember to login to the one you setup this project in!). 

This flow obtains your credentials and stores them in `~/.config/gcloud/`. Now anytime you run a gcloud command from the terminal, it will find these credentials automatically.

Note that the credentials obtained here are tied to your google user account.

As a dev, you can now use the CLI to run gcloud commands from your terminal. These credentials will not, however, be used by any code or SDK e.g. terraform commands will not be able to run with just this authentication.


## Terraform setup

1. Install terraform

You can find details of the terraform website. We are using v1.9.6.

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

4. Add roles and permissions for the service account

This command adds IAM policy bindings at the project level. Here we are using it to grant a role to the new service account we have just created. Note that we are giving broad access here, which is not ideal or best practice.

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
--member="serviceAccount:sa-dezc-housing-tf-dev@{PROJECT_ID}.iam.gserviceaccount.com" \
--role="roles/editor"
```

5. Generate and download keys for your service account

It is not ideal to have static keys like this but this is a simpler approach so we will use it for now.

```bash
gcloud iam service-accounts keys create ~/path/to/key.json \
  --iam-account=your-service-account@your-project-id.iam.gserviceaccount.com
```

## A note on this approach

Since this project is a demo project I have built resources in my own google account to limit costs and complexity. 

If you wanted to create resources for an organisation and manage users more effectively, you would need to have a Google Workspace (paid service) or Cloud Identity (requires a domain). See [Resource Hiearchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#resource-hierarchy-detail).