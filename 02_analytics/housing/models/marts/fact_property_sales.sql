SELECT
   transaction_uid,
   price,
   date_of_transfer,
   location_id,
   property_type_id,
   CASE 
    WHEN is_new_build = 'Y' THEN TRUE
    WHEN is_new_build = 'N' THEN FALSE
    ELSE NULL
   END AS is_new_build,
   tenure_id,
   transaction_type_id
FROM {{ ref('stg_price_paid') }} stg_price_paid
INNER JOIN {{ ref('dim_locations')}} dim_location ON dim_location.location_hash = stg_price_paid.location_hash
INNER JOIN {{ ref('dim_property_types')}} dim_property_type ON dim_property_type.property_type = stg_price_paid.property_type
INNER JOIN {{ ref('dim_tenures')}} dim_tenure ON dim_tenure.tenure = stg_price_paid.tenure_duration
INNER JOIN {{ ref('dim_transaction_types')}} dim_transaction_type ON dim_transaction_type.transaction_type = stg_price_paid.transaction_type


