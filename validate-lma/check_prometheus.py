import requests, time, sys

url = "http://192.168.5.61:30008/api/v1/query"
TIMEOUT=600
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
        "prometheus-pushgateway",
        "prometheus-test-kube-prome-kubelet"]


h = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}
def check_up(svc):
    params = {
        "query":"sum(up{service='"+svc+"'})"
        # "query":"sum(up{service='prometheus-test-kube-prome-kubelet'})"
    }

    r = requests.get(url, headers=h, params=params).json()


    if (r["status"]!="success"):
        return False

    results = r['data']['result']

    count = int('{value[1]}'.format(**results[0]))
    if(count==0):
        return False
    
    return True

while targets:
    checked=[]
    for target in targets:
        if check_up(target):
            checked.append(target)

    print(checked, "are checked.")

    for target in checked:
        targets.remove(target)

    # print(len(targets))
    # if len(targets)<3: 
    #     sys.exit(0)
    print(targets, "are not checked. Timeout(", TIMEOUT, ") is left before terminate with fail.")
    time.sleep(CHECK_INTERVAL)
    TIMEOUT = TIMEOUT-CHECK_INTERVAL
    if TIMEOUT<0:
        sys.exit('My error message')
