# Marketing Attribution — dbt Project

Analytics Engineering project implementing **4 attribution models** with dbt.

## Attribution Models

| Model | Logic |
|---|---|
| Last Touch | 100% credit to last touchpoint |
| First Touch | 100% credit to first touchpoint |
| Linear | Equal credit split across all touches |
| Time Decay | Exponential credit (later touches get more) |

## Key Models
- `attribution_models` — all 4 models in one UNION ALL query
- `channel_performance` — ROAS and CAC per channel per model

## How to Run
```bash
docker compose up -d
python scripts/generate_marketing_data.py
dbt deps && dbt run && dbt test
```
