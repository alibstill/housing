{{
    config(
        materialized='incremental'
    )
}}

WITH unique_tenures AS (
    SELECT DISTINCT tenure_duration AS tenure
    FROM {{ ref('stg_price_paid')}}
),

staging_dim_tenures AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['tenure'])}} AS tenure_id,
        tenure,
        CASE
            WHEN tenure = 'F' THEN 'Freehold'
            WHEN tenure = 'L' THEN 'Leasehold'
            ELSE 'unknown'
        END as tenure_name,
        CURRENT_DATETIME() AS created_at
    FROM unique_tenures
)

SELECT *
FROM staging_dim_tenures
{% if is_incremental() %}
    WHERE tenure_id NOT IN (SELECT tenure_id FROM {{this}})
{% endif %}


