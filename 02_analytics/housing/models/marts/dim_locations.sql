
{{
    config(
        materialized='incremental',
        unique_key="location_id",
        incremental_strategy='merge'
    )
}}


WITH unique_locations AS (
    SELECT DISTINCT location_hash,
        paon,
        saon,
        street,
        locality,
        town_city,
        district,
        county,
        postcode
    FROM {{ ref('stg_price_paid') }}
),

staging_locations AS (
    SELECT 
        {{ dbt_utils.generate_surrogate_key([
            'paon',
            'saon',
            'street',
            'locality',
            'town_city',
            'district',
            'county',
            'postcode'
        ])}} AS location_id,
        *,
        CURRENT_DATETIME() AS created_at
    FROM unique_locations
)

SELECT *
FROM staging_locations
{% if is_incremental() %}
-- only update dim_locations with location_ids that don't already exist in it
    WHERE location_id NOT IN (SELECT location_id FROM {{ this }})
{% endif %}
