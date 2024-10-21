from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterable

import aiofiles

from resources import logger


@dataclass
class CustomerData:
    customer_name: str
    company: str

    @classmethod
    async def iterate_csv(cls, csv_file) -> AsyncIterable[CustomerData]:
        try:
            async with aiofiles.open(csv_file, 'r') as f:
                header_line = await f.readline()
                headers = header_line.strip().split(',')
                async for line in f:
                    values = line.strip().split(',')
                    customer_data = CustomerData(**dict(zip(headers, values)))
                    yield customer_data
        except FileNotFoundError:
            logger.error(f"CSV file {csv_file} not found.")
            raise
