import asyncio
import os.path
from uuid import uuid4

import aiofiles

from models.customer import CustomerData
from resources import logger

TEMPLATE_FILE = os.path.join('data', 'template.txt')


class Agent:
    template_content = None

    def __init__(self):
        logger.debug(f"Initialized Agent")
        self.load_template()

    def load_template(self):
        """
        Load the base template content from the template file
        """
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                self.template_content = f.read()
                logger.debug(f"Loaded template from {TEMPLATE_FILE}")
        except FileNotFoundError:
            logger.error(f"Template file {TEMPLATE_FILE} not found.")
            raise

    async def create_script(self, customer_data: CustomerData, **kwargs):
        """
        Create a script for the given customer data and save it to a file
        :param customer_data:
        :param kwargs:
        :return:
        """
        script = self.template_content.format(
            customer_name=customer_data.customer_name,
            company=customer_data.company,
            **kwargs
        )
        script_id = f"Script_{uuid4()}"

        scripts_dir = os.path.join('data', 'scripts')
        os.makedirs(scripts_dir, exist_ok=True)

        filename = os.path.join(scripts_dir, f"{script_id}.txt")
        async with aiofiles.open(filename, 'w') as f:
            await f.write(script)
        logger.info(f"Script created and saved for {customer_data} with ID {script_id}")
        return script_id

    @staticmethod
    async def call_api(customer_data: CustomerData, script_id: str, **kwargs):
        """
        Simulate calling the /call API with the given parameters with the given customer data and script ID
        :param customer_data:
        :param script_id:
        :param kwargs:
        :return:
        """
        logger.info(f"Starting API call for {customer_data.customer_name}")
        logger.debug(
            f"API Call Parameters: Script ID: {script_id}, Company: {customer_data.company}, Additional Args: {kwargs}")
        await asyncio.sleep(5)  # Simulate an API call
        logger.info(f"API call completed for {customer_data.customer_name}")
