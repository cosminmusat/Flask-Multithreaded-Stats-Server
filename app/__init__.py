from threading import Lock
import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor(
    "./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1
webserver.job_counter_lock = Lock()

os.makedirs("results", exist_ok=True)

from app import routes
