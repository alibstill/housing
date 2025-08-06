WITH raw_price_paid AS (
    SELECT * FROM {{ source('land_registry', 'price_paid') }}
)

SELECT 
   CAST(transaction_uid AS STRING) AS transaction_uid,
   CAST(price AS INT64) AS price,
   CAST(date_of_transfer AS DATE) As date_of_transfer, 
   CAST(postcode AS STRING) AS postcode,
   CAST(property_type AS STRING) AS property_type,
   CAST(is_new_build AS STRING) AS is_new_build,
   CAST(tenure_duration AS STRING) AS tenure_duration,
   CAST(paon AS STRING) AS paon,
   CAST(saon AS STRING) AS saon,
   CAST(street AS STRING) AS street,
   CAST(locality AS STRING) AS locality,
   CAST(town_city AS STRING) AS town_city,
   CAST(district AS STRING) AS district,
   CAST(county AS STRING) AS county,
   CAST(transaction_type AS STRING) AS transaction_type,
   CAST(record_status AS STRING) AS record_status,
   CAST(location_hash AS STRING) AS location_hash
FROM raw_price_paid