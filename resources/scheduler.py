import asyncio
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from resources import logger


class Scheduler:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def schedule_agent_call(self, func: Any, *args, **kwargs):
        # Schedule the agent's call_api method
        logger.debug(f"Scheduling {func.__name__} with args: {args}, kwargs: {kwargs}")
        self.scheduler.add_job(func, *args, **kwargs)

    def start(self):
        self.scheduler.start()
        logger.info("Scheduler started. Waiting for scheduled tasks...")

    @staticmethod
    async def run_forever():
        """
        Keep the script running so that scheduled jobs can execute
        """
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            pass
