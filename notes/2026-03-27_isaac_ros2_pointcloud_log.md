# 2026-03-27 Isaac Sim ROS2 PointCloud 확인 로그

## 오늘 한 일
오늘은 Isaac Sim에서 quadruped(ANYmal) 위에 RTX LiDAR를 추가하고,
ROS2 `PointCloud2` 형태로 publish하여 RViz에서 실제로 보이는지 확인했다.

---

## 목표
오늘의 목표는 다음 최소 파이프라인 검증이었다.

- Isaac Sim에서 센서 데이터 생성
- ROS2로 point cloud publish
- RViz에서 시각화 확인

즉, local height map을 직접 구현하기보다
**시뮬레이터 데이터가 실제 프로젝트 입력 형식으로 빠져나오는지**를 먼저 검증하는 것이 목적이었다.

---

## 진행 과정 요약
### 1. 기존 ANYmal asset의 센서 구조 확인
- `/World/Anymal/base` 아래에
  - `depth_camera_left_camera`
  - `depth_camera_right_camera`
  - `lidar_cage`
  - `imu_link`
  같은 prim 이름이 존재하는 것을 확인했다.
- 하지만 이 prim들은 실제 sensor prim이라기보다 **Xform 기반의 장착 위치/형상 구조**로 판단했다.
- 따라서 기존 asset에서 바로 데이터를 읽기보다는, 실제 RTX LiDAR sensor를 명시적으로 추가하는 방향으로 결정했다.

### 2. RTX LiDAR 예제 경로 확인
다음 Isaac Sim 예제를 기준으로 작업 방향을 잡았다.
- `/home/dangmu/isaacsim/standalone_examples/api/isaacsim.ros2.bridge/rtx_lidar.py`
- `/home/dangmu/isaacsim/standalone_examples/api/isaacsim.sensors.rtx/rotating_lidar_rtx.py`

특히 `rtx_lidar.py`에서:
- `IsaacSensorCreateRtxLidar`
- `RtxLidarROS2PublishPointCloud`
구조를 가져오는 것이 핵심이었다.

### 3. ANYmal용 ROS2 point cloud 테스트 스크립트 작성
- 스크립트 파일:
  - `/home/dangmu/3D_Navigation_project/scripts/anymal_rtd_lidar_ros2.py`
- 작업 내용:
  - `isaacsim.ros2.bridge` 활성화
  - `/World/Anymal/base` 아래에 `front_lidar` RTX LiDAR 생성
  - `RtxLidarROS2PublishPointCloud` writer 부착
  - `RtxLidarDebugDrawPointCloud`도 같이 활성화

### 4. 초기 코드 오류 수정
초기 작성본에서는 `omni.kit.commands.execute()` 호출에서
명령 이름 `"IsaacSensorCreateRtxLidar"`가 빠져 있었다.
이 부분을 수정하고,
path 지정도 다음과 같이 더 안전한 형태로 정리했다.

- `path="front_lidar"`
- `parent="/World/Anymal/base"`

---

## 최종 확인 결과
실행 후 RViz에서 `PointCloud2`가 실제로 보이는 것을 확인했다.

즉 오늘 기준으로는 다음 파이프라인이 성공했다.

**Isaac Sim → RTX LiDAR → ROS2 PointCloud2 → RViz**

이것으로,
향후 elevation mapping 패키지나 별도 프로젝트 레포에 입력을 연결하기 위한
기본 센서 데이터 파이프라인이 확보되었다고 볼 수 있다.

---

## 오늘의 의미
오늘 작업은 단순 센서 테스트가 아니라,
앞으로의 terrain perception / elevation mapping 프로젝트에서 필요한 첫 번째 실질 입력 경로를 확보한 것이다.

이제 다음 단계에서는:
- topic / frame 정리
- 실제 프로젝트 레포 입력 형식과 맞추기
- elevation mapping 패키지에 point cloud 연결
같은 작업으로 자연스럽게 이어질 수 있다.

---

## 다음 단계 후보
1. 현재 point cloud topic / frame 구조 정리
2. 실제 프로젝트 레포에서 기대하는 ROS2 입력 형식 확인
3. 이 point cloud를 elevation mapping 패키지 입력으로 연결
4. 이후 [16] 논문을 읽고 model-based control 연결로 확장
