import random
import time
from flask import make_response
from flask import request
from flask import Flask
from prometheus_client import Counter, Histogram, CollectorRegistry
from prometheus_client import generate_latest


# parameters of the app
address = '0.0.0.0'
port = 5000

# creating the app
app = Flask('my app')


# creating a route for the app
@app.route('/', methods=['GET'])
def index():
    # creating a start time to get the request duration
    start = time.time()
    # keeping the values for the labels:
    method_label = request.method
    endpoint_label = '/'
    # incrementing the Counter
    nb_of_requests_counter.labels(
        method=method_label, endpoint=endpoint_label
    ).inc()

    # creating a false waiting time to simulate actual work
    # waiting time set between 0 and 2s
    waitingTime = round(random.uniform(a=0, b=1) * 2, 3)

    # waiting
    time.sleep(waitingTime)

    # creating a stop time to get the request duration
    stop = time.time()
    duration_of_requests_histogram.labels(
        method=method_label, endpoint=endpoint_label
    ).observe(stop - start)

    return 'This request took {}s'.format(waitingTime)


@app.route('/my_metrics', methods=['GET'])
def my_metrics():
    # creating the text to display
    text_to_display = generate_latest(collector)
    # creating a response object
    response = make_response(text_to_display)
    # specifying response headers
    response.headers['Content-Type'] = 'text/plain'
    # returning the response
    return response


collector = CollectorRegistry()

nb_of_requests_counter = Counter(
    name='nb_of_requests',
    documentation='number of requests per method or per endpoint',
    labelnames=['method', 'endpoint'],
    registry=collector
)

duration_of_requests_histogram = Histogram(
    name='duration_of_requests',
    documentation='duration of requests per method or endpoint',
    labelnames=['method', 'endpoint'],
    registry=collector
)

if __name__ == '__main__':
    app.run(host=address, port=port)
