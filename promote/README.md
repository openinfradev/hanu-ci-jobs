# Promote
본 job은 검증이 완료된 Hanu 제품군의 소스코드들을 대상으로 Version release 작업을 수행한다. 좀더 구체적으로는, 미리 정의된 repository들을 대상으로, 새로운 release branch에 코드를 push하고, version tagging까지 수행하게 된다.

## Job Parameter
* SRC_BRANCH: source branch (default: main)
* SRC_TAG: source tag
  * 일반적으로는 값을 넣을 필요가 없으며, 현재의 main 브랜치 대신 특정 버전으로부터 새로운 버전을 릴리즈할 때 사용한다.
* DST_BRANCH: destination branch
* DST_TAG: destination tag

## Example
현재 HANU 에서 사용하는 기본 versioning 정책을 참고하여 예를 들면 다음과 같이 job을 수행할 수 있다 
```
* SRC_BRANCH: main
* SRC_TAG:
* DST_BRANCH: release-v21.03
* DST_TAG: hanu-v21.03
```
