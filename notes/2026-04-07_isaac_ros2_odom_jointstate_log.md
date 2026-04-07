# 2026-04-07 Isaac Sim ROS2 odom / joint_states 연동 로그

## 오늘 한 일
오늘은 Isaac Sim에서 이미 성공한 LiDAR point cloud publish 파이프라인 위에,
- `/odom` publish
- `odom -> base` TF 구성
- `/joint_states` publish
까지 추가해서,
ROS2/RViz 쪽 robot model과 sensor frame을 더 실제 시스템에 가깝게 동기화하는 작업을 진행했다.

---

## 1. `/odom` publish 추가 시도와 초기 문제
처음에는 Isaac Sim 스크립트 안에서 `rclpy`를 직접 import해서
`nav_msgs/Odometry`와 TF broadcaster를 쓰는 방향을 시도했다.

하지만 실행 시 다음 문제가 발생했다.
- Isaac Sim 내부 Python은 3.11 기반
- 시스템 ROS2 Jazzy의 `rclpy`는 Python 3.12 경로를 보고 있었음
- 그 결과 `_rclpy_pybind11` C extension mismatch가 발생

즉 `rclpy`를 직접 쓰는 방식은 현재 환경에서 맞지 않는 것으로 판단했다.

---

## 2. Isaac Sim 내부 ROS2 bridge 방식으로 전환
그 다음에는 Isaac Sim의 ROS2 bridge + OmniGraph 노드를 사용하는 방식으로 방향을 바꿨다.

핵심적으로 사용한 노드는 다음과 같다.
- `isaacsim.core.nodes.IsaacComputeOdometry`
- `isaacsim.ros2.bridge.ROS2PublishOdometry`

초기에는 TF까지 Isaac 안에서 바로 만들려고 `ROS2PublishTransformTree`를 같이 넣었지만,
이 노드에 잘못된 포트를 넣어서
- `inputs:parentFrameId`
- `inputs:childFrameId`
를 사용할 수 없다는 OmniGraphError가 발생했고,
이를 계기로 **먼저 `/odom`만 안정적으로 살리는 방향**으로 수정했다.

결과적으로:
- `anymal_odom.py`에서 `/odom` topic publish 성공
- twist 값도 Isaac 내부 odometry 계산 결과를 통해 포함되는 구조 확보

---

## 3. ROS2 쪽에서 `/odom`을 받아 `odom -> base` TF broadcast
Isaac 안에서 TF까지 억지로 만들기보다,
ROS2 workspace 쪽에서 `/odom`을 받아 TF로 재방출하는 방식이 더 안정적이라고 판단했다.

그래서 `anymal_description` 패키지 안에 다음 C++ 노드를 새로 작성했다.
- `src/odom_to_tf_broadcaster.cpp`

이 노드는:
- `/odom` subscribe
- `msg.pose.pose`를 읽음
- `odom -> base` TF를 broadcast
한다.

또한 다음 파일들도 함께 수정했다.
- `CMakeLists.txt`
- `package.xml`
- `launch/display.launch.py`

---

## 4. `/joint_states` publish 추가
다음 단계로는 Isaac Sim에서 실제 robot joint state를 publish해서,
RViz의 RobotModel과 URDF가 가짜 joint_state가 아니라 **실제 ANYmal 관절값**을 따라가게 만드는 작업을 진행했다.

핵심 노드는 다음과 같다.
- `isaacsim.ros2.bridge.ROS2PublishJointState`

처음에는 target prim을 `/World/Anymal`로 두었는데,
실행 로그에서 Isaac이 articulation을 찾지 못한다고 나왔다.

오류 예:
- `Failed to find articulation at '/World/Anymal'`
- `Provided pattern list did not match any articulations`

이를 통해 actual articulation root가 `/World/Anymal/base`라는 점을 다시 확인했고,
다음처럼 수정했다.
- `targetPrim = /World/Anymal/base`

이후 `/joint_states` publish가 정상 동작하는 방향으로 정리했다.

---

## 5. launch 정리
ROS2 쪽 launch 파일도 현재 구조에 맞게 정리했다.

현재 구성:
- `robot_state_publisher`
- `tf2_ros static_transform_publisher` (`base -> lidar_frame`)
- `odom_to_tf_broadcaster`
- `rviz2`

그리고 이제 Isaac에서 실제 `/joint_states`가 들어오기 때문에,
기존의 `joint_state_publisher_gui`는 launch에서 제거했다.

또한 현재는 `use_sim_time`도 `true`로 바꿔,
Isaac Sim과 함께 쓸 때의 구조에 맞춰놓은 상태다.

---

## 6. 현재 확보된 구조
오늘 세션이 끝난 시점의 구조는 다음과 같다.

### Isaac Sim 쪽
- `point_cloud`
- `/odom`
- `/joint_states`

### ROS2 쪽
- `odom -> base` TF (`/odom` 기반 broadcaster)
- `base -> lidar_frame` static TF
- `robot_state_publisher`
- RViz visualization

즉 현재는
**LiDAR frame / odom / joint state / robot model**이 모두 한 파이프라인 안에서 거의 맞물리는 상태까지 왔다.

---

## 오늘의 의미
오늘은 단순히 토픽 하나를 더 띄운 게 아니라,
이후 `elevation_mapping_cupy` 같은 perception/mapping 패키지를 붙이기 전에 필요한
ROS2 입력 구조를 거의 한 세트로 정리한 날이었다.

이제 다음 단계에서는:
1. 현재 `/odom`, `/joint_states`, point cloud 구조를 다시 점검하고
2. `elevation_mapping_cupy`가 요구하는 입력 토픽/프레임과 맞춘 뒤
3. 실제 elevation map이 생성되는지 연결 테스트를 해볼 수 있다.

---

## 한 줄 정리
오늘은 Isaac Sim에서 **point cloud + odom + joint_states**를 ROS2로 연결하고,
ROS2 쪽에서 **TF 및 URDF RobotModel과 동기화하는 구조**까지 거의 완성했다.
