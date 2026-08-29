{{ config(materialized='table') }}
with last_touch as (
    select channel, 'Last Touch' as model,
        count(distinct user_id) as attributed_conversions
    from {{ ref('stg_touchpoints') }}
    where touch_position = 'last' and converted
    group by 1
),
first_touch as (
    select channel, 'First Touch' as model,
        count(distinct user_id) as attributed_conversions
    from {{ ref('stg_touchpoints') }}
    where touch_position = 'first' and converted
    group by 1
),
linear_touch as (
    select channel, 'Linear' as model,
        sum(1.0 / total_touches) as attributed_conversions
    from {{ ref('stg_touchpoints') }}
    where converted
    group by 1
),
time_decay as (
    select channel, 'Time Decay' as model,
        sum(power(2.0, touch_order - 1) /
            sum(power(2.0, touch_order - 1)) over (partition by user_id)) as attributed_conversions
    from {{ ref('stg_touchpoints') }}
    where converted
    group by 1, user_id
)
select * from last_touch
union all select * from first_touch
union all select * from linear_touch
union all select channel, model, sum(attributed_conversions) from time_decay group by 1,2
