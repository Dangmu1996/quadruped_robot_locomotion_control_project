# Isaac Sim / Isaac Lab 체크리스트

## 현재 상태
- [x] Isaac Sim 5.1.0이 홈 디렉토리에 설치되어 있음
- [x] Isaac Sim 5.1.0 기본 상태 확인 완료
- [ ] `3D_Navigation_project` 기준으로 Isaac 관련 작업 구조 정리
- [ ] Isaac Lab 호환 버전 확인
- [ ] Isaac Lab 설치

---

## 1. Isaac Sim 단독 확인

### 실행
- [x] Isaac Sim GUI 실행 확인
- [ ] 샘플 stage / example 정상 실행 확인
- [ ] headless 실행 가능 여부 확인
- [ ] 실행 시 에러 로그 정리

### Python / standalone
- [ ] `python.sh` 또는 해당 실행 엔트리포인트 확인
- [ ] standalone Python script 실행 확인
- [ ] Python에서 stage 로드 가능 여부 확인
- [ ] Python에서 simulation tick 가능 여부 확인

---

## 2. Quadruped / Terrain 확인

### 로봇 asset
- [ ] 기본 quadruped asset 확인
- [ ] scene에 spawn 가능 여부 확인
- [ ] physics 정상 동작 확인
- [ ] base pose 읽기 가능 여부 확인
- [ ] joint state 읽기 가능 여부 확인

### terrain
- [ ] flat terrain 확인
- [ ] rough terrain 예제 확인
- [ ] slope / stairs 예제 확인
- [ ] quadruped가 terrain 위에 정상 spawn되는지 확인

---

## 3. Sensor 확인

### 센서 구성
- [ ] depth camera 사용 가능 여부 확인
- [ ] LiDAR / RTX LiDAR 사용 가능 여부 확인
- [ ] 카메라/센서 frame 구조 확인
- [ ] 센서 부착 위치 정리

### 데이터 추출
- [ ] depth image 읽기 가능 여부 확인
- [ ] point cloud 또는 equivalent 3D data 추출 가능 여부 확인
- [ ] robot pose 추출 가능 여부 확인
- [ ] timestep별 데이터 저장 가능 여부 확인

---

## 4. Elevation Mapping 연결을 위한 최소 요구사항

다음 3개가 되면 mapping 실험 시작 가능:
- [ ] robot pose를 Python에서 읽을 수 있음
- [ ] depth / point cloud 데이터를 Python에서 읽을 수 있음
- [ ] terrain이 포함된 quadruped scene을 반복 실행할 수 있음

---

## 5. Isaac Lab 준비

### 호환성 확인
- [ ] Isaac Lab이 Isaac Sim 5.1.0과 호환되는 branch/tag 확인
- [ ] 필요한 Python 버전 확인
- [ ] 설치 가이드 확인
- [ ] 의존성 확인

### 설치 구조
- [ ] `3D_Navigation_project/isaaclab/`를 실제 repo 위치로 쓸지 결정
- [ ] 별도 repo로 둘지 결정
- [ ] git clone 경로 확정

### 설치 후 첫 확인
- [ ] Isaac Lab import / setup 완료
- [ ] 기본 예제 실행 확인
- [ ] quadruped locomotion 예제 존재 여부 확인
- [ ] env reset / step / render 확인

---

## 6. 연구 방향별 다음 단계

### A. Terrain perception 먼저
- [ ] 센서 데이터 추출 스크립트 작성
- [ ] local height / elevation map용 입력 데이터 저장
- [ ] terrain visualization 확인

### B. Locomotion / RL 먼저
- [ ] 기본 quadruped locomotion env 실행
- [ ] observation / action 구조 파악
- [ ] terrain curriculum / reward 구조 확인

---

## 7. 추천 우선순위

현재 추천 순서:
1. Isaac Sim에서 quadruped + terrain + sensor + pose 확인
2. point cloud / depth 데이터 추출 확인
3. Isaac Lab 호환 버전 확인
4. Isaac Lab 설치
5. 기본 quadruped env 실행
6. 이후 terrain perception 또는 locomotion 방향으로 분기

---

## 8. 메모
- 현재 연구 방향은 quadruped locomotion + terrain perception + elevation mapping + Isaac Sim 연계
- 지금은 Isaac Lab보다 먼저 Isaac Sim에서 데이터 흐름을 확인하는 것이 더 중요함
