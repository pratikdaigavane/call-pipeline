import asyncio
import os

from models.customer import CustomerData
from processors.agent import Agent
from resources.scheduler import Scheduler


async def main():
    agent = Agent()
    scheduler = Scheduler()

    # Start the scheduler
    scheduler.start()

    async for customer_data in CustomerData.iterate_csv(os.path.join('data', 'data.csv')):
        # Create script for the customer
        script_id = await agent.create_script(customer_data)

        # Schedule the API call
        scheduler.schedule_agent_call(agent.call_api, args=(customer_data, script_id), trigger='interval', seconds=10)
        # Can also be scheduled for a specific date and time
        # scheduler.schedule_agent_call(agent.call_api, args=(customer_data, script_id), trigger='date', run_date='2021-08-01 00:00:00')

    # Run indefinitely to allow scheduled jobs to execute
    await scheduler.run_forever()


if __name__ == '__main__':
    asyncio.run(main())
