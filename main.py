from prometheus_client import Counter, Gauge, Summary, Histogram


def main():
    nb_of_requests_counter = Counter(
        name='nb_of_requests',
        documentation='number of requests made to the app',
        labelnames=['method', 'endpoint'],
    )
    nb_of_requests_counter.labels(method='GET', endpoint='/').inc()

    with nb_of_requests_counter.labels(method='GET', endpoint='/').count_exceptions():
        raise TypeError


if __name__ == "__main__":
    main()
