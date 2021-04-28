kubectl get svc -n istio-gateway -o=jsonpath='{.items[0].spec.ports[?(@.port==80)].nodePort}'
