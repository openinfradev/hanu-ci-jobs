# buildCAPIImages

Cluster-API 노드를 위한 이미지 생성을 수행한다.

## Job Parameter
* UBUNTU_VERSION: 기본 Ubuntu 리눅스 버전을 지정한다, 예) 2004, 1804
* K8S_VERSION_MAJOR_MINOR: 사용하고자 하는 Kubernetes 버전의 Major.Minor를 지정한다, 예) 1.20
* K8S_VERSION_PATCH: 사용하고자 하는 Kubernetes 버전의 Patch 번호를 지정한다, 예) 2

## 참고
[image-builder](https://github.com/kubernetes-sigs/image-builder)를 사용하며 아래와 같은 변경 사항이 존재한다.
* Ubuntu에서 growroot를 initramfs가 아닌 cloud-init에서 구동
* Ubuntu의 systemd-resolved를 /etc/resolv.conf를 보존하는 모드로 사용 (https://wiki.archlinux.org/index.php/Systemd-resolved#DNS)
