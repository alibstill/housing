WITH unique_transaction_types AS (
    SELECT DISTINCT transaction_type 
    FROM {{ ref('stg_price_paid')}}
)


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
    END as transaction_type_description
FROM unique_transaction_types