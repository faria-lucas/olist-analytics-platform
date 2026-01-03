with products as (
    select * from {{ ref('stg_products') }}
)

select
    product_id,
    coalesce(product_category, 'others') as product_category,
    product_weight_g,
    -- Add volume calculations (L x W x H)
    (product_length_cm * product_height_cm * product_width_cm) as product_volume_cm3
from products