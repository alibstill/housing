--Return all rows whose date_of_transfer doesn't safely cast to date
SELECT date_of_transfer
FROM {{ ref('stg_price_paid') }}
WHERE SAFE_CAST(date_of_transfer AS DATE) IS NULL