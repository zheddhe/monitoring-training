from prometheus_client import Counter, Gauge, Summary, Histogram, Info
from prometheus_client import generate_latest, CollectorRegistry
from prometheus_client import REGISTRY
import random


def main():

    collector = CollectorRegistry()

    # test compteur (counter)
    nb_of_requests_counter = Counter(
        name='nb_of_requests',
        documentation='number of requests made to the app',
        labelnames=['method', 'endpoint'],
        registry=collector,
    )
    nb_of_requests_counter.labels(method='GET', endpoint='/').inc()
    try:
        with nb_of_requests_counter.labels(method='GET', endpoint='/').count_exceptions():
            raise TypeError
    except TypeError:
        print("une exception levée manuellement")

    # test jauge (gauge)
    nb_of_active_connections_gauge = Gauge(
        name="nb_active_connections",
        documentation="number of active connections at a given time",
        labelnames=['authenticated'],
        registry=collector,
    )
    nb_of_active_connections_gauge.labels(authenticated='false').dec(1.2)
    nb_of_active_connections_gauge.labels(authenticated='false').inc(100)

    requests_duration_summary = Summary(
        name='requests_duration_summary',
        documentation='duration of the requests',
        labelnames=['method', 'endpoint'],
        registry=collector
    )
    for i in range(100):
        requests_duration_summary.labels(
            method='GET', endpoint='/'
        ).observe(random.uniform(0, 100))

    requests_duration_histogram = Histogram(
        name='requests_duration_histogram',
        documentation='requests duration presented as a histogram',
        labelnames=['method', 'endpoint'],
        buckets=[0, .01, .5, .8, 1., 1.5, 2],
        registry=collector,
    )
    for i in range(100):
        requests_duration_histogram.labels(
            method='GET', endpoint='/'
        ).observe(random.uniform(0, 1) * 2)

    service_info = Info(
        name='service_info',
        documentation='information on the requests service',
        registry=collector,
    )
    service_info.info({'author': 'datascientest'})

    print(generate_latest(collector).decode('utf-8'))

    for metric in REGISTRY.collect():
        print(metric.name)

    print(generate_latest().decode('utf-8'))


if __name__ == "__main__":
    main()
