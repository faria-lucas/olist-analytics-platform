with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select 
        order_id,
        sum(price) as total_items_price,
        sum(freight_value) as total_freight_value,
        sum(total_item_amount) as total_order_amount,
        count(order_item_id) as total_items_count
    from {{ ref('stg_order_items') }}
    group by 1
)

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchased_at,
    o.delivered_customer_at,
    o.estimated_delivery_at,
    -- Time Metrics
    date_diff('day', o.purchased_at, o.delivered_customer_at) as actual_delivery_days,
    date_diff('day', o.purchased_at, o.estimated_delivery_at) as estimated_delivery_days,
    -- Financial Metrics
    i.total_items_price,
    i.total_freight_value,
    i.total_order_amount,
    i.total_items_count
from orders o
left join order_items i on o.order_id = i.order_id
where i.total_order_amount is not null -- Remove orders without items