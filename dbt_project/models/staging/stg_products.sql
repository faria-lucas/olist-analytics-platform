with source as (
    select * from {{ source('olist', 'raw_products') }}
),

renamed as (
    select
        product_id,
        product_category_name,
        -- Removing underscores to make the Dashboard name look nicer
        replace(product_category_name, '_', ' ') as product_category,
        product_name_lenght as product_name_length,
        product_description_lenght as product_description_length,
        product_photos_qty as product_photos_count,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    from source
)

select * from renamed