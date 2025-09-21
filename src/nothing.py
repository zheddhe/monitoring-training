# import time
from prometheus_client import Counter, Info, CollectorRegistry, push_to_gateway

# the address of the Push Gateway
push_gateway_address = 'http://localhost:9091'

# creating a registry
collector = CollectorRegistry()

# creating an info metric
info = Info(
    name='name_of_the_script',
    documentation='documentation of the script',
    registry=collector
)
info.info({'version': '0.1', 'author': 'datascientest'})

# creating a counter to count iteration
# but it could count exceptions, measure time,...
counter = Counter(
    name='iterations',
    documentation='a counter used to record the starting time of the job',
    labelnames=['job'],
    registry=collector)

for i in range(10):
    # incrementing counter
    counter.labels(job="my_python_script").inc()

    # sleeping for 1 second
    # time.sleep(1)
    print(10 - i - 1, 's to sleep remaining...')

push_to_gateway(gateway=push_gateway_address, job="my_python_script", registry=collector)
