Mușat-Mare Cristian-Cosmin
332CD
Le Stats Sportif

task_runner.py:

    ThreadPool is essentialy composed of 3 elements and 3 important functions:
        - A task queue where tasks will be placed for worker threads to execute
        - A task dictionary of Events which will mark when a job is done by having called the set function
        The dictionary will have as keys ints signifying the job id.
        - An shutdown Event variable which will mark when shutdown is initiated by having called the set function
        - A list of TaskRunners which share all the above mentioned data with the Thread Pool

        - The job_done function has a job id as parameter and uses the task dictionary to check if a job 
        has been completed (checks with the is_set function)
        - The shutdown function sets the shutdown event and waits for the worker threads to finish
        - The submit_task function has a task as parameter in the form of a tuple which contains
        the function to execute, the necessary data and the job id for that specific task (in this order).
        This function adds the task to the task queue (no synchornization needed as Queue is synchronized internally)
        and also creates an Event object as value for the job id entry in the task dictionary.

    task_runner.py contains an additional class TaskRunner which represent the worker threads.
    TaskRunner features a function called run which extracts tasks from the task queue, when available, and executes them.
        - The get is non-blocking because otherwise it would block when there are no more tasks to execute, ultimately on server shutdown.
        This get can throw an Empty exception which is handled by checking if the shutdown Event is set.
        If yes then the thread will sieze execution by breaking out of the infinite loop, otherwise the loop is re-run.
        - As soon as a task in completed, the result is written in the corresponding json file with the name in <job_id>.json format and
        the Event in the task dictionary is set so the result can be collected through a GET request.

helpers.py:

    This file only contains the make_job function which takes a function and its data as parameters.
        - Firstly it determines a job id for the task that will be created. The job_counter is protected by a Lock in case of multiple
          requests done at the same time. Then it purely submits the task to the thread pool.

data_ingestor.py:

    - Reads the csv and creates a header dictionary which will have column names as keys and indices as values but also a variable rows
      which will store the remainder of the table (without the header).

routes.py:

    - get_response basically checks if job is done with the job_done function and if yes, then it gets the results.
    - The jobs, num_jobs and graceful_shutdown are handled by the server.
    - Each other api route contains a wrapper function with limited scope which will call the make_job function with the corresponding function
      in the backend as argument.

backend.py:

    - Implementation of server logic mainly making use of filters and dictionaries.
    - Boiler plate code was avoided by calling functions such as state_mean for states_mean.
    - The rest of the logic implementation is depicted in comments.

server_logging.py:

    - Implemented logging as requested. Info logging is done within the main api routes.
    









