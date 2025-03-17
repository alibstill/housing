-- when preprocessing the data I generated a location_hash. 
-- this is a first pass. Another option would be to more rigorously identify location by checking
-- postcodes etc.
-- based on concatenating "postcode","paon","saon","street","locality","town_city","district","county"

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
)

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
    *
    FROM unique_locations
