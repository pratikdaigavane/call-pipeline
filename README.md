Full Problem Statement: [PROBLEM.md](PROBLEM.md)

### Architecture
1. Since the problem statement involves heavy use of I/O operations, `asyncio` is used as the concurrency pattern to handle I/O operations. As compared to `threading` or `multiprocessing`, `asyncio` is more efficient for this usecase.
2. [APScheduler](https://github.com/agronholm/apscheduler) is used to schedule tasks. It is currently configured to use local memory as the job store. This can be easily changed to use a persistent store like a database so that the jobs are not lost on service restart. The scheduler also runs on asyncio event loop.
3. Files are stored in the `data` directory. It has the following structure:
    - `data/`: Root directory
        - `data.csv`: CSV file containing customer data
        - `scripts/`: Directory to store generated scripts with customer data
        - `template.txt`: Base template for the script, with placeholders for customer data

### Flow
1. Instance of `Agent` and `Scheduler` class is created.
2. We then iterate over the rows in the CSV file and create a job for each row. This is done concurrently using `asyncio`. In `CustomerData.iterate_csv` method, `aiofiles` package reads the CSV file asynchronously line by line and yields the row. This is means that the file is not read into memory all at once and as soon as a row is read, it is processed (scheduled job created in this case).
3. For each row: 
    - A script is generated using the base template file and customer data.
    - A script id is assigned (UUID V4) and the script is saved in the `scripts` directory.
4. A job is scheduled using `APScheduler` to run at the specified time. The job is passed the script id, customer name, company and any additional kwargs. Currently for demonstration purposes, the job is scheduled to run 5 seconds but this can be easily changed to any time.
5. When the job runs, it makes a call to a dummy API endpoint with the script id, customer name, company and kwargs. The dummy API endpoint simulates an API call by waiting for 5 seconds.

### Running Local
1. Clone the repository
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the script: `python main.py`