{{ config(materialized='table') }}
select
    a.channel,
    a.model,
    a.attributed_conversions,
    s.total_spend,
    round(s.total_spend / nullif(a.attributed_conversions, 0), 2) as cac,
    round(a.attributed_conversions * 350 / nullif(s.total_spend, 0), 2) as roas
from {{ ref('attribution_models') }} a
left join (
    select channel, sum(spend) as total_spend
    from {{ source('mkt_raw', 'channel_spend') }}
    group by 1
) s using (channel)
