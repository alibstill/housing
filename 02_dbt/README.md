# DBT Project


## Setting up the project

I set up the project with `dbt-core` and `dbt-bigquery` to enable the project to be run against BigQuery.

```bash
# create and install requirements
python3 -m venv .venv_analytics
source .venv_analytics/bin/activate
pip install -r requirements.txt
```

### Running dbt locally
Before you can run any dbt commands locally, you must

1. Have performed all the necessary infrastructure setup e.g. setup a Google cloud platform account, created Google Cloud Storage buckets, created a service account for dbt and downloaded credentials. See [Essential Manual Setup](../infrastructure/notes/00_essential_manual_setup.md)

2. Loaded data into the  Google Cloud Storage bucket called `dezc-housing-processed`: you can do this by running the Kestra pipeline `gcs_price_paid`.

3. Set up a `profile.yml` in the root of the dbt housing project (same level as `dbt_project.yml`) to provide the BigQuery connection details.

```yaml
housing:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: <gcloud-project-id>
      dataset: <dataset-name-see-terraform>
      location: <location-of-project-see-terraform>
      threads: 4 # Must be a value of 1 or greater
      keyfile: ./.credentials/dbt-dev.json
```

I stored my service account credentials in a relative folder: `./.credentials/dbt-dev.json`. If you use [Essential Manual Setup](../infrastructure/notes/00_essential_manual_setup.md), this is the folder that the credentials will download to.

After this, you can run dbt locally:

```bash
source .venv_analytics/bin/activate

# Make sure you are in the directory
cd dbt_project/housing

# Make sure that your configuration works and you can connect to BigQuery
dbt debug

dbt clean

# Run to install dbt_external tables
dbt deps

# Create source nodes i.e. parquet files in GCS
# After running this you should be able to see the price_paid table in BigQuery
dbt run-operation stage_external_sources

# Run specific model and all nodes it requires
dbt run --select +stg_price_paid
```

**Generate Docs**

```bash
dbt docs generate

dbt docs serve --port=8090 # if you have kestra running you need to specify a different port
```

**Run tests**

Remember that before tests can be run, you need to create the models. 

```bash
dbt run
dbt test
```