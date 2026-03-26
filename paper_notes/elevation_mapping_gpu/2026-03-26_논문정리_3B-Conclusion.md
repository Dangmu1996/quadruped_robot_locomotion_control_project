# 2026-03-26 논문정리 — III-B 이후 ~ Conclusion

## 오늘 읽은 범위
오늘은 `Elevation Mapping for Locomotion and Navigation using GPU` 논문의 후반부를 이어서 읽고 conclusion까지 마무리했다.

---

## 핵심 정리
### 1. traversability filter는 전체 파이프라인의 병목이다
- 다른 구성 요소들보다 traversability filter가 가장 많은 계산 시간을 사용한다.
- 따라서 이후 성능 최적화는 이 모듈 개선이 핵심 후보가 된다.
- 이 필터는 단순 geometry rule이 아니라 CNN 기반 terrain interpretation 모듈로 이해했다.

### 2. traversability는 terrain-only라기보다 robot-dependent한 성격이 강하다
- 같은 terrain이라도 로봇 형상, 크기, 동역학, controller 특성에 따라 traversability 의미가 달라진다.
- 따라서 이런 learned traversability 모델은 로봇이 바뀌면 그대로 쓰기 어렵고, 최소한 retuning 또는 retraining 가능성을 고려해야 한다.

### 3. sensor별 map update frequency 문맥은 전체 pipeline 기준으로 읽는 것이 자연스럽다
- Realsense filtered / raw / Bpearl 비교는 단순 height update만이 아니라 논문이 제시한 전체 map pipeline의 update frequency로 읽는 것이 자연스럽다.
- 앞 문맥에서 traversability filter가 포함된 feature별 processing time을 이미 분석했기 때문에, Table II도 실사용 pipeline 성능을 보여주는 맥락으로 이해했다.

### 4. navigation stack에서 map은 실제 planner input이다
- exploration planner가 mid-range target을 주고,
- local planner가 upper bound layer와 traversability layer를 사용해서 local path를 만든다.
- 즉 map은 단순 visualization이 아니라 planner input으로 직접 사용된다.

### 5. locomotion 쪽에서도 map이 controller 입력으로 쓰인다
- RL 기반 controller는 각 발 주변의 높이 정보를 elevation map에서 샘플링해 사용한다.
- 다만 이것은 논문 자체가 foothold planner를 제안했다기보다,
  terrain-aware controller input으로 map을 사용했다는 의미로 보는 것이 적절하다.

### 6. leg odometry 기반 walking에서는 slip 때문에 vertical drift가 커질 수 있다
- 특히 challenging terrain과 long mission에서 vertical drift가 문제가 되었고,
- IMU + LiDAR SLAM 기반 fusion odometry와 drift compensation을 함께 쓰면 문제가 더 줄어든다고 해석했다.
- 이 부분은 RL-specific insight라기보다, map 기반 terrain input을 쓰는 모든 locomotion control에서 공통으로 중요한 시스템 포인트로 정리했다.

### 7. model-based locomotion과의 연결은 가능성/활용 예시 소개 쪽에 가깝다
- 논문은 RL 쪽은 비교적 직접적인 사용 사례로 보여주지만,
- model-based 쪽은 [16], [22], [23] 등과 연결 가능한 feature 제공 관점에서 짧게 소개한다.
- 즉 하나의 통합된 model-based control architecture를 자세히 검증했다기보다,
  terrain representation framework가 여러 downstream locomotion 방식에 재사용될 수 있음을 보여주는 쪽으로 이해했다.

### 8. virtual floor는 foothold 계산용이 아니라 base pose reference용이다
- rough terrain 자체는 foothold 계산에는 중요하다.
- 하지만 base/body reference는 너무 local roughness를 그대로 따라가면 불안정해질 수 있다.
- 그래서 smoothing된 virtual floor는 body 자세 기준면을 안정화하기 위한 별도 레이어로 이해했다.

### 9. conclusion에서의 핵심 self-positioning
- smoothness filters, plane segmentation 등 locomotion 관련 feature를 mapping framework 안에 통합했다.
- 따라서 이 논문은 단순 map 구현이 아니라,
  legged locomotion 연구에 유용한 terrain representation toolbox / infrastructure 성격이 강하다고 정리했다.

---

## 오늘의 최종 정리
이 논문은 다음처럼 이해하는 것이 적절하다.

- 핵심 기여:
  - fast GPU elevation mapping
  - drift compensation / visibility cleanup / overlap clearance
  - traversability / upper bound / smoothing / segmentation 등 파생 기능 통합
- 강한 적용 사례:
  - navigation
  - RL-based terrain-aware locomotion
- 상대적으로 약한 부분:
  - model-based locomotion과의 end-to-end closed-loop 검증은 깊지 않음
- 전체 포지션:
  - 여러 downstream locomotion/control 연구에 재사용 가능한 terrain representation framework
