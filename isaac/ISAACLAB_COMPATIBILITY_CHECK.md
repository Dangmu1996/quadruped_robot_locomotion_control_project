# Isaac Lab ↔ Isaac Sim 5.1.0 호환성 확인 체크

## 목적
이 문서는 현재 설치된 **Isaac Sim 5.1.0**에 맞는 **Isaac Lab 버전/branch/tag**를 확인하고,
설치 전에 꼬이기 쉬운 부분을 미리 점검하기 위한 체크 문서다.

---

## 1. 가장 먼저 확인할 것

- [ ] Isaac Lab 공식 문서에서 **Isaac Sim 5.1.0 지원 여부** 확인
- [ ] 지원된다면 어떤 **branch / tag / release**를 써야 하는지 확인
- [ ] 지원되지 않는다면 권장 Isaac Sim 버전이 무엇인지 확인

메모:
- Isaac 계열은 버전 불일치가 나면 설치는 돼도 예제 실행에서 깨질 수 있음
- 따라서 "최신 Isaac Lab"을 그냥 받는 방식은 피하는 게 좋음

---

## 2. 확인해야 할 핵심 정보

### A. 버전 매핑
- [ ] Isaac Sim 5.1.0 ↔ Isaac Lab 어떤 버전이 대응되는지 확인
- [ ] release note / installation guide / README에 명시되어 있는지 확인
- [ ] branch 이름이 `main`이 아니라 특정 release branch인지 확인

### B. Python 버전
- [ ] Isaac Sim 5.1.0이 요구하는 Python 버전 확인
- [ ] Isaac Lab이 요구하는 Python 버전 확인
- [ ] 두 버전이 충돌하지 않는지 확인

### C. OS / GPU / 드라이버
- [ ] Ubuntu 버전 요구사항 확인
- [ ] NVIDIA driver 요구사항 확인
- [ ] CUDA 관련 요구사항이 있는지 확인

### D. 설치 방식
- [ ] pip / editable install / script-based install 중 어떤 방식인지 확인
- [ ] Isaac Sim 경로를 직접 지정해야 하는지 확인
- [ ] environment variable 설정이 필요한지 확인

---

## 3. 설치 전에 확인할 질문

- [ ] Isaac Lab은 현재 설치된 Isaac Sim 폴더를 직접 참조하는 구조인가?
- [ ] 별도 conda / venv 환경이 필요한가?
- [ ] `python.sh`를 통해 실행해야 하는가?
- [ ] 예제 실행은 GUI 기반인지 headless도 가능한지?
- [ ] quadruped 관련 예제가 기본 포함되어 있는지?

---

## 4. 설치 후 최소 성공 기준

호환 버전이 맞고 설치가 잘 되었다고 보기 위한 최소 기준:

- [ ] Isaac Lab import 성공
- [ ] 기본 예제 하나 실행 성공
- [ ] quadruped 관련 env/task 로드 성공
- [ ] reset / step / render 동작 확인
- [ ] 에러 없이 한 번 종료 후 재실행 가능

---

## 5. quadruped 연구 관점에서 추가 확인할 것

- [ ] 기본 quadruped robot asset이 있는가
- [ ] terrain randomization 또는 rough terrain 예제가 있는가
- [ ] depth / lidar / camera sensor 연결 예제가 있는가
- [ ] observation에 terrain/perception 관련 항목을 넣을 수 있는 구조인가
- [ ] 나중에 elevation mapping용 point cloud / pose 데이터를 뽑기 쉬운가

---

## 6. 실패 시 흔한 원인 메모

체크할 문제들:
- [ ] Isaac Sim 버전과 Isaac Lab branch 불일치
- [ ] Python 버전 불일치
- [ ] 의존성 패키지 버전 충돌
- [ ] 실행 경로 문제
- [ ] environment variable 누락
- [ ] GPU / driver 문제

---

## 7. 권장 진행 순서

1. 공식 문서에서 **Isaac Sim 5.1.0 대응 Isaac Lab 버전 확인**
2. 설치 branch/tag 확정
3. Python/OS/GPU 요구사항 확인
4. 설치 전용 디렉토리 결정 (`3D_Navigation_project/isaaclab/` 또는 별도 repo)
5. 설치
6. 기본 예제 실행
7. quadruped 예제 확인
8. sensor / terrain / data extraction 가능 여부 확인

---

## 8. 진행 메모

- 현재 상태: Isaac Sim 5.1.0 동작 확인 완료
- 다음 목표: Isaac Lab의 정확한 호환 버전 확인
- 최종 목표: quadruped + terrain + sensor + elevation mapping / locomotion 연구로 확장
