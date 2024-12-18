
import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from .news.router import router as news_router
from .users.router import router as users_router
from .prices.router import router as prices_router
from .database import SessionLocal
from .news.service import (get_new_info)
from .news.models import NewsArticle
from .config import get_main_settings
from sentry_sdk import capture_exception
import logging
main_settings=get_main_settings()
sentry_sdk.init(
    dsn="https://c002ed3a235c1ad39f64f93194f1b66b@o4508490249732096.ingest.us.sentry.io/4508490254974976",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set continuous_profiling_auto_start to True
    # to automatically start the profiler on when
    # possible.
    profiles_sample_rate=1.0,
)


app = FastAPI()
Scheduler = BackgroundScheduler()


app.include_router(news_router, prefix=main_settings.FASTAPI_PRIFIX)
logging.debug("News router (/news) initialised")
app.include_router(users_router, prefix=main_settings.FASTAPI_PRIFIX)
logging.debug("Users router (/router) initialised")
app.include_router(prices_router, prefix=main_settings.FASTAPI_PRIFIX)
logging.debug("Prices router (/prices) initialised")


app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def start_scheduler():
    database = SessionLocal()
    if database.query(NewsArticle).count() == 0:
        # should change into simple factory pattern
        logging.info("No news present in the database. Fetching latest news.")
        get_new_info()
    database.close()
    Scheduler.add_job(get_new_info, "interval", minutes=100)
    Scheduler.start()
    logging.debug("Background scheduler started.")
    logging.info("PriceTracker backend has started.")


@app.on_event("shutdown")
def shutdown_scheduler():
    Scheduler.shutdown()
    logging.debug("Background scheduler shutdown.")

@app.get("/sentry-debug")
async def trigger_error():
    try:
        division_by_zero = 1 / 0
    except ZeroDivisionError as e:
        capture_exception(e)
        logging.error(f"You attempted to divide by zero!: {e}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while performing division by zero"
        )
    
