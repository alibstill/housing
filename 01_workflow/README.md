# Workflows

This folder contains scripts and configuration required to run Kestra workflows.

## Workflow Descriptions

### Download price paid to local Postgres

- kestra workflow: `flows/local_pg_price_paid.yml`

This workflow downloads a csv file of a years worth of Price Paid data and uploads it to a local postgres database.

## Running Local services

To run Kestra locally together with its postgres backend and the postgres housing database, run

```bash
docker-compose up -d
```

Kestra is available at: http://localhost:8080/

PgAdmin is available at: http://localhost:8085/

### Manual Configuration

1. Adding files to Namespace

The flows make use of some Python [scripts](./scripts/). We need to manually add these files to Kestra.

Navigate to the locally running kestra `Namespaces` (http://localhost:8080/ui/namespaces). Select `housing_local`. Go to `Files` and click on the plus icon to import the `scripts` folder and all its files.


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