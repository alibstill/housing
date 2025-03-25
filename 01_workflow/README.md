# Workflows

This folder contains scripts and configuration required to run Kestra workflows.

## Workflow Descriptions

### Core workflows (GCP)

**Note that before you can run any of the core pipelines, you must have setup your Google Cloud Platform (GCP) project and uploaded the google cloud credentials for the kestra service account created by terraform to the local kestra instance. See [Infrastructure](../infrastructure/notes/) and below.**

1. Download Price Paid to GCS

- kestra workflow: `flows/local_gcs_price_paid.yml`

This workflow downloads a csv file of a years worth of Price Paid data and uploads it to a GCS bucket. It also performs some minor preprocessing (e.g. adding column names, adding location hash) and saves the result to another GCS bucket for use downstream.

2. Load data and run transformations with dbt

- kestra workflow: `flows/local_bg_dbt.yml`

This workflow uses dbt to pull in processed data from the GCS bucket and transform it into models that can then be used for analytics.


### Other workflows

3.  Download price paid to local Postgres

- kestra workflow: `flows/local_pg_price_paid.yml`

This workflow downloads a csv file of a years worth of Price Paid data and uploads it to a local postgres database.

4. Sync Files to Namespace (*WIP, not part of v1*)

- kestra workflow: `sync_files_to_namespace`

This workflow will sync all the files in the `01_workflow` and the `02_analytics` folder from my github repo to the `housing_local` namespace, which is not quite what I want to do longterm (I don't want to load all the files).

To work, I needed to create a `GITHUB_ACCESS_TOKEN`. On my github profile, I clicked on my Profile photo then `Settings`. Went to `Developer Settings`, clicked on `Fine-grained tokens` from `Personal access tokens` and generated a new token. The token should have READ-ONLY access for Contents and Metadata.

For version 1, I will manually upload files to the `housing_local` namespace and work on syncing files when I have Kestra running continuously in the cloud.

## Running Kestra

To avoid costs, I have opted to run Kestra locally for v1.

To run Kestra locally together with its postgres backend and the postgres housing database (see workflow 3 above), run

```bash
docker-compose up -d
```

Kestra is available at: http://localhost:8080/

PgAdmin is available at: http://localhost:8085/

### Manual Configuration

1. Adding files to Namespace

Both core flows rely on additional code: we need to manually upload code files to the `housing_local` namespace to enable the pipelines to make use of them.

- `local_gcs_price_paid` needs [scripts](./scripts/)
- `local_bq_dbt` needs [housing]()

The flows make use of some Python . We need to manually add these files to Kestra.

Navigate to the locally running kestra `Namespaces` (http://localhost:8080/ui/namespaces). Select `housing_local`. Go to `Files` and click on the plus icon to import the `scripts` folder and all its files.

2. Setting up environment variables

This project uses a `.env` file to set all environment variables (except GCP credentials). You can see an example [here](.env_example). You should create your own `.env` file with all of these variables set. 

We will load these variables into Kestra as secrets via the `docker-compose.yml` file. You will notice that the `docker-compose.yml` uses a `.env_encoded` file, not the `.env` file. This is because Kestra requires all secrets to be base64 encoded and be prefixed by `SECRET_` so we need to convert our `.env` file. You can do this by running the following in the directory where you have `.env`:

```bash
while IFS='=' read -r key value; do
    echo "SECRET_$key=$(echo -n "$value" | base64)";
done < .env > .env_encoded
```

After running the above in your terminal, you should now see a `.env_encoded` file. See [kestra how-to-guide](https://kestra.io/docs/how-to-guides/secrets) for more information.

**Troubleshooting**

- Your `.env_encoded` is missing the last environment variable

The bash loop script expects each line to end with a newline. Make sure that your `.env` file has this by hitting return after your last line.

3. Uploading 

## Download price paid to local Postgres

In addition to adding files to the Namespace and setting up the environment variables, you will also need to configure pgadmin if you want to view the price paid data in PostgreSQL locally.

### Configuring PgAdmin
This docker-compose.yml contains a PgAdmin instance to make it easier to view your housing database.

After running `docker-compose up -d`, navigate to http://localhost:8085/.

Right click on `Servers` and select `Register. 

In the `General` tab, give the database a name e.g. `housing`. This is just the name that will be used for the database in PgAdmin, it does not need to be the same as the name used in your docker-compose file.

In connection enter the following:
- Host name/address: host.docker.internal
- Port: 5435 
- Username: my_user
- Password: my_password

Note that port, username and password must match the configurations specified in your docker-compose file.

## Download Price Paid to GCS

In addition to adding files to the Namespace and setting up the environment variables, you will also need to ensure that you have uploaded your google cloud credentials to kestra's key/value store.

Remember, before you can run this pipeline, you must have setup your Google Cloud Platform (GCP) project and downloaded the credentials of the kestra service account created by terraform. See [Infrastructure](../infrastructure/notes/). 

### Adding Credentials to key/value store

Navigate to your locally running kestra at `http://localhost:8080` > Namespaces > KV Store and add an entry for your Google Cloud credentials:

```bash
KEY: GCP_CREDENTIALS
TYPE: JSON
VALUE: # see below
```
For the value field, you should paste in the credentials that you downloaded after setting up the service account for Kestra with terraform. See [Terraform essential manual setup](../infrastructure/notes/00_essential_manual_setup.md).

The JSON will look something like this:

```json
{
  "type": "service_account",
  "project_id": "{project-id}",
  "private_key_id": "c123567492",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBA\n-----END PRIVATE KEY-----\n",
  "client_email": "{service-account-name}@{project-id}.iam.gserviceaccount.com",
  "client_id": "11321",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/{service-account-name}%40{project-id}.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```
