# DBT Project


## Getting started

I set up the project with `dbt-core` and `dbt-bigquery`

```bash
# create and install requirements
python3 -m venv .venv_analytics
source .venv_analytics/bin/activate
pip install -r requirements.txt

# Make sure you are in the directory
cd housing

# Run dbt commands
dbt build
dbt run
```