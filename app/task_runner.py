from queue import Queue, Empty
from threading import Thread, Event
import json
import os


class ThreadPool:

    def job_done(self, job_id: int):
        """ Checks if the server finished processing the task with the given job id """
        return self.jobs_event_list[job_id].is_set()

    def shutdown(self):
        """ Shuts down the server by not accepting any more tasks 
            and waiting for the remaining tasks to finish 
        """
        self.shutdown_.set()
        for task_runner in self.task_runners:
            task_runner.join()

    def __init__(self):
        # Determine the number of thread pool working threads
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()

        self.task_queue = Queue()
        self.jobs_event_list = {}
        self.shutdown_ = Event()

        self.task_runners = [
            TaskRunner(
                self.task_queue,
                self.jobs_event_list,
                self.shutdown_) for _ in range(
                self.num_threads)]
        # Start the worker threads
        for task_runner in self.task_runners:
            task_runner.start()

    def submit_task(self, task: tuple):
        """ Submits a task to the thread pool """
        if not self.shutdown_.is_set():
            # Place the task in the queue to be processed by the worker threads
            self.task_queue.put(task)
            (_, _, job_id) = task
            self.jobs_event_list[job_id] = Event()


class TaskRunner(Thread):
    def __init__(
            self,
            task_queue: Queue,
            jobs_event_list: dict,
            shutdown: Event):
        super().__init__()
        self.task_queue = task_queue
        self.jobs_event_list = jobs_event_list
        self.shutdown = shutdown

    def run(self):
        while True:
            try:
                # Get a task from the queue, if any
                job = self.task_queue.get(block=False)
                function, data, job_id = job
                # Execute the task
                res = function(data)
                # Save the result json file
                with open(f"results/{job_id}.json", 'w') as json_file:
                    json.dump(res, json_file)
                # Task is done so the result may be retrieved
                self.jobs_event_list[job_id].set()
            except Empty:
                if self.shutdown.is_set():
                    break
