import time
from ..schemas.utility import *

class UtilityAPI:
    endpoint_get_job = "/object/job/{id}"

    # Initializes the UtilityAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Polls a job status until completion with exponential backoff and timeout handling
    def wait_for_job(self, job_id, poll_interval=2, timeout=300, max_interval=30, backoff=1.5) -> JobResponse:
        start_time = time.monotonic() # Stores intial start time

        interval = poll_interval

        # Triggers indefinitely so that job status is constantly polled
        while True:
            # Invoke the API call
            response = self.get_job_details(job_id)

            # Checks if job has been executed yet or not
            if response.finished is not None:
                return response # Returns the response once job has been executed

            # Determines if the method has been running past the specified timeout amount
            elapsed = time.monotonic() - start_time
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Job {job_id} did not finish within {timeout} seconds."
                )
            
            # Sleeps for the calculated interval
            time.sleep(interval)

            # Calculates new exponentially increasing interval (max_interval is enforced so that too long is not waited)
            interval = min(interval * backoff, max_interval)
            
    # Retrieves details and status for a specific job by its ID
    def get_job_details(self, job_id) -> JobResponse:
        
        return JobResponse(**self.client.safe_get(self.endpoint_get_job.format(id=job_id)))