-- This is a DBT template that cleans the request data.
WITH source AS (
    SELECT * FROM {{ source('olist', 'raw_orders') }}
),

renamed AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        -- Converting strings to timestamps (essential for analytics)
        CAST(order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
        CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_at,
        CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_at
    FROM source
)

SELECT * FROM renamed