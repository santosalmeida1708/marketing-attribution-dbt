"""Generate synthetic marketing attribution data."""
import os, random
from datetime import date, timedelta
import pandas as pd
from sqlalchemy import create_engine

DB_URL = os.getenv("DATABASE_URL", "postgresql://mkt_user:mkt_pass@localhost:5435/mkt_db")
random.seed(42)

CHANNELS = ["paid_search", "organic_search", "social_media", "email", "display", "referral"]
CHANNEL_COSTS = {"paid_search": 5000, "organic_search": 0, "social_media": 3000,
                 "email": 500, "display": 2000, "referral": 1000}

def generate():
    engine = create_engine(DB_URL)
    touchpoints = []
    conversions = []

    for user_id in range(1, 1201):
        n_touches = random.randint(1, 8)
        start = date(2024, 1, 1) + timedelta(days=random.randint(0, 364))
        touches = []
        for i in range(n_touches):
            ts = start + timedelta(days=i * random.randint(1, 7))
            channel = random.choice(CHANNELS)
            touches.append({
                "touchpoint_id": f"tp_{user_id}_{i}",
                "user_id": f"user_{user_id:04d}",
                "channel": channel,
                "touch_order": i + 1,
                "total_touches": n_touches,
                "touched_at": ts,
                "touch_position": "first" if i == 0 else ("last" if i == n_touches - 1 else "middle"),
                "converted": random.random() < 0.25
            })
        touchpoints.extend(touches)
        if touches[-1]["converted"]:
            conversions.append({"user_id": f"user_{user_id:04d}",
                                 "converted_at": touches[-1]["touched_at"],
                                 "order_value": random.uniform(50, 2000)})

    pd.DataFrame(touchpoints).to_sql("touchpoints", engine, if_exists="replace", index=False)
    pd.DataFrame(conversions).to_sql("conversions",  engine, if_exists="replace", index=False)
    channel_spend = [{"channel": c, "month": f"2024-{m:02d}-01", "spend": v * random.uniform(0.8,1.2)}
                     for c, v in CHANNEL_COSTS.items() for m in range(1,13)]
    pd.DataFrame(channel_spend).to_sql("channel_spend", engine, if_exists="replace", index=False)
    print(f"Generated {len(touchpoints)} touchpoints, {len(conversions)} conversions")

if __name__ == "__main__":
    generate()
