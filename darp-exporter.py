from prometheus_client import start_http_server, Summary, Histogram, REGISTRY, Metric
import os
import time
import json
import requests

darp_host_list = {}
genesis_host = os.environ['GENESIS_HOST']
class DarpCollector(object):
    def collect(self):
        c = Metric('darp_owl', 'Help text', 'summary')
        response = json.loads(requests.get('http://'+genesis_host+'/config').content.decode('UTF-8'))
        for k in response['gSRlist']:
            darp_host_id = response['gSRlist'][k]
            darp_host_list[darp_host_id] = {}
            darp_host_list[darp_host_id]['hostname'] = k
            owl = response['pulses'][k]['owls'].split(',')
            owl_values = {}
            for a in owl:
                if '=' not in a:
                    owl_values[a] = '3000'
                    continue
                owl_values[a.split('=')[0]] = a.split('=')[1]
            darp_host_list[darp_host_id]['latency'] =  owl_values
        print(darp_host_list)
        for host in darp_host_list:
            for k in darp_host_list[host]['latency']:
                ll = darp_host_list[host]['latency'][k]
                c.add_sample('darp_owl', value=ll, labels={'darp_host': darp_host_list[host]['hostname'], 'dest_host': darp_host_list[k]['hostname']})
        yield c

REGISTRY.register(DarpCollector())
def main():
    start_http_server(18000)
    print('Started DARP Prometheus exporter')
    while True:
        time.sleep(10)

main()
