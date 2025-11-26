from app import webserver


def make_job(function, data):
    """
        Submits a job to the thread pool and returns the job id.
    """

    with webserver.job_counter_lock:
        job_id = webserver.job_counter
        webserver.job_counter += 1

    webserver.tasks_runner.submit_task((function, data, job_id))

    return job_id
