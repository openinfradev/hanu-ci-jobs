#!/usr/bin/python
import requests,time,sys,getopt

# url = "http://192.168.5.61:30008/api/v1/query"
timeout=600
CHECK_INTERVAL=30
targets = ["kubernetes",
    "kube-state-metrics",
    "lma-coredns",
    "lma-kube-controller-manager",
    "lma-kube-proxy",
    "lma-kube-scheduler",
    "lma-prometheus",
    "process-exporter",
    "prometheus-node-exporter",
    "prometheus-operator-kube-p-kubelet",
    "prometheus-operator-kube-p-operator",
    "prometheus-pushgateway"]


h = {
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

def check_up(url, svc):
  params = {
    "query":"sum(up{service='"+svc+"'})"
  }

  r = requests.get(url, headers=h, params=params).json()


  if (r["status"]!="success"):
    return False

  results = r['data']['result']

  print(svc, results)
  try:
    count = int('{value[1]}'.format(**results[0]))
    if(count==0):
        return False
    
    return True
  except IndexError:
    return False


def printhelp():
    print('Usage: check_prometheus.py -p PROMETHEUS_SERVER [-t TIMEOUT]')

def main(argv):
  try:
    opts, args = getopt.getopt(argv,"hp:t:",["prometheus=","timeout="])
  except getopt.GetoptError:
    printhelp()
    sys.exit(-1)
  
  url = "http://127.0.0.1:30008/api/v1/query"
  for opt, arg in opts:
    if opt == '-h':
      printhelp()
      sys.exit(0)
    elif opt in ("-p", "--prometheus"):
      url = "http://{}/api/v1/query".format(arg)     
    elif opt in ("-t", "--timeout"):
      timeout = int(arg)

  print(url)
  while targets:
    checked=[]
    for target in targets:
      if check_up(url, target):
        checked.append(target)

    print(checked, "are checked.")

    for target in checked:
      targets.remove(target)

    print(targets, "are not checked. Sleeping for",CHECK_INTERVAL,". Timeout(", timeout, ") is left before terminate with fail.")
    time.sleep(CHECK_INTERVAL)
    timeout = timeout-CHECK_INTERVAL
    if timeout<0:
      sys.exit(targets, "are not checked. (finished with fail)")

if __name__ == "__main__":
  main(sys.argv[1:])