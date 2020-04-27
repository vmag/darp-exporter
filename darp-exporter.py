from prometheus_client import start_http_server, Summary, Histogram, REGISTRY, Metric
import time

class DarpCollector(object):
    def collect(self):
        c = Metric('my_counter_total', 'Help text', 'summary')
        c.add_sample('svc_requests_duration_seconds_count', value=11, labels={})
        yield c

REGISTRY.register(DarpCollector())
def main():
    start_http_server(18000)
    while True:
        time.sleep(10)

main()
