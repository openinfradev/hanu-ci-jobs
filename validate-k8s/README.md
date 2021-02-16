# Validate-k8s 
본 job은 기존에 배포가 완료된 k8s cluster에 대해, sonobuoy라는 테스트 툴을 사용하여 일련을 테스트들을 수행함으로써 클러스터가 정상적으로 동작하는지 검증하는 job이다. 

## Job Parameter
* SONOBUOY_VERSION: sonobuoy version (default: latest)
* SONOBUOY_MODE: test mode를 선택할 수 있으며 mode 종류는 다음과 같다.
  * custom: 미리 정의된 10 여가지의 주요 테스트를 수행 ('quick'과 'non-disruptive-conformance'의 중간 정도의 커버리지를 가짐. Default mode)
  * quick: pod를 생성하고 삭제하는 등 매우 간단한 single test를 수행.
  * non-disruptive-conformance: 클러스터 내의 다른 워크로드를 방해하지 않는 범위에서, Conformance(적합성)로 표시된 모든 테스트를 실행.
  * certified-conformance: 모든 적합성 테스트를 실행하며 Certified Kubernetes Conformance Program을 신청할 때 사용되는 모드이다. 이러한 테스트 중 일부는 클러스터 내의 다른 워크로드에 지장을 줄 수 있으므로 주의가 필요하다.
* KUBERNETES_CLUSTER_IP: 테스트의 대상이 될 kubernetes cluster의 API endpoint IP

## Test Result
테스트가 완료된 후 Jenkins console 상에서 다음과 같이 결과를 확인할 수 있다.
테스트 통계를 요약해서 보여주며, 실패한 케이스에 대해 상세로그를 표시해준다.
아래 예시의 경우는, 실제 테스트 케이스 수행 이전에 사전 체크에서 실패하여 total case 숫자가 1로 표시되어 있으며, 실제로는 더 큰 수치가 표시될 수 있다.
```
Plugin: e2e
Status: failed
Total: 1
Passed: 0
Failed: 1
Skipped: 0

Failed tests:
BeforeSuite

Plugin: systemd-logs
Status: passed
Total: 1
Passed: 1
Failed: 0
Skipped: 0
{
  "failure": "_output/dockerized/go/src/k8s.io/kubernetes/test/e2e/e2e.go:71\nFeb 10 07:01:28.601: Error waiting for all pods to be running and ready: 1 / 12 pods in namespace \"kube-system\" are NOT in RUNNING and READY state in 10m0s\nPOD                    NODE PHASE   GRACE CONDITIONS\ncoredns-dff8fc7d-765qt      Pending       [{Type:PodScheduled Status:False LastProbeTime:0001-01-01 00:00:00 +0000 UTC LastTransitionTime:2021-02-09 07:28:57 +0000 UTC Reason:Unschedulable Message:0/1 nodes are available: 1 node(s) didn't match pod affinity/anti-affinity, 1 node(s) didn't satisfy existing pods anti-affinity rules.}]\n\n_output/dockerized/go/src/k8s.io/kubernetes/test/e2e/e2e.go:279"
}
```
