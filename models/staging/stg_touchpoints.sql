{{ config(materialized='view') }}
select
    touchpoint_id,
    user_id,
    channel,
    touch_order,
    total_touches,
    touched_at::date as touched_at,
    touch_position,
    converted
from {{ source('mkt_raw', 'touchpoints') }}
