# 2026-03-18 Isaac Sim 시작 로그

## 오늘 한 일
오늘은 본격적인 프로젝트 구현에 들어가기 전에,
Isaac Sim 환경에서 quadruped asset이 실제로 실행되는지 확인하는 단계까지 진행했다.

---

## 현재 기준 프로젝트 상태
- 메인 프로젝트 디렉토리: `/home/dangmu/3D_Navigation_project`
- Isaac Sim 설치 경로: `/home/dangmu/isaacsim`
- Isaac Sim 버전: **5.1.0 계열**
- Isaac Lab은 아직 설치 전이며, 호환성 조사 결과 현재 stable 기준으로는 **v2.3.2**를 우선 후보로 보기로 했다.

---

## 오늘 asset 선택 관련 정리
처음에는 Unitree Go2를 우선 후보로 생각했지만,
로컬 Isaac Sim 내부 검색 결과 Go2 asset은 바로 확인되지 않았다.

반면 ANYmal 관련 asset/example 흔적은 명확하게 확인되었다.
특히 아래 경로들이 확인되었다.

- `standalone_examples/api/isaacsim.robot.policy.examples/anymal_standalone.py`
- `exts/isaacsim.robot.policy.examples/.../robots/anymal.py`

또한 코드 상에서 다음 asset 경로가 사용되는 것을 확인했다.
- `/Isaac/Robots/ANYbotics/anymal_c/anymal_c.usd`

따라서 오늘은 빠르게 파이프라인을 열기 위해,
**Go2 대신 ANYmal을 사용해 먼저 시작하는 방향**으로 결정했다.

---

## 오늘 실행한 것
실행 명령:

```bash
cd /home/dangmu/isaacsim
./python.sh standalone_examples/api/isaacsim.robot.policy.examples/anymal_standalone.py
```

---

## 실행 결과
실행은 정상적으로 진행되었고,
로그상 다음과 같은 상태를 확인했다.

- `Simulation App Starting`
- `app ready`
- `Simulation App Startup Complete`

즉 Isaac Sim standalone example은 실제로 정상 기동되었다고 볼 수 있다.

---

## 로그에서 본 warning에 대한 해석
실행 중 deprecation warning, mesh warning, PhysX warning, performance warning 등이 보였지만,
현재 시점에서는 **재설치가 필요한 치명적 오류로 보지는 않기로 했다.**

해석:
- deprecated warning: 구버전 API/extension 사용 경고
- mesh warning: 일부 asset/렌더링 메타데이터 관련 경고 가능성
- physx warning: solver/iteration 관련 동작 경고
- performance warning: 내부 최적화 권고

현재 기준으로는:
- 실행 자체는 정상
- crash 없음
- example이 돌아감

따라서 **지금은 재설치보다 계속 진행하는 것이 맞다**고 판단했다.

---

## 오늘 기준 체크포인트
오늘 상태에서 확인해야 할 핵심 포인트를 정리하면 다음과 같다.

1. 로봇이 scene에 정상 spawn되었는가
2. simulation loop가 정상적으로 도는가
3. 센서가 실제로 부착되어 있는 위치를 파악할 수 있는가
4. terrain / world가 관찰 가능한 단순한 상태인가
5. fatal error 없이 실행이 유지되는가

현재 사용자가 직접 확인한 바에 따르면,
**일단 잘 돌아간다**는 점이 가장 중요하게 확인되었다.

---

## 센서 관련 현재 판단
현재 모델은 사용자가 원하던
"앞뒤에 라이다가 달린 최신 구성"과는 다를 수 있지만,
일단 quadruped + 센서가 있는 상태로 실행된다는 점이 중요하다.

현재 판단:
- 지금 센서 구성이 최종 목표와 달라도 괜찮음
- 우선은 시뮬레이션 데이터 흐름을 여는 것이 우선
- 이후 필요하면 앞/뒤 LiDAR 등 센서 구성을 추가 조정하면 됨

---

## 다음에 이어서 할 일
다음 단계는 아래 중 하나로 바로 이어질 수 있다.

1. ANYmal의 pose/state를 Python에서 읽는 최소 코드 확인
2. 현재 부착된 센서 데이터(depth/point cloud 계열)를 읽는 방법 확인
3. 이후 Go2 asset을 따로 붙일지, 계속 ANYmal로 갈지 다시 결정

현재 프로젝트 관점에서는,
**ANYmal로 먼저 pose + sensor 데이터 흐름을 잡는 것**이 가장 자연스러운 다음 단계다.
