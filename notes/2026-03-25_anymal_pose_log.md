# 2026-03-25 ANYmal pose/state 확인 로그

## 오늘 한 일
오늘은 Isaac Sim에서 실행되던 ANYmal standalone example을 기반으로,
프로젝트 스크립트 안에서 quadruped의 pose/state를 직접 읽는 단계까지 진행했다.

---

## 사용한 스크립트
- 프로젝트 스크립트 경로:
  - `/home/dangmu/3D_Navigation_project/scripts/anymal_pose_test.py`

기존 standalone example을 바탕으로,
`on_physics_step()` 내부의 정상 simulation step 구간(`else`)에서
ANYmal의 상태를 주기적으로 출력하도록 수정했다.

---

## 오늘 적용한 핵심 수정
### 1. 출력 카운터 변수 추가
- `self.print_count_ = 0`

### 2. physics callback 내 주기적 출력
- `else:` 구간에서 `self._anymal.forward(...)` 이후
- 카운터를 증가시키고
- 30 step마다 robot state를 출력하도록 구성

### 3. 출력 함수 분리
- `printRobotState()` 함수를 따로 만들어
  - base position
  - base orientation
  - joint positions
을 출력하도록 구성

---

## 현재 코드 구조 해석
이 구조가 적절한 이유는 다음과 같다.

- keyboard subscribe는 이벤트 처리용이라 pose 관찰 루프에 적합하지 않음
- robot state는 simulation이 정상 step을 밟는 구간에서 읽는 것이 자연스러움
- 따라서 `on_physics_step()`의 `else` 부분에서 출력하는 것이 가장 적절함
- 출력 로직을 별도 함수로 분리해서 나중에 file logging / sensor state 추가 / 데이터 저장으로 확장하기 쉬움

---

## 오늘 확인된 것
- ANYmal standalone example 기반 프로젝트 스크립트가 정상 실행됨
- simulation loop 안에서 quadruped의 state를 읽을 수 있음
- 최소한 다음 데이터 접근이 가능함:
  - world pose
  - orientation
  - joint positions

즉,
오늘 기준으로는 **quadruped pose/state extraction의 첫 번째 성공**이라고 볼 수 있다.

---

## 의미
이 단계는 단순히 예제를 실행한 것이 아니라,
이제부터 Isaac Sim 안에서
- robot pose
- 이후 sensor data
를 실제 프로젝트 코드에서 읽어오는 데이터 파이프라인을 열기 시작했다는 의미가 있다.

특히 elevation mapping 관점에서 보면,
오늘 확인한 robot pose는 나중에 필요한 핵심 입력 중 하나다.

---

## 다음 단계 후보
다음에는 아래 중 하나로 자연스럽게 이어질 수 있다.

1. base velocity까지 읽어보기
2. 현재 모델에 달린 센서 데이터(depth / LiDAR 계열) 접근 확인
3. pose를 print가 아니라 파일/구조화된 logger 형태로 저장하기

현재 우선순위로 보면,
다음은 **센서 데이터 읽기** 쪽으로 넘어가는 것이 가장 자연스럽다.
