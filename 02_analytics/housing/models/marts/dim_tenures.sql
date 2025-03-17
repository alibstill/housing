WITH unique_tenures AS (
    SELECT DISTINCT tenure_duration AS tenure
    FROM {{ ref('stg_price_paid')}}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['tenure'])}} AS tenure_id,
    tenure,
    CASE
        WHEN tenure = 'F' THEN 'Freehold'
        WHEN tenure = 'L' THEN 'Leasehold'
        ELSE 'unknown'
    END as tenure_name,
FROM unique_tenures
