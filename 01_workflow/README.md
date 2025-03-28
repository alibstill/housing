# Workflows

This folder contains scripts and configuration required to run Kestra workflows.

## Workflow Descriptions

### Core workflow (GCP)

**Note that before you can run any of the core pipelines, you must have setup your Google Cloud Platform (GCP) project and uploaded the google cloud credentials for the kestra service account created by terraform to the local kestra instance. See [Infrastructure](../infrastructure/notes/) and below (Manual Configuration (3)).**

1. ETLT: extract, transform, load and transform price paid

- name: `gc_etlt_price_paid`
- kestra workflow: `flows/housing_local_gc_etlt_price_paid.yml`

**Tasks**

There are three main tasks, two call subflows and are built to run in parallel with a maximum of 4 threads. This means it extracts and transforms 4 years of data at a time. Note that the tasks run sequentially i.e. raw data for all years (1995 to 2025 inclusive) is extracted and loaded to GCS first before being transformed in the second task.

```mermaid
flowchart LR
  ExtractRaw --> TransformRaw
  TransformRaw --> Load[Load and Transform in BigQuery]
  subgraph ExtractRaw[Extract Raw to GCS]
    YearRaw[List of years] --> StartExtractPricePaid1
    YearRaw --> StartExtractPricePaid2
    YearRaw --> StartExtractPricePaid3
    YearRaw --> StartExtractPricePaid4
    subgraph "Thread 1"
      StartExtractPricePaid1[Year] --> ExtractUpload1[Run gc_extract_raw_price_paid pipeline]
    end
    subgraph "Thread 2"
      StartExtractPricePaid2[Year] --> ExtractUpload2[Run gc_extract_raw_price_paid pipeline]
    end
    subgraph "Thread 3"
      StartExtractPricePaid3[Year] --> ExtractUpload3[Run gc_extract_raw_price_paid pipeline]

    end
    subgraph "Thread 4"
      StartExtractPricePaid4[Year] --> ExtractUpload4[Run gc_extract_raw_price_paid pipeline]
    end    
  end
  subgraph TransformRaw[Transform Raw to GCS]
    YearTransformed[List of years] --> StartTransformPricePaid1
    YearTransformed --> StartTransformPricePaid2
    YearTransformed --> StartTransformPricePaid3
    YearTransformed --> StartTransformPricePaid4
    subgraph "Thread 1"
      StartTransformPricePaid1[Year] --> TransformUpload1[Run gc_transform_raw_price_paid pipeline]
    end
    subgraph "Thread 2"
      StartTransformPricePaid2[Year] --> TransformUpload2[Run gc_transform_raw_price_paid pipeline]
    end
    subgraph "Thread 3"
      StartTransformPricePaid3[Year] --> TransformUpload3[Run gc_transform_raw_price_paid pipeline]
    end
    subgraph "Thread 4"
      StartTransformPricePaid4[Year] --> TransformUpload4[Run gc_transform_raw_price_paid pipeline]
    end    
  end
```

**What does it do?**

This workflow retrieves price paid data for every year from 1995 to 2025, loads the raw data into google cloud storage bucket ("raw") then transforms this raw data and stores the end result in another google cloud storage bucket ("processed") as parquet files. After this the pipeline runs dbt commands to load the parquet files into BigQuery as an external table and transform the data to create new dimension, fact and aggregate tables for use in downstream analytics.

**Subflows called**

This workflow calls the following subflows:
- `gc_extract_raw_price_paid`
- `gc_transform_raw_price_paid`
- `gc_load_transform_price_paid`

**When to use**

This is the core workflow i.e. the one that should be run every month to get the most up-to-date price paid data.

This workflow took around 1 hour to complete on my machine.


### Subflows

2. **Extract** 

- name: - `gc_extract_raw_price_paid`
- kestra workflow: `flows/housing_local_gc_extract_raw_price_paid.yml`

**Tasks**

```mermaid
flowchart LR
  Start["Select Year (1995 - 2025)"] --> SetLabel[Set Labels]
  SetLabel --> Extract[Download Price Paid CSV]
  Extract --> UploadRaw[Upload Price Paid CSV to 'raw' bucket <img src='images/cloud_storage.svg' width='40' height='40' /> ]
  UploadRaw --> Purge[Purge large files]
```

**What does it do?**

This workflow takes a year in the range 1995 to 2025 as input and downloads a csv file of Price Paid data for that year. It then uploads this raw csv file to the `landregistry_price_paid` folder in a GCS bucket called `{google-cloud-project-id}-raw`. The `{project-id}-raw/landregistry_price_paid` bucket is where the original, untransformed yearly price paid csvs are stored. 

Since the data is updated monthly, each raw file has the following naming conventions: 

- `pp-{yyyy}_{yyyy-MM}.csv` e.g. `pp-2004_2025-03.csv` 

This indicates that this file is the price paid data for 2004 downloaded in March 2025. 

The size of the price paid files range from 115 MB to 230 MB.

**When to use**

You can use this to download a file with a specific year to GCS.

3. **Transform (Basic)**

- name:`gc_transform_raw_price_paid`
- kestra workflow: `flows/housing_local_gc_transform_raw_price_paid.yml`

**Tasks**

```mermaid
flowchart LR
  Start["Select Year (1995 - 2025)"] --> SetLabel[Set Labels]
  SetLabel --> Extract[Download Raw Price Paid CSV from GCS <img src='images/cloud_storage.svg' width='40' height='40'/> ]
  Extract --> Transform[Transform]
  Transform --> UploadProcessed[Upload transformed parquet file to 'processed' bucket <img src='images/cloud_storage.svg' width='40' height='40'/> ]
  UploadProcessed --> Purge[Purge large files]
```

**What does it do?**

This workflow takes a year in the range 1995 to 2025 as input and loads the relevant raw price paid data from the month in which the pipeline is running e.g. I was running the pipeline with year=2004 in March 2025 so it picked up the `pp-2004_2025-03.csv` file. It then performs some minor transformations and stores the result in a GCS bucket called `{google-cloud-project-id}-processed`.

**When to use**

You can use this to transform a file for a specific year.

4. Load and Transform with dbt

- name: `gc_load_transform_price_paid`
- kestra workflow: `flows/housing_local_gc_load_transform_price_paid.yml`

**Task**

There is only one task, `dbt build`, which runs the following commands:

```mermaid
flowchart LR
  Start[dbt deps] --> ExternalTables["dbt run-operation stage_external_sources (create/refresh external tables)"]
  ExternalTables --> DbtBuild[dbt build] 
```

**What does it do?**

This workflow runs the dbt project which loads the price paid parquet files from the "processed" bucket as an external table in BigQuery and then performs a series of transformations to create some dimension, fact and aggregate tables for downstream analytics

**When to use**

Use this when you want to create tables in Bigquery.

### Other workflows

5.  **Extract and Transform Price Paid data to google cloud storage (*deprecated*)**

- name: `gc_extract_transform_raw_price_paid`
- kestra workflow: `flows/housing_local_gc_extract_transform_raw_price_paid.yml`

**Tasks**

```mermaid
flowchart LR
  Start["Select Year (1995 - 2025)"] --> SetLabel[Set Labels]
  SetLabel --> Extract[Download Price Paid CSV]
  Extract --> UploadRaw[Upload Price Paid CSV to 'raw' bucket <img src='images/cloud_storage.svg' width='40' height='40' /> ]
  UploadRaw --> Transform[Transform]
  Transform --> UploadProcessed[Upload transformed parquet file to 'processed' bucket <img src='images/cloud_storage.svg' width='40' height='40'/> ]
  UploadProcessed --> Purge[Purge large files]
```

**What does it do?**

This workflow combines `gc_extract_raw_price_paid` and `gc_transform_raw_price_paid`. 

**When to use**

This is an old flow but I kept it here because it may be useful when you want to download and transform data for a specific year.

6. Sync Files to Namespace (*not part of v1*)

- name: `sync_files_to_namespace`
- kestra workflow: `flows/housing_local_sync_files_to_namespace`

**What does it do?**

This workflow will sync all the files in the `01_workflow/scripts` and the `02_dbt/dbt_project` folder from my github repo to the `housing_local` namespace.

For version 1, I will manually upload files to the `housing_local` namespace and work on syncing files when I have Kestra running continuously in the cloud.

**When to use**

Note that if you want to get this flow to work, you will need to upload the project to your own github repo and generate a github access token with read-only access for Contents and Metadata.

To get this to work, I needed to create a `GITHUB_ACCESS_TOKEN`. On my github profile, I clicked on my Profile photo then `Settings`. Went to `Developer Settings`, clicked on `Fine-grained tokens` from `Personal access tokens` and generated a new token. The token should have READ-ONLY access for Contents and Metadata. I then added it to my `.env` (see .env_example). 

## Running Kestra

To avoid costs, I have opted to run Kestra locally for v1.

To run Kestra locally together with its postgres backend run

```bash
docker-compose up -d
```

Kestra is available at: http://localhost:8080/

Navigate to Flows and you should see all 6 workflows described above.


### Manual Configuration

1. Adding files to Namespace

Both core flows rely on additional code: we need to manually upload code files to the `housing_local` namespace to enable the pipelines to make use of them.

- `local_gcs_price_paid` needs [scripts](./scripts/scripts)
- `local_bq_dbt` needs [housing](../02_dbt/dbt_project/housing)

Navigate to the locally running kestra `Namespaces` (http://localhost:8080/ui/namespaces). Select `housing_local`. Go to `Files` and click on the plus icon, select `import folder`. In the file navigator, select:

- `01_workflow/scripts/scripts`

This will upload the whole `scripts` folder. 

Repeat this process to import the `housing` dbt project:

- `02_dbt/dbt_project/housing`

You should now have two folders in your Namespaces: `housing` and `scripts`.

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

3. Upload JSON Credentials to Kestra key-value store

In addition to adding files to the Namespace and setting up the environment variables, you will also need to ensure that you have uploaded your google cloud credentials to kestra's key/value store.

Remember, before you can run this pipeline, you must have setup your Google Cloud Platform (GCP) project and downloaded the credentials of the kestra service account created by terraform. See [Infrastructure](../infrastructure/notes/). 

Navigate to your locally running kestra at `http://localhost:8080` > Namespaces > KV Store and add an entry for your Google Cloud Kestra credentials:

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