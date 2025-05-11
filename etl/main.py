import asyncio
from datetime import datetime as dt, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from connection import async_session
from extractor import extract_updated_products
from loader import load_to_elasticsearch
from shared.core.config import get_settings


settings = get_settings()
SCHEDULE_INTERVAL_SECONDS = settings.SCHEDULE_INTERVAL_SECONDS
last_sync_time = dt.now(timezone.utc) - timedelta(minutes=10)


async def etl():
    global last_sync_time
    async with async_session() as session:
        products = await extract_updated_products(session, last_sync_time)
        if products:
            await load_to_elasticsearch(products)
            print(f"[ETL] Synced {len(products)} updated product(s)")
        else:
            print("[ETL] No changes to sync.")
        last_sync_time = dt.now(timezone.utc)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(etl, "interval", seconds=SCHEDULE_INTERVAL_SECONDS)
    scheduler.start()

    print(f"[ETL] Scheduler started. Interval: {SCHEDULE_INTERVAL_SECONDS} seconds")
    asyncio.get_event_loop().run_forever()