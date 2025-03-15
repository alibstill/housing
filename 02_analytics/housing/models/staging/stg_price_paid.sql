with raw_price_paid as (
    select * from {{ source('land_registry', 'price_paid') }}
)

select 
   CAST(transaction_uid, AS STRING),
   CAST(price AS INT64),
   CAST(date_of_transfer AS DATE),
   CAST(postcode AS STRING),
   CAST(property_type AS STRING),
   CAST(is_new_build AS STRING),
   CAST(tenure_duration AS STRING),
   CAST(paon AS STRING),
   CAST(saon AS STRING),
   CAST(street AS STRING),
   CAST(locality AS STRING),
   CAST(town_city AS STRING),
   CAST(district AS STRING),
   CAST(county AS STRING),
   CAST(transaction_type AS STRING),
   CAST(record_status AS STRING),
   CAST(location_hash AS STRING)
 
from raw_price_paid