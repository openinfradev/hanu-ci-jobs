# Validate-service-mesh
본 job은 기존에 배포가 완료된 service-mesh infra (istiod 및 ingressGateway)를 대상으로, sample app과 해당 app으로의 routing 설정을 위한 virtualService 자원을 생성하고 외부에서 실제로 ingress URL을 통해 정상적으로 접속이 되는지 검증하는 job이다. 

## Job Parameter
* KUBERNETES_CLUSTER_IP: 테스트의 대상이 될 kubernetes cluster의 API endpoint IP

## Test Logic
테스트는 다음의 명령을 수행하여 진행되며, 정상 접속이 되면 job이 pass되고, 접속이 실패할 경우 에러 메시지와 함께 job이 실패하게 된다.
```
curl -s -I -HHost:nginx.hanu.com http://${endpoint}:${ingressNodePort} | grep '200 OK'"
```

실패시 에러 메세지
```
Failed to connect to nginx service.
```
