import json
from flask import request, jsonify
from app import webserver
from .helpers import make_job
from .backend import *
from .server_logging import logger


# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):

    job_id = int(job_id)
    with webserver.job_counter_lock:
        current_job_counter = webserver.job_counter

    if job_id <= current_job_counter:
        if webserver.tasks_runner.job_done(job_id):
            # The job is done
            # Return the results
            file_path = f"results/{job_id}.json"

            with open(file_path) as file:
                res = json.load(file)
                return jsonify({
                    'status': 'done',
                    'data': res
                })
        else:
            return jsonify({'status': 'running'})
    else:
        return jsonify({
            "status": "error",
            "reason": "Invalid job_id"
        })


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    def wrapper(data):
        question = data['question']
        mean = states_mean(question)
        return mean

    data = request.json

    logger.info("States mean request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for states mean request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    def wrapper(data):
        question = data['question']
        state = data['state']
        mean = state_mean(question, state)
        return mean

    data = request.json

    logger.info("State mean request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for state mean request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    def wrapper(data):
        question = data['question']
        res = best5(question)
        return res

    data = request.json

    logger.info("Best5 request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for best5 request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    def wrapper(data):
        question = data['question']
        res = worst5(question)
        return res

    data = request.json

    logger.info("Worst5 request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for worst5 request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    def wrapper(data):
        question = data['question']
        mean = global_mean(question)
        return mean

    data = request.json

    logger.info("Global mean request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for global mean request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    def wrapper(data):
        question = data['question']
        diff = diff_from_mean(question)
        return diff

    data = request.json

    logger.info("Diff from mean request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for diff from mean request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    def wrapper(data):
        question = data['question']
        state = data['state']
        diff = state_diff_from_mean(question, state)
        return diff

    data = request.json

    logger.info("State diff from mean request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for state diff from mean request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    def wrapper(data):
        question = data['question']
        mean = mean_by_category(question)
        return mean

    data = request.json

    logger.info("Mean by category request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for mean by category request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    def wrapper(data):
        question = data['question']
        state = data['state']
        mean = state_mean_by_category(question, state)
        return mean

    data = request.json

    logger.info("State mean by category request for %s", data)

    job_id = make_job(wrapper, data)

    logger.info("Job id for state mean by category request is %d", job_id)

    return jsonify({
        "job_id": job_id
    })

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    webserver.tasks_runner.shutdown()
    return jsonify({
        "status": "shutting down"
    })


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    with webserver.job_counter_lock:
        no_jobs = webserver.job_counter
    jobs = webserver.tasks_runner.jobs_event_list

    data = []

    for job_id in range(1, no_jobs):
        status = "done" if jobs[job_id].is_set() else "running"
        data.append({f"job_id_{job_id}": status})

    return jsonify({
        "status": "done",
        "data": data
    })


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    with webserver.job_counter_lock:
        no_jobs = webserver.job_counter
    jobs = webserver.tasks_runner.jobs_event_list

    remaining_jobs = 0
    for job_no in range(1, no_jobs):
        if not jobs[job_no].is_set():
            remaining_jobs += 1
    return jsonify({
        "remaining_jobs": remaining_jobs
    })
