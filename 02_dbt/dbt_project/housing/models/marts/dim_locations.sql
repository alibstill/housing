
{{
    config(
        materialized='incremental',
        unique_key="location_id",
        incremental_strategy='merge'
    )
}}

-- Get unique location information across rows
WITH unique_location_rows AS (
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

-- Add location_id
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
        location_hash,
        paon,
        saon,
        street,
        locality,
        town_city,
        district,
        county,
        postcode
    FROM unique_location_rows
),

-- identify rows with the same location_hash
-- example scenario: row 1 has {paon:23, saon: null...}, row 2 has {paon:null, saon: 23...}
-- row 1 and row 2 will have the same location_hash but different location_ids
ranked_locations AS (
    SELECT *,
        DENSE_RANK() OVER(PARTITION BY location_hash ORDER BY location_id) as rank
    FROM staging_locations
),

deduped_locations AS (
    SELECT *,
        CURRENT_DATETIME() AS created_at   
    FROM ranked_locations
    WHERE rank = 1
)

SELECT *
FROM deduped_locations
{% if is_incremental() %}
    -- only update dim_locations when new location_hash that don't already exist in it
    WHERE location_hash NOT IN (SELECT location_hash FROM {{ this }})
{% endif %}
