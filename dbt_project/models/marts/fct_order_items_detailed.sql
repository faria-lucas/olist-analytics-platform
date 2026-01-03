with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('dim_products') }}
)

select
    i.order_id,
    i.order_item_id,
    i.product_id,
    p.product_category,
    i.price,
    i.freight_value,
    i.total_item_amount,
    p.product_weight_g,
    p.product_volume_cm3
from order_items i
left join products p on i.product_id = p.product_id