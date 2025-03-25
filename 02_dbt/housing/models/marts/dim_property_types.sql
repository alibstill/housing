{{
    config(
        materialized='incremental'
    )
}}


WITH unique_property_types AS (
    SELECT DISTINCT property_type
    FROM {{ ref('stg_price_paid')}}
),

staging_dim_property_types AS (
    SELECT
        {{dbt_utils.generate_surrogate_key(['property_type'])}} AS property_type_id,
        property_type,
        CASE
            WHEN property_type = 'S' THEN 'Semi-Detached'
            WHEN property_type = 'T' THEN 'Terraced'
            WHEN property_type = 'D' THEN 'Detached'
            WHEN property_type = 'F' THEN 'Flats/Maisonettes'
            WHEN property_type = 'O' THEN 'Other'
            ELSE 'unknown' 
        END AS property_type_name,
        CURRENT_DATETIME() AS created_at
    FROM unique_property_types
)

SELECT *
FROM staging_dim_property_types
{% if is_incremental() %}
    WHERE property_type_id NOT IN (SELECT property_type_id FROM {{this}})
{% endif %}



