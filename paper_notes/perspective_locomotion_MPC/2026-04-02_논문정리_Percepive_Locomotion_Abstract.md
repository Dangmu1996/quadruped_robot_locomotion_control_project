# 2026-04-02 논문정리 — Perceptive Locomotion through Nonlinear Model Predictive Control (Abstract)

## 오늘 읽은 범위
오늘은 `Perceptive Locomotion through Nonlinear Model Predictive Control` 논문의 **abstract**만 읽고,
이 논문이 현재 프로젝트 흐름에서 어떤 위치를 가지는지 정리했다.

---

## abstract 핵심 해석
### 1. 이 논문은 perception-only 논문이 아니다
이 논문은 단순히 terrain map을 만드는 논문이 아니라,
- perception
- planning
- control
을 모두 포함한 **통합 파이프라인**을 다룬다.

즉 최종 목적은 terrain 정보를 가지고 실제 quadruped가 rough terrain에서 동적으로 움직이게 만드는 것이다.

---

### 2. 핵심 아이디어는 terrain 정보를 optimization-friendly하게 바꾸는 것이다
abstract의 핵심 문장은 다음 흐름으로 정리된다.

- elevation map에서 terrain 정보를 얻고
- steppability classification, plane segmentation, signed distance field(SDF)를 미리 계산한 뒤
- foothold feasibility를 local convex inequality constraints로 근사하고
- 이를 online nonlinear MPC 안에 넣는다.

즉 이 논문은 단순 foothold selector라기보다,
**perception 결과를 MPC가 실시간으로 쓸 수 있는 제약 형태로 변환하는 논문**으로 이해하는 것이 맞다.

---

### 3. convex optimization으로 발 위치만 따로 고르는 논문은 아니다
처음에는 “convex optimization으로 cost minimum foothold를 찾는 논문”처럼 보일 수 있지만,
좀 더 정확히 보면 이 논문은
- terrain 정보를 convex한 feasible region으로 근사하고
- 발 위치를 포함한 전체 motion optimization을 nonlinear MPC 안에서 같이 푸는 구조
에 가깝다.

즉 핵심은
**foothold-only optimization**이 아니라
**constraint-embedded nonlinear MPC**이다.

---

### 4. 이전 elevation mapping 논문과 겹치는 부분이 많지만 역할은 다르다
이 논문에는
- elevation map
- steppability
- plane segmentation
- terrain preprocessing
같은 요소가 다시 등장해서,
이전 `Elevation Mapping for Locomotion and Navigation using GPU` 논문과 겹쳐 보인다.

하지만 역할은 다르다.

- 이전 논문:
  - terrain representation / preprocessing / map quality 자체가 중심
- 현재 논문:
  - 그 representation을 실제 MPC/control에 어떻게 넣는지가 중심

즉 재료는 겹치지만,
이번 논문은 **perception-to-control integration** 쪽 논문으로 보는 것이 맞다.

---

### 5. 프로젝트와의 연결
이 논문이 요구하는 구조는 대략 다음과 같다.

1. point cloud / pose / TF 입력 정리
2. elevation mapping
3. plane segmentation / steppability / SDF 같은 terrain preprocessing
4. convex foothold feasibility constraints 생성
5. nonlinear MPC
6. whole-body/reactive control

현재 프로젝트는 이 중에서
- Isaac Sim 센서 입력
- ROS2 point cloud
- URDF/TF 정리
같은 **입력 인프라 단계**를 쌓고 있는 중이라고 정리했다.

즉 지금까지 한 일은 이 논문의 앞단을 준비하는 작업으로 볼 수 있다.

---

## 오늘의 한 줄 정리
이 논문은 elevation map 기반 terrain 정보를 단순히 보는 데서 끝나는 것이 아니라,
그 정보를 **steppability / plane segmentation / SDF / convex foothold constraints**로 가공해
실시간 nonlinear MPC와 연결하는 **perceptive locomotion 통합 논문**이다.
