# Validate-LMA
본 job은 기존에 LMA 배포가 완료된 k8s cluster에 대해, LMA가 정상 작동하는지 확인하는 테스트 잡이다.

## Job Parameter
* KUBERNETES_CLUSTER_IP: 테스트의 대상이 될 kubernetes cluster의 API endpoint IP

## Test Scenario
각 모듈별로 아래의 순서대로 테스트가 진행되며 실패할 시 에러 메세지와 함께 젠킨스 잡이 종료된다.

### Elasticsearch, Fluentbit and Kibana
Elasticsearch, Fluentbit 그리고 Kibana를 축약하여 `efk`라고 칭한다.
EFK가 정상 동작하는지 확인하기 위해 다음과 같은 테스트를 한다.
1. Elasticsearch Index가 생성됐는지 API를 통한 확인
2. Elasticsearch Index의 Document가 정상적으로 쌓이는지 API를 통한 확인
3. Kibana의 Index Pattern Create, Delete API를 통한 동작 테스트

### Prometheus and exporters.
TACO LMA를 설치하면 다음과 같은 챠트들이 기본으로 배포된다.
* Prometheus Server류
  * prometheus
  * prometheus-fed-master
  * thanos
* Exporter 류
  * prometheus-node-exporter
  * kube-state-metrics
  * kubernetes-event-exporter 
* 기본 컴포넌트
  * prometheus-operator
  * prometheus-process-exporter
  * prometheus-pushgateway
  * prometheus-adapter

다단계의 Pipeline을 거쳐서 궁극적으로는 fed-master나 thnos를 통해 그 값을 조회하게 되면 모든 컴포넌트가 잘 설치되었음을 확인할 수 있다.
추가적으로 위에서 보여지는 내용외에도 Prometheus는 내부적으로 준비된 다양한 데이터 소스에서 매트릭을 수집하게 되는데 이를 나열하면 다음과 같다.
다만 이 내용은 현재(2021.02)의 형상을 담고 있으므로 지속적으로 prometheus 진영과 Ha.nu의 LMA 변경사항을 반영해 줘야한다.

Scrap Target
* kubernetes
* kube-state-metrics
* lma-coredns
* lma-kube-controller-manager
* lma-kube-proxy
* lma-kube-scheduler
* lma-prometheus
* process-exporter
* prometheus-node-exporter
* prometheus-operator-kube-p-kubelet
* prometheus-operator-kube-p-operator
* prometheus-pushgateway
* prometheus-test-kube-prome-kubelet

각 Target의 up 메트릭을 조회하여 합을 구한것이 0보다 크다면 다음의 내역을 확인할 수 있다.
1. target별 exporter가 정상동작 중
2. exporter의 데이터를 prometheus 서버에서 잘 수취하고 저장함
3. prometheus 서버에 대한 promQL이 잘 처리되어 정확한 동작을 수행함


### Grafana
추가적으로 prometheus를 소스로 연결하는 Grafana에 대한 처리를 포함해야 한다. (다음 중 하나로 결정해 수행해야 함)
* 200 OK.를 확인
* DataSource를 통해 grafana와 prometheus가 잘 연결되어 있음을 확인
* 같이 올려진 dashboard가 잘 적용되어 있으며 데이터도 잘 가져온다. (현실적으로 힘들어 보임)


