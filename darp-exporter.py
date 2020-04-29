from prometheus_client import start_http_server, Summary, Histogram, REGISTRY, Metric
import time
import json
import requests

genesis_url = 'http://13.48.248.81:65013/config'
class DarpCollector(object):
    def collect(self):
        c = Metric('darp_owl', 'Help text', 'summary')
        response = json.loads(requests.get(genesis_url).content.decode('UTF-8'))
        print(response['pulses'])
        owl_values = {}
        for darp_host in response['pulses']:
            print(darp_host.split(':')[0])
            print(response['pulses'][darp_host])
            owls = response['pulses'][darp_host]['owls'].split(',')
            for owl in owls:
                owl_values[owl.split('=')[0]] = owl.split('=')[1]
                c.add_sample('darp_owl', value=owl.split('=')[1], labels={'darp_host': darp_host, 'dest_host': owl.split('=')[0]})
        yield c

REGISTRY.register(DarpCollector())
def main():
    start_http_server(18000)
    while True:
        time.sleep(10)

main()
