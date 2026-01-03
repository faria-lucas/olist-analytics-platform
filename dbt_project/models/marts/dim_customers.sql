with customers as (
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    customer_unique_id,
    -- Standardizing city for title (e.g., sao paulo -> SAO PAULO)
    upper(city) as city_upper,
    state
from customers