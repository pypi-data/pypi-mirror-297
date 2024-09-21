"""Main module of the project for starting the agent."""

import asyncio

from loguru import logger

from vantage_agent.scheduler import init_scheduler, shut_down_scheduler
from vantage_agent.sentry import init_sentry


def main():
    """Start the agent by initiating the scheduler."""
    logger.info("Starting the Vantage Agent")
    init_sentry()

    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scheduler = init_scheduler()
            loop.run_until_complete()
        except (KeyboardInterrupt, SystemExit):  # pragma: no cover
            logger.info("Shutting down the Vantage Agent")
            shut_down_scheduler(scheduler)  # pragma: no cover
        else:
            continue
        finally:
            loop.close()


if __name__ == "__main__":
    main()  # pragma: no cover
