# matter-ax-sprint-2026

「지능형 홈(AI@Home) matter AX Sprint 2026」 해커톤 팀 저장소. 본선 시연은 2026년 10월 중.

## 폴더

| 폴더 | 내용 |
|---|---|
| `firmware/` | nRF54LM20 DK용 Matter 펌웨어. 설치·빌드·플래시 절차는 [`firmware/README.md`](firmware/README.md) |
| `firmware/app/` | 현재 앱. NCS v3.4.1의 Matter **template** 샘플을 그대로 복사한 상태(아직 수정 없음) |
| `firmware/tools/` | Linux용 udev 규칙과 `setup-system.sh` |
| `pm/` | 제안서 초안(`PROPOSAL.md`). 제출용 PDF·docx·hwp는 git에 올리지 않는다 |
| `research/` | 조사 노트 |

## 2026-10-05 현재 상태

- 보유 하드웨어: **nRF54LM20 DK v0.7.0 1개** (SoC nRF54LM20B, 보드 번호 PCA10184). nRF5340 DK는 없음.
- 개발환경(Arch Linux)에서 nRF Connect SDK **v3.4.1**로 template 샘플을 빌드·플래시했고, 보드가 부팅 후 BLE로 `MatterTemplate` 광고를 내는 것까지 확인했다. CLI(west)와 VS Code 확장 양쪽 다 빌드 성공.
- Matter over **Thread** 구성. Wi-Fi 실드(nRF7002 EB2)는 없다.
- 주제(공모 분야)는 **미정**. `pm/PROPOSAL.md`의 「새막이」안은 쓰지 않기로 했다. 새 주제가 정해지면 `firmware/app/src/default_zap/template.zap`에서 엔드포인트·클러스터를 추가하는 것부터 시작한다.

## 아직 안 된 것 (다음 사람이 이어갈 일)

1. **Thread Border Router가 없다.** Matter over Thread 기기는 BR 없이는 커미셔닝이 안 된다.
   - LM20 DK는 기기 역할이라 BR 라디오로 못 쓴다. nRF5340 DK는 애초에 RCP 펌웨어가 지원되지 않는다(NCS 전 버전 확인).
   - 가장 싼 길: **nRF52840 Dongle**(국내 약 2만원, 디바이스마트·아이씨뱅큐) + PC에서 docker OTBR. 대안: Home Assistant Connect ZBT-2($49), 또는 Nest Hub 2세대·Apple TV 4K 같은 상용 허브.
2. BR이 생기면 컨트롤러로 **chip-tool**(디버깅)과 **Home Assistant + Matter Server**(시연 UI)를 올려 커미셔닝을 시험한다.
3. 엣지 AI(LM20B의 Axon NPU) 툴링은 주제가 "보드에서 추론"을 요구할 때만 추가한다.

## 다른 OS에서 환경 만들기 (Windows·macOS)

Linux(Arch) 절차는 `firmware/README.md`에 있다. Windows·macOS는 Nordic 공식 경로가 더 쉽다.

1. [VS Code](https://code.visualstudio.com/) 설치 후 확장 **nRF Connect for VS Code Extension Pack** 설치.
2. [SEGGER J-Link](https://www.segger.com/downloads/jlink/) 설치 (DK 플래시에 필요).
3. VS Code 왼쪽 nRF Connect 아이콘 → **Welcome** 패널 → **Manage SDKs**에서 `v3.4.1` 설치, **Manage toolchains**에서 `v3.4.1` 설치. 합쳐서 약 13 GB.
4. `firmware/` 폴더를 VS Code로 연다(`.vscode/settings.json`이 SDK·툴체인 v3.4.1과 `app`을 자동으로 잡는다).
5. **Applications** 패널의 `app` → **Add build configuration** → Board target `nrf54lm20dk/nrf54lm20b/cpuapp` → **Generate and Build**.
6. DK를 **디버거 쪽 USB-C(J4)** 에 연결하고 **Actions → Flash**. 로그는 **Connected Devices**에서 **VCOM1**을 연다(VCOM0은 조용하다).

공식 설치 문서: https://nrfconnectdocs.nordicsemi.com/ncs/3.4.1/nrf/installation/install_ncs.html

## 알아둘 값 (template 그대로일 때)

| 항목 | 값 |
|---|---|
| 보드 타깃 | `nrf54lm20dk/nrf54lm20b/cpuapp` (sysbuild) |
| 시리얼 콘솔 | VCOM1, 115200 |
| Discriminator / Passcode | 3840 / 20202021 |
| 수동 페어링 코드 | 34970112332 |
| BLE 기기 이름 | `MatterTemplate` |
