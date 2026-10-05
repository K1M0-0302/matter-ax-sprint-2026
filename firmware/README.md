# firmware — nRF54LM20 DK Matter 펌웨어

matter AX Sprint 2026 출품작의 Matter over Thread 펌웨어. 보드는 **nRF54LM20 DK v0.7.0 (SoC nRF54LM20B, PCA10184)**, SDK는 **nRF Connect SDK v3.4.1**.

현재 `app/`은 NCS의 `samples/matter/template`을 그대로 복사한 상태다. 주제가 확정되면 이 위에 엔드포인트와 로직을 얹는다.

## 1. 개발 환경 (Arch Linux 기준, 1회)

공식 지원 OS는 Windows·macOS·Ubuntu지만 Arch에서도 같은 도구로 동작한다.

```bash
# 1) nrfutil (Nordic 통합 CLI) — ~/.local/bin 이 PATH에 있어야 한다
mkdir -p ~/.local/bin && cd ~/.local/bin
curl -L -o nrfutil https://files.nordicsemi.com/artifactory/swtools/external/nrfutil/executables/x86_64-unknown-linux-gnu/nrfutil
chmod +x nrfutil
nrfutil install sdk-manager device

# 2) 툴체인 + SDK (약 13 GB, ~/ncs/ 아래)
nrfutil sdk-manager install v3.4.1

# 3) VS Code 확장
code --install-extension nordic-semiconductor.nrf-connect-extension-pack

# 4) SEGGER J-Link (DK 플래시에 필수) — AUR
yay -S jlink-software-and-documentation     # libudev0-shim 도 함께 설치된다

# 5) udev 규칙 + 시리얼 그룹 (재로그인 필요)
sudo bash tools/setup-system.sh
```

확인:

```bash
nrfutil device list          # Board version PCA10184, Ports /dev/ttyACM0,1 이 보이면 OK
nrfutil device device-info --serial-number <SN>   # deviceName: nRF54LM20B
```

## 2. 빌드

west는 SDK 워크스페이스(`~/ncs/v3.4.1`) 안에서 실행해야 하고, 툴체인 환경은 `nrfutil sdk-manager toolchain launch`가 잡아 준다.

```bash
FW=$(pwd)            # 이 firmware/ 디렉터리
cd ~/ncs/v3.4.1
nrfutil sdk-manager toolchain launch --ncs-version v3.4.1 -- \
  west build --sysbuild -b nrf54lm20dk/nrf54lm20b/cpuapp -d $FW/build $FW/app
```

- 보드 타깃: `nrf54lm20dk/nrf54lm20b/cpuapp` (LM20A 보드면 `nrf54lm20a`)
- 결과물: `build/merged.hex` (MCUboot + 앱 + factory data)
- 재빌드는 같은 명령. 설정을 바꿨으면 `-p` 추가(pristine).

VS Code에서는 nRF Connect 확장의 "Add an existing application"으로 `app/`을 열고, Build Configuration에서 같은 보드 타깃을 고르면 된다.

## 3. 플래시·시리얼

```bash
cd ~/ncs/v3.4.1
nrfutil sdk-manager toolchain launch --ncs-version v3.4.1 -- west flash -d $FW/build

# 시리얼 로그: 앱 콘솔은 vcom 1 = /dev/ttyACM1 (115200). vcom 0 은 조용하다.
stty -F /dev/ttyACM1 115200 raw -echo -crtscts clocal && cat /dev/ttyACM1
# tio/picocom 이 있으면 그걸 써도 된다. VS Code 는 nRF Terminal 확장이 같은 포트를 연다.
# 보드 리셋:  nrfutil device reset --serial-number <SN>
```

부팅 로그에 Matter 온보딩 QR 코드 URL과 수동 페어링 코드가 찍힌다. 기본 샘플은 부팅 직후 BLE 광고(기기 이름 `MatterTemplate`)를 시작한다.

2026-10-05 실측(template 그대로):

| 항목 | 값 |
|---|---|
| 앱 플래시 사용량 | 720,244 B / 1,949,552 B (36.9%) |
| 앱 RAM 사용량 | 168,796 B / 511 KB (32.3%) |
| VID / PID | 65521 (0xFFF1) / 32768 (0x8000) — 테스트용 |
| Discriminator / Passcode | 3840 (0xF00) / 20202021 |
| QR 페이로드 | `MT:Y.K9042C00KA0648G00` |
| 수동 페어링 코드 | 34970112332 |
| BLE 광고 | PC `bluetoothctl` 스캔에서 `MatterTemplate` 확인 |

부팅 로그의 `[DIS]Failed to advertise commissionable node: 3` 류 에러는 Thread 네트워크에 아직 안 붙어 IPv6 인터페이스가 없어서 나는 것이다. 커미셔닝 전에는 정상이다.

## 4. 버튼·LED (template 샘플 기본값)

| 입력/출력 | 동작 |
|---|---|
| LED1 | 상태 표시: 광고 중 짧은 점멸, 커미셔닝 후 점등 |
| Button1 길게(6초) | 공장 초기화 |
| Button4 | BLE 광고 재시작 |

## 5. 2단계 (아직 안 함)

- Thread Border Router: nRF52840 Dongle(RCP) + 이 PC docker OTBR, 또는 상용 허브
- 컨트롤러: chip-tool + Home Assistant(Matter Server)
- 엣지 AI(Axon NPU) 툴링: 주제 확정 후

## 참고

- [nRF54LM20 DK 제품 페이지](https://www.nordicsemi.com/Products/Development-hardware/nRF54LM20-DK)
- [Matter: Template 샘플 문서](https://nrfconnectdocs.nordicsemi.com/ncs/3.4.1/nrf/samples/matter/template/README.html)
- [NCS v3.4.1 설치 문서](https://nrfconnectdocs.nordicsemi.com/ncs/3.4.1/nrf/installation/install_ncs.html)
