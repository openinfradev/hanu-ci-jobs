# Validate-k8s 
본 job은 기존에 LMA 배포가 완료된 k8s cluster에 대해, LMA가 정상 작동하는지 확인하는 테스트 잡이다.

## Job Parameter
* KUBERNETES_CLUSTER_IP: 테스트의 대상이 될 kubernetes cluster의 API endpoint IP

## Test Scenario
### Elasticsearch, Fluentbit and Kibana
Elasticsearch, Fluentbit 그리고 Kibana를 축약하여 `efk`라고 칭한다.
EFK가 정상 동작하는지 확인하기 위해 다음과 같은 테스트를 한다.
1. Elasticsearch Index가 생성됐는지 API를 통한 확인
2. Elasticsearch Index의 Document가 정상적으로 쌓이는지 API를 통한 확인
3. Kibana의 Index Pattern Create, Delete API를 통한 동작 테스트

만약, 테스트가 실패할 시 에러 메세지와 함께 젠킨스 잡이 종료된다.