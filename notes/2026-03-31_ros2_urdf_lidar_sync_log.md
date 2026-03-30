# 2026-03-31 ROS2 URDF / LiDAR frame 정리 로그

## 오늘 한 일
오늘은 `elevation_mapping_cupy` 세팅 전에,
ROS2 쪽 기본 bringup 구조를 먼저 정리하는 작업을 진행했다.

핵심 목적은 다음과 같았다.
- ANYmal URDF를 ROS2 패키지로 포팅
- RViz에서 robot model / TF 확인
- Isaac Sim LiDAR point cloud를 ROS2 frame 구조와 맞출 준비

---

## 1. ROS2 workspace / description package 구성
프로젝트 디렉토리 아래에 ROS2 workspace와 description 패키지를 두는 구조로 진행했다.

- workspace:
  - `/home/dangmu/3D_Navigation_project/dangmu_ws`
- package:
  - `/home/dangmu/3D_Navigation_project/dangmu_ws/src/anymal_description`

---

## 2. ANYmal URDF 포팅 및 mesh 경로 정리
기존에 가져온 ANYmal URDF에서 mesh URI가 원래 package 이름을 가리키고 있었는데,
이를 현재 패키지 이름에 맞게 모두 수정했다.

예:
- 기존:
  - `package://anymal_c_simple_description/meshes/...`
- 수정 후:
  - `package://anymal_description/meshes/...`

확인 결과:
- `package.xml`의 패키지 이름은 `anymal_description`
- `urdf/anymal.urdf` 안의 mesh URI도 `anymal_description`
- `meshes/` 폴더 안의 `.dae` 파일도 실제로 존재

즉 description 패키지 구조 자체는 정상으로 정리되었다.

---

## 3. display launch / RViz 설정
`display.launch.py`를 작성/수정해서 다음이 가능하도록 정리했다.

- `robot_state_publisher`
- `joint_state_publisher_gui`
- `rviz2`
- `display.rviz` 자동 로드

관련 파일:
- launch:
  - `/home/dangmu/3D_Navigation_project/dangmu_ws/src/anymal_description/launch/display.launch.py`
- rviz config:
  - `/home/dangmu/3D_Navigation_project/dangmu_ws/src/anymal_description/rviz/display.rviz`

또한 `CMakeLists.txt`에 `launch`, `urdf`, `meshes`, `rviz`가 설치되도록 정리했다.

---

## 4. TF 문제 확인: 원인은 use_sim_time
처음에는 revolute joint 이후 TF가 RViz에서 끊겨 보이는 문제가 있었다.
`view_frames`와 RViz 상태를 같이 확인한 뒤,
원인은 `use_sim_time=true` 상태에서 실제 `/clock` 없이 로컬 bringup을 띄운 것이었다.

정리:
- Isaac Sim 없이 로컬에서 URDF만 볼 때는 `use_sim_time=false`
- Isaac Sim / clock 연동 시에는 `use_sim_time=true`

이 문제를 바로 잡은 뒤,
URDF 기반 TF 트리는 정상적으로 동작하는 것을 확인했다.

---

## 5. LiDAR frame 구조 정리
처음에는 URDF 안의 기존 `lidar` / `lidar_cage` 구조와,
Isaac Sim에서 생성한 RTX LiDAR prim/frame을 어떻게 맞출지 여러 번 조정했다.

최종적으로는 현재 단계에서 다음과 같이 정리했다.

- URDF는 일단 그대로 유지
- launch에서 `base -> lidar_frame` static TF 사용
- Isaac Sim point cloud publish도 `lidar_frame` 기준으로 맞춤

즉 오늘 기준으로는
**ROS/RViz 쪽에서 실제 사용하는 LiDAR frame 이름을 `lidar_frame`으로 통일**해서 맞춰놓은 상태다.

---

## 6. Isaac Sim LiDAR ROS2 스크립트 정리
관련 스크립트:
- `/home/dangmu/3D_Navigation_project/scripts/anymal_rtx_lidar_ros2.py`

오늘 이 파일에서 한 일:
- RTX LiDAR 생성 코드 정리
- ROS2 bridge 사용
- `RtxLidarROS2PublishPointCloud` writer 사용
- PointCloud2 frame_id를 `lidar_frame` 기준으로 맞춤

이 과정에서,
기존 asset 안의 lidar 모형/Xform과 실제 RTX LiDAR 생성 위치를 어떻게 맞출지 여러 번 조정했고,
오늘 세션 기준으로는 **RViz에서 point cloud와 frame 정렬이 일단 맞는 상태**까지 왔다.

---

## 오늘의 결과
오늘 기준으로 확보된 상태는 다음과 같다.

1. ANYmal URDF가 ROS2 description 패키지로 포팅됨
2. RViz에서 robot model / TF 확인 가능
3. `use_sim_time` 관련 TF 문제 원인 파악 및 해결
4. LiDAR frame과 Isaac point cloud publish 기준을 현재 구조에 맞게 정리
5. 이후 Isaac joint states / odom 동기화로 넘어갈 준비가 됨

---

## 다음 단계
다음에는 아래 순서로 진행하면 된다.

1. Isaac Sim에서 실제 `joint_states` 받아서 URDF와 동기화
2. Isaac pose / odometry 받아서 `odom -> base` 동기화
3. 현재 point cloud + TF 구조를 `elevation_mapping_cupy` 입력에 연결

---

## 한 줄 요약
오늘은 **ANYmal URDF 포팅 + ROS2 bringup + RViz 확인 + LiDAR frame 동기화 기초 정리**까지 완료했다.
