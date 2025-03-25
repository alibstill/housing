{{ config(
   materialized='incremental',
   partition_by={'field': 'day_date', 'data_type': 'DATE', 'granularity': 'year'}
)}}

WITH raw_dates AS (
    SELECT day_date
    FROM UNNEST(GENERATE_DATE_ARRAY(DATE('1995-01-01'),DATE('2026-01-01'), INTERVAL 1 day)) AS day_date
),

staging_dim_dates AS (
    SELECT
        day_date,
        EXTRACT(day FROM day_date) AS day,
        EXTRACT(month FROM day_date) AS month_number,
        EXTRACT(year FROM day_date) AS year,
        EXTRACT(dayofweek FROM day_date) AS weekday_number,
        EXTRACT(quarter FROM day_date) AS quarter,
        EXTRACT(week FROM day_date) AS week,
        FORMAT_DATE('%A', day_date) AS weekday_name,
        FORMAT_DATE('%B', day_date) AS month_name,
        CURRENT_DATETIME() AS created_at
    FROM raw_dates
)
SELECT *
FROM staging_dim_dates
{% if is_incremental() %}
-- only add new dates
    WHERE day_date > (SELECT MAX(day_date) FROM {{this}})
{% endif %}

