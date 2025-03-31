# UK Residential Property Sales Data Pipeline

## Overview

This project focuses on extracting and visualising data related to residential property sales in England & Wales. The goal is to understand better what factors influence property price changes by analyzing various attributes, such as location, property type (Semi-Detached/Flat/Terraced/Detached), age (new build vs. old), and leasehold status. In the long term, the project will expand to include Energy Performance Certificate (EPC) data, enabling predictions about which homes are most likely to need retrofitting and estimating retrofit costs.

[![Demo of Dashboard](https://cdn.loom.com/sessions/thumbnails/c7980272036f474496f2bb08bee83dd3-c1747f9d4dc41e42-full-play.gif)](https://www.loom.com/share/c7980272036f474496f2bb08bee83dd3?sid=8d8101cf-4477-4d5c-b775-ad5b5d5eee3d)

## Problem description

The residential property market is influenced by a range of factors, including the location of the property, its type, whether it is a new build, and its leasehold status. Understanding how these factors interact and contribute to property price changes is essential for both buyers and sellers in making informed decisions.

This project aims to explore the relationships between key property attributes and price changes.

In future iterations, I would like to:
- Build predictive models to forecast housing prices.
- Integrate EPC data to predict homes requiring retrofitting and assess retrofit cost implications.

## Key features

- **ELT Data Pipeline**: A pipeline that extracts residential property sale data, including location, property type, new build status, and leasehold status and loads it into BigQuery where it is then transformed into fact and dimension tables for ease of analysis with dbt. The pipeline should be run monthly to obtain updates to data across the years.

- **Data Visualisation**: Integration with Metabase for interactive visualisation of property sale trends

## Data Sources 

### Price Paid Data

The Price Paid data is published by the HM Land Registry. It includes data on all residential property sales in England and Wales that were sold for a value, with records dating back to 1995. See [HM Land Registry Price Paid Data webpage](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#full-publication-update-history).

Information is published monthly with a monthly lag e.g. December 2024 data was published on 29 January 2025. The data is updated on the 20th working day of each month. 

**Attribution**: Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

## Approach and General Workflow

The Price Paid data is updated monthly, so I’ve designed a batch ELT pipeline using Kestra and dbt. Raw data is stored in Google Cloud Storage, and BigQuery is used as the data warehouse, partitioned by year to optimize query performance. I’ve structured the data using dbt to create fact and dimension tables, as well as an aggregated fact table for the dashboard. The dashboard itself is built using Metabase.

To minimize costs for version 1, I opted not to host Kestra or Metabase in the cloud.

**Workflow**

1. Set up the basic infrastructure with terraform. See [Essential Manual Setup](./infrastructure/notes/00_essential_manual_setup.md)

2. Run the pipelines with Kestra. See [Workflow README](./01_workflow/README.md) to get setup.

3. Visualise data with Metabase. See [Visualisation README](./03_visualisation/README.md)
