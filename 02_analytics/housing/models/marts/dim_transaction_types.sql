{{
    config(
        materialized='incremental'
    )
}}

WITH unique_transaction_types AS (
    SELECT DISTINCT transaction_type 
    FROM {{ ref('stg_price_paid')}}
),

staging_dim_transaction_types AS (
    SELECT
        {{dbt_utils.generate_surrogate_key(['transaction_type'])}} AS transaction_type_id,
        transaction_type,
        CASE 
            WHEN transaction_type = 'A' THEN 'Standard'
            WHEN transaction_type = 'B' THEN 'Additional'
        END AS transaction_type_name,
        CASE
            WHEN transaction_type = 'A' THEN 'single residential property sales for full market value to private individuals'
            WHEN transaction_type = 'B' THEN 'includes repossessions, buy-to-lets and transfers to non-private individuals'
        END as transaction_type_description,
        CURRENT_DATETIME() AS created_at
    FROM unique_transaction_types
)

SELECT *
FROM staging_dim_transaction_types
{% if is_incremental() %}
    WHERE transaction_type_id NOT IN (SELECT transaction_type_id FROM {{this}})
{% endif %}