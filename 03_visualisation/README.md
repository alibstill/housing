# Visualisation

I created a dashboard using Metabase. For a guided tour of the final dashboard, check out my loom video:

[![Watch the video](https://cdn.loom.com/sessions/thumbnails/c7980272036f474496f2bb08bee83dd3-c1747f9d4dc41e42-full-play.gif)](https://www.loom.com/share/c7980272036f474496f2bb08bee83dd3?sid=8d8101cf-4477-4d5c-b775-ad5b5d5eee3d)

Unfortunately, I was not able to easily extract and [load a configuration file](https://www.metabase.com/docs/latest/configuring-metabase/config-file) on the free version of Metabase so I have included instructions on how to recreate the dashboards manually. 

## Manually recreating the dashboard locally

**Before you can do this you must have set up your infrastructure. See [Essential Manual Setup](../infrastructure/notes/00_essential_manual_setup.md) and loaded data into BigQuery i.e. you need to run the Kestra workflows. See [Workflow README.md](../01_workflow/README.md)**

### 1. Run metabase with Docker

Run the following command from this folder to create a local version of metabase:

```bash
docker-compose up -d
```

Navigate to `http://localhost:3000` and you will automatically be rerouted to a setup page.

### 2. First time configuration

This first time you run metabase you will have to configure it. The `docker-compose` file contains volumes so provided you don't delete these, you should only have to do this once.

There are several stages:

- Choose language

- User details

For local development this can be anything e.g.

**Name**: Example

**Email**: a@housing-example.com

**Company**: housing-example

**Password**: 1simple_housing_password (must contain number)

- Metabase usage

- Add your Data

Select BigQuery.

**Display name**: Property Prices (this is the name you see in metabase)

**Project ID**: {gcloud-project-id} 

**Service account JSON**: upload the `metabase-dev.json` google cloud credentials that you created when you ran terraform. See [Essential Manual Setup](../infrastructure/notes/00_essential_manual_setup.md).

**Datasets**: All (for simplicity)

- Usage data preferences

After you complete these steps, you will be automatically redirected to your local Metabase homepage. You will notice that there is an Examples collection that comes with Metabase.

### 3. Create a New collection (optional)

This is not necessary but I found it easier to group all my SQL queries and dashboard in a separate collection.

In the home page, under collections go to the ellipsis (`...`) and choose `+ New collection` from the drop down. 

Create a collection e.g. `Price Paid (England & Wales)`

### 4. Create Questions with SQL Queries

I used the native query editor in metabase to retrieve data that I needed for each dashboard tile.

To create a sql statement that queries the BigQuery data, click on the blue `+ New` button in the top right corner and select `SQL Query`.

See [SQL Queries](sql_queries.md) for more information of each.

### 5. Create Dashboard

To create a dashboard, click on the blue `+ New` button in the top right corner and select `Dashboard`.

(You will be prompted when you create SQL queries, to add them to a dashboard. You can build up the dashboard like this if you want.)

Building a dashboard is fairly intuitive so I'll just note a few things I needed to look up:

**Layout**

You can add structure to your dashboard with sections and tabs.

My dashboard is divided into two sections: Overview and Property Price by Property Type.

There is an `Add section` button on the right hand side of the dashboard that you can use to create sections. This will allow you to add a Heading and then select questions to include in the section.

**Adding a filter**

I use a location filter dropdown in my second dashboard to allow users to see property price data specific to a county in England and Wales.

Watch Metabase's [How to set up dashboard filters for SQL queries](https://youtu.be/itNp4cHktlw?feature=shared) tutorial for a good overview of how to achieve this. Note that you need to have created a `Field Filter`. See the [Location - Field Filters](./sql_queries.md) section.

