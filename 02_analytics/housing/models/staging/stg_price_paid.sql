with price_paid as (
    select * from {{ source('land_registry', 'price_paid') }}
)

select 
   *
from price_paid