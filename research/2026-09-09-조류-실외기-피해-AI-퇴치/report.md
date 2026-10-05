---
topic: 비둘기·조류의 에어컨 실외기 둥지·배변 문제와 온디바이스 AI 퇴치 Matter 기기의 실현성 (지능형 홈 matter AX Sprint 2026 출품 검토)
date: 2026-09-09
mode: deep
project: /home/kimo/Projects/02-hackathon/matter-ax-sprint-2026
notebooklm: none
sources: 40
reviewer: not-run
reviewer_metrics: 미실행 — pm-agent 세션에서 작성(research-reviewer 없음). 서브에이전트 5개가 출처 본문을 열어 원문 문자열을 대조했고 그 기록은 notes/q1~q5.md 에 있다
---

# 비둘기·조류의 에어컨 실외기 둥지·배변 문제와 온디바이스 AI 퇴치 Matter 기기의 실현성

하위질문 5개(피해 실태 · 기존 해결책과 경쟁 · 온디바이스 기술 실현성 · Matter 표준 매핑과 개발킷 · 법·윤리·안전)를 서브에이전트 5개가 병렬 조사했고(각 WebSearch 8회), 이 보고서는 `notes/q1.md`~`q5.md` 를 병합한 것이다. 인용 문자열은 출처 페이지 원문 그대로다. 의견은 "추론:" 으로 시작한다.

## 1. 한 줄 결론

집비둘기는 2009년 유해야생동물로 지정된 종이고 산성 배설물·둥지 재료가 실외기 부식·통풍 차단(과열)을 일으키는데[1][3][5][8], 실외기 전용 AI·카메라 퇴치 상용 제품과 Matter 지원 퇴치 기기는 국문·영문 검색 모두 0건이며[12][14], COCO 사전학습 검출기의 `bird` 클래스와 Occupancy/Contact/On-Off 표준 클러스터만으로 "온디바이스 감지 → Matter 이벤트 → 로컬 퇴치"를 5주 안에 만들 수 있고[17][18][23][28], 법적으로는 포획·살상이 아닌 비접촉 기피는 허가 대상이 아니되 고통·상해를 주는 방식은 학대 조항에 걸린다[32][33][36].

## 2. 핵심 발견

1. 실외기(실외기실) 둥지·배변은 실제 민원 사례가 있고, 비둘기는 "한 번 둥지를 튼 안식처는 다시 찾는 습성" 이 있어 초기 차단이 중요하다[1][16]. 서울시 비둘기 관련 민원은 2024년 1,481건에서 2025년 1,658건으로 늘었다[2].
2. 피해 메커니즘은 1차 출처로 "산성 배설물 → 금속(특히 구리) 부식"[3][8]과 "둥지 나뭇가지 → 실외기 배기 차단 → 과열·화재 위험"[5]까지 확인된다. 알루미늄 핀 부식·효율 10~15% 저하 같은 실외기 특화 수치는 업체 자료(2차)에만 있다(§4).
3. 수동형(스파이크·망·반사물)은 습관화가 핵심 한계고, 초음파 단독은 대조군과 차이가 없었으며, 여러 종류를 무작위로 섞고 위치를 바꾸는 것이 습관화를 늦춘다[9]. 이것이 "새를 골라 반응하고 반응 패턴을 무작위화하는" 카메라+AI 방식의 논리적 근거다.
4. AI·카메라 기반 퇴치는 학술(Mask R-CNN + 레이저, 일일 퇴치율 40.3%)[10]·오픈소스(YOLOv5 + Raspberry Pi + Arduino)[11]가 있지만 전부 농경지·공장 규모이고, 실외기 전용 상용 AI 제품과 Matter 지원 퇴치 기기는 검색에서 0건이다[12][14].
5. 온디바이스 감지는 별도 학습 없이 시작할 수 있다 — COCO 에 `bird` 클래스가 있고[23], Raspberry Pi 5 CPU 만으로 YOLO 나노급이 NCNN 에서 67.03 ms/im[18], Coral 을 붙이면 26.35 ms[17], ESP32-S3 급 MCU 에서도 FOMO 가 143 ms(약 7 fps)로 돈다[19].
6. Matter 노출은 표준 조합 — 조류 감지 = Occupancy Sensor(Occupancy Sensing), 둥지 의심 = Contact Sensor(Boolean State), 퇴치기 = On/Off Light·Plug-in Unit(On/Off) — 이 안전하다. Google 은 지원 표 밖의 디바이스 타입을 "not officially supported" 라고 못박는다[28]. Matter 1.5 에 카메라 타입이 들어갔지만[24] MCU·컨트롤러 지원은 미확인이라 카메라는 AI 입력으로만 둔다.
7. 주최 지급 개발킷 두 종(nRF5340 DK · nRF54LM20 DK)은 nRF Connect SDK v3.2.0 Matter over Thread 샘플의 보드 타깃이고[31], Thread 는 Border Router 가 필수인데[30], SDK 는 완전한 Border Router 를 제공하지 않고 Linux PC 의 Docker OTBR + 외부 nRF RCP 조합을 안내하며[39], nRF54LM20 DK 가 Co-processor(RCP) 샘플의 보드 타깃이다[40] — 즉 킷 두 개로 "기기 + 보더 라우터" 를 구성할 수 있다.

## 3. 상세

### 3.1 문제 실태와 피해 (Q1)

**한국 사례와 메커니즘.** 도심 비둘기는 높은 곳·바위틈을 선호하는 습성 때문에 "아파트 에어컨 실외기실에 둥지를 틀기" 도 하며 입주민은 "깃털이나 배설물 탓에 피해를 입는다."[1] 인천 연수구 사례에서는 "에어컨 실외기실 창 틈으로 비둘기가 날아들어 둥지를 틀고 알을 낳을 때까지 몰랐다" 고 했다[1]. 같은 기사에서 전문가는 "비둘기는 한 번 둥지를 튼 안식처는 다시 찾는 습성이 있고, 비둘기 배설물은 산성이어서 건축 구조물 부식이나 세균 번식을 유발할지 몰라 전용 퇴치기구를 설치해야 한다" 고 조언한다[1]. 서울시 공식 안내도 "강한 산성을 띤 분변이 복구가 어려운 손상을 유발합니다." / "털날림, 분변 등으로 위생상의 피해를 줍니다." 라고 적는다[3]. 학술 출처는 배설물이 "its acidic pH end-product corrodes various metals, especially copper" 라고 확인한다[8]. 둥지 재료의 위험은 2026-06 체험 기사에 나온다 — "실외기 뒤쪽에 새들이 물어다 놓은 어마어마한 양의 나뭇가지가 쌓여 있었다." / "우리 집은 불이 나는 거였다"[5].

**건강 위험.** 히스토플라스마증은 "The disease is transmitted to humans by airborne fungus spores from soil contaminated by pigeon and starling droppings (as well as from the droppings of other birds and bats)." 로 전파되고[6], 비둘기 배설물은 크립토코쿠스의 "the most important source of the disease" 로 보이며 "It has been found in as many as 84 percent of samples taken from old roosts." 라고 한다[6]. 다만 같은 문서는 "Health risks from birds and bats are often exaggerated." 라고 단서를 달고 면역 저하자가 더 취약하다고 적는다[6]. 청소 시에는 "During the cleanup, seal heating and cooling air ducts or shut the system down." 이 권고된다[6] — 공조 설비 자체가 오염 경로가 된다는 뜻이다.

**정책·민원 수치.** 환경부는 "지난 2009년 '집비둘기 관리업무 처리지침'을 만들어 집비둘기를 유해동물로 지정했다."[1] 서울시의회는 2024-12-20 유해야생동물 먹이 주기 금지 조례 제정안을 통과시켰고 "조례안은 내년 1월 24일부터 시행된다."[4] 과태료는 "▴1회 20만 원 ▴2회 50만 원 ▴3회 이상은 최대 100만 원" 이며 서울시는 2026년 6월부터 집중 단속한다[2]. "전체 민원은 2024년 1,481건에서→2025년 1,658건으로 증가했으나, 위생 및 생활환경 관련 민원은 줄어든 것으로 나타났다." 그리고 단속·금지구역 지정 요청 민원이 "15건에서 910건으로 급증" 했다[2]. 서울시는 "먹이 제공은 집비둘기 개체 수 증가와 밀집을 유발해 배설물·악취·소음·시설물 오염 등 시민 불편의 주요 원인이다." 라고 본다[2].

**해외 통계.** "An individual pigeon can excrete up to 12 kg of excrement a year"[7], "Each year in the United States, pigeons cause approximately 1.1 billion dollars in environmental and infrastructural damage"[7], Sopron 구도심 조사에서 "The highest count was 963 pigeons in September, which, given the size of the area surveyed, represents a maximum density of 42 pigeons per hectare."[8]

추론: 실외기 특화 수치(핀 부식·효율 저하 %)는 1차가 없으므로 기획서에는 메커니즘(산성 부식·통풍 차단)만 1차로 쓰고, 문제 규모는 서울시 민원 총량이 아니라 "실외기실 둥지 사례 + 귀소성" 으로 서술하는 것이 정직하다.

### 3.2 기존 해결책과 한계 · AI 기반 경쟁 현황 (Q2)

**수동형.** 말레이시아 공장 실증(2025)에서 "The most effective were the moving predator model, reflective compact disc and high visibility reflective tapes." 였고, 그러나 "birds may habituate to these methods if they are exposed for some time" / "most birds tend to habituate when these are used for longer periods" 라고 습관화를 명시한다[9]. 완화책은 "any bird deterrent method was best to be deployed in multiple types at one time and in random patterns to slow down the habituation rates" 와 "frequently changing the location of these deterrents would prolong the efficacy rates." 다[9]. 국내 자가 설치용 스테인리스 버드스파이크는 "₩14,700원" 에 팔리고[15], 업체 시공은 "퇴치망·버드스파이크 시공을 하고 보통 25만~30만원을 받는다."[16] 비둘기는 "귀소 본능이 강해 한번 찾아온 곳은 다시 찾는 습성이 있기 때문에, 초기에 비둘기를 퇴치하지 않으면 비둘기와 원치 않는 동거를 하게될 수 있다."[16] 전국 개체 수는 "전국에는 약 100만 마리의 비둘기가 서식하고, 이중 수도권에만 50만 마리가 있다." 로 보도됐다(2019, 2차)[16].

**능동형.** 초음파 24.5–45.5 kHz 단독 장치는 "did not significantly different from control treatment" 였고, 가청역을 포함한 13.5–45.5 kHz + 점멸등 조합만 "were significantly effective" 였다[9]. 레이저는 "wild birds would not see the laser spot when weather is very sunny." 와 "The same laser scanning path would cause wild birds habituated" 라는 한계가 있다[10]. 모션 감지 스프링클러 Orbit Yard Enforcer 는 "$99.99", PIR 로 "up to 40 ft. away", 대상에 "birds" 가 포함되며 "Requires 4 AA alkaline batteries (not included)" 다[13]. "스마트" 조류 퇴치기로 팔리는 제품도 "When an intruder bird moves within 50 feet (15m) of the device, the motion sensor gets activated" 방식의 PIR + 소리이며 카메라·AI 분류는 없다[14].

**AI·카메라 기반.** Scientific Reports(2024-07-10)의 시스템은 "This model is established and trained using a mask R-CNN deep learning method, and the backbone used in this work is ResNet-101-FPN." 에 "a Jetson TX2 embedded system" 과 "a 400-mW green laser source" 를 결합했고 "with a high repulsion rate of 40.3% each day." / "The highest hourly wild bird repulsion rate was 97.1%." 를 보고한다[10]. 오픈소스 AVIGUARD 는 "AI-Powered Smart Bird Detection and Repellent System using YOLOv5, Raspberry Pi, OpenCV, and Arduino." 로 "activates a laser pointer, sounds a buzzer, and switches on a water pump through a relay module" 한다[11]. 2026-05 국내 언론의 "AI 비둘기 물총" 은 "USB 카메라와 소형 AI 컴퓨터, 서보모터, 전동 물총 등을 이용해 제작됐으며" 출처가 "레딧(muxamilian)" 인 개인 제작물이고 실외기 언급이 없다[12]. **실외기 전용 AI·카메라 퇴치 상용 제품은 국문·영문 질의 모두 0건**이었고(§4 검색 로그 #12·#15), **Matter 지원 조류 퇴치 기기도 0건**으로, 가장 "스마트" 한 제품이 "World's Only Device That Uses Bluetooth As Remote Control" 을 내세운다[14].

추론: "감지 → 트리거" 구조에서 카메라+AI 가 갖는 차별점은 (1) 비둘기만 골라 반응해 사람·바람 오작동을 줄이고 (2) 반응 패턴을 무작위화해 습관화를 늦추는 것이며, 이는 [9]의 권고와 맞는다. 특허 조사는 미수행이라 IP 공백까지는 단정할 수 없다.

### 3.3 온디바이스 감지·퇴치 장치의 기술 실현성 (Q3)

**감지 성능 실측.** Raspberry Pi + Coral 로 비둘기를 감지하는 공개 저장소는 라이브 처리 속도를 CPU 전용 "8.38 FPS", Coral 1개 "22.88 FPS", 2개 "32.34 FPS" 로, 순수 추론 지연을 CPU "114.28 ms" · Dual Coral "26.35 ms" 로 보고하며, COCO 사전학습·양자화 모델 "ssdlite_mobiledet_coco_qat_postprocess_edgetpu.tflite" 을 그대로 쓴다[17]. 단 Coral 경로는 "Google is no longer actively maintaining `pycoral`" 이고 "`pycoral` wheels only support up to **Python 3.9**" 다[17]. 가속기 없는 Raspberry Pi 5 CPU 에서 YOLO26n(640 입력, FP32)은 NCNN 포맷 67.03 ms/im(mAP50-95 0.4784), PyTorch 포맷 299.09 ms/im 이며 "Inference time does not include pre/post-processing."[18] XIAO ESP32S3 Sense 에서 Edge Impulse FOMO(MobileNetV2 0.35, 96×96)는 "the model latency is 143ms, and the frame rate per second is around 7 fps" / "This model uses around 250KB of RAM and 80KB of ROM (Flash)" 다[19].

**데이터셋.** COCO 는 "COCO contains 330K images, with 200K images having annotations for object detection, segmentation, and captioning tasks." 이고 클래스 목록에 "14: bird" 가 있다[23]. FOMO 예제는 "All the not-labeled images (47) were uploaded" 로 시작해 "the model ends with an overall F1 score of 85%, similar to the result when using the test data (83%)" 를 얻었다[19].

**저전력 트리거.** ESP32-S3 딥슬립은 "In Deep-sleep mode, the CPUs, most of the RAM, and all digital peripherals that are clocked from APB_CLK are powered off." 이고 "The RTC IO module contains the logic to trigger wakeup when one of RTC GPIOs is set to a predefined logic level." 이다[20]. HLK-LD2410 은 "24GHz millimeter wave radar sensor" 로 "The longest sensing distance is up to 5 meters" 이며 벤더는 "identify human bodies in motion and stationary states" 용으로 규정한다[21] — 새 감지 검증은 없다.

**액추에이터.** 12V 물 솔레노이드 밸브는 "$6.95", "12V320 mA", "Working Pressure: 0.02 Mpa - 0.8 Mpa" 이고 "We suggest a TIP120 or N-Channel power FET with a 1N4001 kickback diode to drive this from a microcontroller pin."[22] AVIGUARD 부품표는 "Raspberry Pi 3B" / "Arduino UNO" / "USB Webcam" / "2 × SG90 Servo Motors" / "Laser Module" / "Passive Buzzer" / "2-Channel Relay Module" / "12V DC Water Pump" 이며, 정량 결과 없이 향후 과제로 "Edge AI optimization for faster inference" 를 든다[11]. adamp87/pigeon 저장소도 퇴치 동작을 "Output & Repellent Action (Pigeon Trigger Callback / Annotated Video)" 로만 정의한다[17].

추론: 새가 실외기에 앉는 이벤트는 초 단위이므로 1~5 fps 면 충분하고, 노트북·Pi 5 CPU 만으로도 YOLO 나노급이 15 fps 안팎[18]이라 가속기 없이 시작할 수 있다. 공개 프로젝트 두 곳 모두 퇴치율을 싣지 않았으므로[11][17] 해커톤 산출물도 "감지 정확도·반응 지연" 은 수치화하되 "퇴치율" 은 실외 장기 관찰 없이 주장하지 않는 것이 맞다. 실외기 상부 온도·진동·방수·전원 인출 근거는 이번 조사에서 확보하지 못했다(§4).

### 3.4 Matter 표준 매핑 · SDK · 개발킷 · Multi-Admin (Q4)

**디바이스 타입·클러스터.** Google Home 지원 표에서 Occupancy Sensor 의 애플리케이션 클러스터는 "Occupancy Sensing", Contact Sensor 는 "Boolean State", On/Off Light·Plug-in Unit 은 "Level Control" 과 "On/Off" 다[28]. Google 은 "Device types other than the ones listed here are not officially supported in the Google Home ecosystem." 라고 명시한다[28]. matter.js 생태계 검증 표는 "On/Off Light (ID: 0x0100)" / "Contact Sensor (ID: 0x0015)" 를 싣고[27], Home Assistant Matter 통합은 "Binary sensor, Button, Climate, Cover, Fan, Light, Lock, Number, Select, Sensor, Siren, Switch, Update, and Water heater" 엔티티를 노출한다[30]. Matter 1.5(2025-11-20)는 "Matter 1.5 introduces one of the most anticipated additions to the specification: cameras." 이고 "Matter cameras support live video and audio streaming using established WebRTC technology" 다[24].

**Multi-Admin.** Google 프라이머는 "Nodes may also be commissioned on more than one Fabric. This property is often referred to as multi-admin." 라고 정의하고[25], Silicon Labs 는 "Matter devices can participate in multiple Matter ecosystems simultaneously through a feature called Multi-Admin." 라고 적는다[26]. 두 번째 생태계에 공유하는 UI 는 Apple Home "Turn On Pairing Mode", Google Home "Set up without QR Code", SmartThings "Share with other services" 다[26]. Home Assistant 도 "One of the great features of Matter is the so-called Multi Fabric feature: you can join the same device to multiple controllers." 라고 안내한다[30].

**SDK·개발킷.** nRF Connect SDK v3.2.0 Matter Light bulb 샘플의 Matter over Thread 보드 타깃에 "nrf5340dk/nrf5340/cpuapp" 과 "nrf54lm20dk/nrf54lm20a/cpuapp" 이 있고, Matter over Wi-Fi 는 "nrf7002ek" / "nrf7002eb2" 쉴드로 지원한다[31]. 같은 샘플은 "a white dimmable light bulb device" 를 구현하며 원격 제어에는 "the Thread Border Router (only for Matter over Thread communication)" 이 필요하다[31]. matter.js 는 "Please use 0xFFF1 as Vendor ID and 0x8000 as product id because matter.js uses this by the current example scripts by default." 라고 안내한다[27].

**Thread Border Router.** Home Assistant 문서는 "To add a Matter device which is based on the Thread radio protocol, you need a Thread border router near the device" 라고 명시하고, iPhone 사용자에게 "HomePod Mini or V2, Apple TV 4K or Home Assistant with the Home Assistant OpenThread Border Router app" 을, Android 사용자에게 "Nest Hub (2nd Gen) or Nest Wi-Fi Pro or Home Assistant with the Home Assistant OpenThread Border Router app" 을 든다[30]. Nordic 문서(v3.2.0)는 "The |NCS| does not provide a complete Thread Border Router solution." 이라 적고, "For development purposes, you can run the OpenThread Border Router on any Linux-based system using a Docker container that already has the Border Router installed." 라며 "you must connect an external nRF device that serves as radio co-processor." 라고 안내한다[39]. 그 RCP 펌웨어인 OpenThread Co-Processor sample 의 보드 타깃 목록에는 "nrf54lm20dk/nrf54lm20a/cpuapp" 이 있고(nrf5340dk 는 없음)[40].

**미인증 기기 커미셔닝.** Google 문서상 "VIDs `0xFFF1` — `0xFFF4` are reserved for testing." 이고 "Make sure you have created an integration with the correct VID/PID combination in the Developer Console." 이 필요하다[29]. matter.js 문서는 "When pairing with matter.js the operating system will ask you to allow to pair an 'uncertified device' which you need to allow." 라고 적는다[27]. Google Home 은 "All devices behind a Matter bridge appear as normal for a user in the Google Home ecosystem." 이라 밝히고[28], matter.js 표에서 Bridge 는 Apple·Google·Amazon·SmartThings·Home Assistant 가 "X"(지원)다[27].

추론: 채점 항목 "Cluster 표준 준수" 를 위해서는 커스텀 클러스터 대신 모든 컨트롤러가 이미 해석하는 표준 조합(Occupancy·Boolean State·On/Off)으로 매핑하는 것이 안전하다[28][30]. 하드웨어 분할은 (1) nRF5340 DK 단일 Matter 노드(엔드포인트 3개)에 노트북/Pi 의 AI 결과를 UART 로 넘기는 안이 커미셔닝·상태 동기화 시연에 가장 단순하고, (2) 두 번째 킷 nRF54LM20 DK 를 RCP 로 삼아 노트북 Docker OTBR 을 세우면[39][40] 보더 라우터를 따로 사지 않아도 된다. 다만 sample.yaml 의 보드 목록만 확인했고 실제 빌드·시리얼 연결은 실측 전이다. Multi-Admin 시연은 Apple Home 1차 커미셔닝 → "Turn On Pairing Mode" → Google Home "Set up without QR Code" → Home Assistant 공유 코드 순서가 문서로 뒷받침된다[26][30].

### 3.5 법·윤리·안전 제약 (Q5)

**포획·살상 vs 기피.** 야생생물법 제19조 제1항은 "누구든지 멸종위기 야생생물에 해당하지 아니하는 야생생물 중 기후에너지환경부령으로 정하는 종(…)을 포획ㆍ채취하거나 죽여서는 아니 된다." 이고, 제3항은 포획·살상 목적의 "1. 폭발물, 덫, 창애, 올무, 함정, 전류 및 그물의 설치 또는 사용" 을 금지하며, 예외는 "제23조제1항에 따라 시장ㆍ군수ㆍ구청장으로부터 유해야생동물의 포획허가를 받은 경우" 등이다[32]. 조문의 규제 동사는 "포획ㆍ채취하거나 죽여서는" 이고 "퇴치"·"기피" 를 허가 대상으로 삼는 문구는 없다[32]. 현행 야생생물법상 유해야생동물에는 "일부 지역에 서식밀도가 너무 높아 피해를 주는 꿩, 비둘기, 고라니, 멧돼지, 청설모 등" 이 포함된다[4]. 기사는 "모든 야생생물은 포획이나 감금, 고통을 주거나 상해를 입히는 행위를 금지한다." / "각 지자체에 신청해 따로 포획 허가를 받거나 전문 업체에 맡겨 문제를 해결해야 한다." 라고 정리한다[1].

**학대 금지.** 야생생물법 제8조 제2항은 "누구든지 정당한 사유 없이 야생동물에게 고통을 주거나 상해를 입히는 다음 각 호의 학대행위를 하여서는 아니 된다." 이며 그 안에 "3. 도구ㆍ약물을 사용하거나 물리적인 방법으로 고통을 주거나 상해를 입히는 행위" 가 있다[33]. 동물보호법 제10조 제2항은 "도구ㆍ약물 등 물리적ㆍ화학적 방법을 사용하여 상해를 입히는 행위" 와 "사람의 생명ㆍ신체에 대한 직접적 위협이나 재산상의 피해를 방지하기 위하여 다른 방법이 있음에도 불구하고 동물에게 고통을 주거나 상해를 입히는 행위" 를 금지한다[36].

**먹이주기 금지.** 근거는 법률 제20119호(공포 "2024. 1. 23.", 시행 "2025. 1. 24.")로 "지방자치단체의 장이 조례로 정하는 바에 따라 장소 또는 시기를 정하여 유해야생동물에게 먹이를 주는 행위를 금지하거나 제한할 수 있도록 하는" 개정이다[35]. 현행 조문은 제23조의3 제2항 "지방자치단체의 장은 조례로 정하는 바에 따라 장소 또는 시기를 정하여 유해야생동물에게 먹이를 주는 행위를 금지하거나 제한할 수 있다."[34] 서울시는 "2025년 7월 1일부터 서울시 유해야생동물 먹이주기 금지구역에서 비둘기에게 먹이를 주면 과태료가 부과됩니다." 라고 안내하며 구역은 "서울시 38개 유해야생동물 먹이주기 금지구역", 과태료는 "1차 20만원, 2차 50만원, 3차 100만원" 이다[3].

**설치·카메라·소음.** 공동주택관리법 시행령 제19조 제2항은 "입주자등은 다음 각 호의 어느 하나에 해당하는 행위를 하려는 경우에는 관리주체의 동의를 받아야 한다." 이며 "4. 가축(장애인 보조견은 제외한다)을 사육하거나 방송시설 등을 사용함으로써 공동주거생활에 피해를 미치는 행위" 와 "5. 공동주택의 발코니 난간 또는 외벽에 돌출물을 설치하는 행위" 가 들어 있다[38]. 개인정보 보호법 제25조는 공개된 장소의 고정형 영상정보처리기기 설치를 원칙 금지하되 예외로 "촬영된 영상정보를 저장하지 아니하는 경우로서 대통령령으로 정하는 경우" 를 두고, 안내판에 "설치 목적 및 장소" / "촬영 범위 및 시간" / "관리책임자의 연락처" 를 적어야 하며, "설치 목적과 다른 목적으로 임의로 조작하거나 다른 곳을 비춰서는 아니 되며, 녹음기능은 사용할 수 없다."[37]

추론: 설계 원칙은 "접촉 없이 놀라게만 한다" — 빛·움직임·짧은 소리 같은 비접촉 기피는 제19조·제23조 허가 밖이고[32], 상해·고통을 주는 물 고압 분사·전기충격은 제8조[33]와 동물보호법 제10조[36]에 걸릴 수 있으며 "전류 및 그물" 은 애초에 금지 도구다[32]. 카메라는 자기 실외기·난간 안쪽만 비추고 온디바이스 추론 후 저장하지 않는 설계[37]가 리스크를 가장 줄인다. 실외기 위 장치는 "외벽에 돌출물" 로, 소리 퇴치는 "방송시설 등" 으로 읽힐 수 있어[38] 관리주체 동의를 제품 온보딩에 넣는다. 둥지·알 처리 조문은 못 찾았으므로(§4) 제품은 "둥지가 생기기 전 예방" 을 목표로 하고, 둥지 의심 시 자동 퇴치를 멈추고 지자체 문의를 안내하는 보수 모드가 안전하다.

### 3.6 대회 배점 대응 종합 (추론)

추론: 본선 배점(Matter 구현 30 · 상호운용성 20 · 온디바이스 AI 20 · 창의성 15 · 사업화·기여도 15 — 대회 프로필 `/home/kimo/Projects/00-contests/2026-09-01-kashi-matter-ax-sprint-2026/profile.md`)에 대해 이 조사가 뒷받침하는 대응은 다음과 같다. (a) Matter 30·상호운용 20: 표준 3 엔드포인트[28] + Multi-Admin 공유 절차[26][30] + 킷 두 개로 기기·보더 라우터 구성[31][39][40]. (b) 온디바이스 AI 20: COCO `bird` 클래스 로컬 추론[18][23], 영상 비저장·비전송[37]. (c) 창의성 15: 실외기 전용 AI 퇴치·Matter 퇴치 기기 0건[12][14], 습관화 대응 무작위화[9]. (d) 사업화·기여도 15: 수동형 시장 가격대(1만 원대~30만 원)[15][16]와 개체 수·민원 추이[2][16], 공개 저장소.

## 4. 공백 · 한계 · 상충

- **실외기 특화 피해 수치 없음**: 알루미늄 핀 부식·효율 10~15% 저하·통풍 저하는 조류퇴치·HVAC 업체 자료(2차)에만 있어 인용하지 않았다(notes/q1.md·q2.md 보조 확인). 국내 실외기 수리비·조류 기인 실외기 화재의 공식 통계도 없다.
- **서울시 민원 2020년 667건 → 2023년 1,432건**: 검색 스니펫에만 있고 원문 미확인. Zucconi(2003) 마리당 비용·Shrestha(2022) 금속 부식 실측은 페이월/403.
- **과태료 부과 시점 상충**: [4]는 유예 후 "내년 3월 1일부터", 서울시 페이지[3]는 "2025년 7월 1일부터". 서울시 후속 안내가 최신이므로 기획서에는 [3]을 쓴다.
- **집비둘기 지정 월 상충**: 2009년은 언론 3건이 일치하나 월은 "6월"/"3월" 로 엇갈리고, 시행규칙 별표 3 원문은 law.go.kr 렌더링 실패로 미확인(notes/q5.md). 기획서에는 "2009년" 까지만 쓴다.
- **둥지·알·새끼 처리 조문**: 제19조 전문에 없고 다른 조·별표는 못 열었다. 서울시 비둘기 관리 매뉴얼·환경부 인도적 퇴치 가이드 원문도 못 찾았다.
- **특허 조사 미수행**(Google Patents 500) · **국내 조류 퇴치 시장 규모 없음**(글로벌 USD 426.82M/2025 는 보조 확인만) · **스프링클러형 습관화 학술 근거 없음**.
- **실외기 환경(상부 온도·진동·IP·전원 인출) 1차 근거 없음** — 제조사 매뉴얼 PDF 3종 파싱 실패. **비둘기 전용 데이터셋**(Roboflow) 전부 403.
- **Matter**: 스펙상 최소 fabric 수(5)·Boolean State Configuration·Apple "Add Anyway" 원문·Nordic 문서 사이트 본문(GitHub v3.2.0 rst 로 대체)·nRF7002 쉴드의 지급 킷 포함 여부·matter.js 및 컨트롤러의 1.5 카메라 지원 여부 미확인. RCP sample.yaml 은 보드 목록만 확인했고 빌드·OTBR 연결은 실측 전.
- **초음파 인체·반려동물 영향 1차 자료 없음** · **생활소음 규제의 가정용 장치 포함 여부 불명**(소음ㆍ진동관리법 제21조는 "사업장 및 공사장 등").
- **2차 출처만 있는 주장**: 전국 개체 수 100만·수도권 50만·시공비 25만~30만 원[16], AI 물총 사례[12].
- **MCP 미연결**: exa·jina 없이 내장 WebSearch/WebFetch 만 썼다.

**출처 게이트**: 고유 도메인 27 · 2차 2/40 ([12][16]) — deep 기준(고유 도메인 ≥5 · 2차 ≤50%) 충족.

**검색 로그** (하위질문당 8라운드, 총 40 + 보더 라우터 보강 1 — 상세는 notes/q1~q5.md)
| # | 질의 | 겨냥한 공백 | 얻은 것(태그) / 남은 공백 |
|---|---|---|---|
| 1 | 실외기 비둘기 둥지 피해 | Q1 넓은 질의 | [1] / 정책·민원·건강·화재 |
| 2 | pigeon droppings air conditioner condenser damage nest | Q1 영어 | 업체 블로그(2차)만 / AC 특화 1차 부재 |
| 3 | 서울시 비둘기 민원 건수 유해야생동물 먹이주기 금지 조례 2025 시행 | 정책·민원 수치 | [2][3][4] / 2020→2023 민원 원문 |
| 4 | 에어컨 실외기 새 둥지 화재 소방 사례 | 둥지→화재 | [5] / 조류 기인 화재 공식 통계 없음 |
| 5 | CDC histoplasmosis cryptococcosis bird droppings pigeon health risk | 건강 1차 | [6] / CDC 자체 페이지 없음 |
| 6 | feral pigeon population city droppings damage cost estimate per year study | 해외 통계 | [7][8] / Zucconi 원문 |
| 7 | 실외기 비둘기 차단망 설치 비용 아파트 배설물 청소 업체 실외기 부식 | 국내 비용 | 커뮤니티(2차) / 공식 요금 없음 |
| 8 | bird droppings uric acid corrosion aluminum fins condenser coil HVAC manufacturer maintenance | 핀 부식 1차 | 없음(403·2차) |
| 9 | bird deterrent habituation review pigeons ultrasonic reflective tape effectiveness study | Q2 넓은 질의 | [9] / AI 제품·국내 시장 |
| 10 | AI camera bird deterrent YOLO detection trigger sprinkler laser github | 학술·오픈소스 | [10][11] / 실외기 전용 |
| 11 | 에어컨 실외기 비둘기 퇴치 제품 가격 | 국내 제품 | 보조 확인 / 원문 가격 |
| 12 | 실외기 비둘기 AI 카메라 감지 자동 퇴치 스마트 장치 | 실외기 전용 AI(국문) | [12] / 영문·Matter |
| 13 | Orbit Yard Enforcer motion activated sprinkler birds habituation study effectiveness | 스프링클러 근거 | [13] / 습관화 학술 없음 |
| 14 | Matter compatible bird deterrent device smart home pigeon repeller | Matter 기기 | [14] / 0건 |
| 15 | "air conditioner" outdoor unit pigeon deterrent camera AI automatic product balcony | 실외기 전용 AI(영문) | 수동형만 / 0건 |
| 16 | 비둘기 퇴치 시장 규모 조류 퇴치 용품 국내 아파트 실외기 민원 통계 | 시장·현황 | [15][16] / 국내 시장 규모 없음 |
| 17 | bird deterrent raspberry pi camera object detection github project | Q3 공개 프로젝트 | [17][11] / 데이터셋·트리거 |
| 18 | YOLOv8n Raspberry Pi 5 Hailo-8L AI HAT FPS benchmark object detection | Pi5 수치 | [18] / ESP32 |
| 19 | Edge Impulse FOMO ESP32-S3 object detection inference time ms benchmark | MCU 수치 | [19] / 데이터셋 |
| 20 | Roboflow Universe pigeon detection dataset images YOLOv8 | 비둘기 데이터셋 | 403 → [23] / — |
| 21 | LD2410 mmWave PIR wake ESP32-S3 camera deep sleep inference low power trigger | 웨이크업 구조 | [20][21] / 액추에이터 |
| 22 | wiki.seeedstudio.com XIAO ESP32S3 Sense Edge Impulse FOMO object detection latency ms | 143 ms 1차 | [19] 확정 / 실외기 환경 |
| 23 | 실외기 비둘기 둥지 퇴치 장치 실외기 상부 설치 전원 온도 | 실외기 환경 | 수치 없음 / 미해결 |
| 24 | air conditioner outdoor unit installation manual operating ambient temperature range vibration … | 매뉴얼 수치 | PDF 파싱 실패 / 미해결 |
| 25 | Matter 1.5 camera device type CSA announcement Camera AV Stream Management cluster | Q4 1.5 카메라 | [24] / 타입·클러스터 표 |
| 26 | nRF Connect SDK Matter samples nRF5340 DK Thread light bulb … nRF54LM20 Matter support | Nordic 샘플 | [31] / latest 본문 |
| 27 | Matter Multi-Admin definition fabrics multiple ecosystems Apple Home Google Home SmartThings Home Assistant same device | Multi-Admin 정의 | [25][26] / 최소 fabric 수 |
| 28 | matter.js supported device types bridge aggregator Raspberry Pi Node.js … | matter.js 타입·브릿지 | [27] / 클래스 목록 |
| 29 | Matter uncertified device commissioning test vendor ID 0xFFF1 … Developer Console | 미인증 커미셔닝 | [29][27] / Apple 1차 |
| 30 | Matter over Thread device requires Thread Border Router … OpenThread Border Router SkyConnect commissioning | TBR 필요 여부 | [30] / — |
| 31 | CSA newsroom "Matter 1.6" release joint fabric 2026 | 스펙 최신성 | 보조 확인 / — |
| 32 | Apple Home app Matter accessory "uncertified" "Add Anyway" … | Apple 제약 | 보조 확인 / Apple 원문 |
| 33 | 집비둘기 유해야생동물 지정 야생생물 보호 및 관리에 관한 법률 시행규칙 별표 | Q5 지정 근거 | URL 확보 / 조문 원문 |
| 34 | 비둘기 퇴치 합법 동물보호법 학대 서울시 비둘기 관리 매뉴얼 인도적 | 학대·매뉴얼 | [36] / 매뉴얼 없음 |
| 35 | 초음파 조류 퇴치기 소음 규제 아파트 실외기 위 설치 관리규약 카메라 개인정보보호법 제25조 | 소음·설치·카메라 | 생활법령 / 초음파 영향 |
| 36 | 유해야생동물 먹이주기 금지 과태료 야생생물법 개정 시행 2025 환경부 보도자료 집비둘기 | 먹이주기 | [3][35] / 조문 번호 |
| 37 | 개인정보보호법 제25조 고정형 영상정보처리기기 … 에어컨 실외기 전원 무단 인출 전기안전 KC 인증 | 카메라·전원 | [37] / 전원 규정 없음 |
| 38 | feral pigeon … Migratory Bird Treaty Act 50 CFR 10.13 …; Wildlife and Countryside Act 1981 section 1 | 해외 참고 | 보조 확인 / — |
| 39 | 집비둘기 유해야생동물 지정 2009년 환경부 별표 서울시 비둘기 관리 인도적 둥지 제거 산란기 매뉴얼 | 지정 연도·매뉴얼 | 언론(2009) / 별표 원문 |
| 40 | 초음파 조류퇴치기 인체 영향 반려동물 청력 20kHz … 실외기 위 설치 관리사무소 동의 외벽 부착물 | 초음파·설치 | [38][33][34] / 초음파 1차 없음 |
| 41 | nRF Connect SDK OpenThread Border Router Linux PC nRF5340 DK RCP co-processor sample docker | 보더 라우터 대안(부모 세션) | [39][40] / 빌드 실측 |

## 5. 출처
| N | 제목(원어) | URL | 접근일 | 스냅샷 |
|---|---|---|---|---|
| 1 | 아파트 실외기실 둥지 틀기 딱? 도심 속 비둘기와 불편한 동거 | https://www.kihoilbo.co.kr/news/articleView.html?idxno=1028071 | 2026-09-09 | |
| 2 | 비둘기 먹이주면 과태료! 6월 집중단속…금지구역은? | https://mediahub.seoul.go.kr/archives/2018306 | 2026-09-09 | |
| 3 | 왜 비둘기에게 먹이를 주면 안되나요? | https://news.seoul.go.kr/env/archives/563478 | 2026-09-09 | |
| 4 | 비둘기에게 먹이 주면…과태료 최대 '100만원' | https://www.nongmin.com/article/20241224500084 | 2026-09-09 | |
| 5 | 우연히 에어컨 실외기 뒤를 봤다가, 기절할 뻔했습니다 | https://www.ohmynews.com/NWS_Web/View/at_pg.aspx?CNTN_CD=A0003241182&PAGE_CD=N0002&CMPT_CD=M0137 | 2026-09-09 | |
| 6 | HEALTH HAZARDS ASSOCIATED WITH BIRD AND BAT DROPPINGS | https://dph.illinois.gov/content/dam/soi/en/web/idph/files/publications/health-hazards-associatedwith-bird-and-bat-droppings-050316.pdf | 2026-09-09 | |
| 7 | Ecology of Feral Pigeons: Population Monitoring, Resource Selection, and Management Practices | https://www.intechopen.com/chapters/66330 | 2026-09-09 | |
| 8 | THE ENVIRONMENTAL IMPACT OF THE FERAL PIGEON (COLUMBA LIVIA F. DOMESTICA) IN THE HISTORICAL CITY CENTRE OF SOPRON | https://www.analecta.hu/index.php/analecta/article/download/44455/43572 | 2026-09-09 | |
| 9 | Efficacy of Several Types of Pest Bird Deterrents and General Trend of Pest Birds at an Industrial Factory | https://pmc.ncbi.nlm.nih.gov/articles/PMC12017283/ | 2026-09-09 | |
| 10 | Automatic wild bird repellent system that is based on deep-learning-based wild bird detection and integrated with a laser rotation mechanism | https://www.nature.com/articles/s41598-024-66920-2 | 2026-09-09 | |
| 11 | AVIGUARD — AI-Powered Smart Bird Detection and Repellent System using YOLOv5, Raspberry Pi, OpenCV, and Arduino | https://github.com/HarshaSarathy/AVIGUARD | 2026-09-09 | |
| 12 | "비둘기 보이면 자동 조준"…AI 퇴치 장치 등장 — 전자신문 | https://www.etnews.com/20260514000493 | 2026-09-09 | |
| 13 | Yard Enforcer® Motion-Activated Sprinkler 62100 | https://www.orbitonline.com/products/yard-enforcer-motion-activated-sprinkler | 2026-09-09 | |
| 14 | Smart Bird Repellent - Gets Pigeons, Crows, Blackbirds, Sparrow, Canary & Other Birds Out of Your Patio, Balcony or Garden | https://homeshielders.com/products/smart-bird-repellent-gets-pigeons-crows-blackbirds-sparrow-canary-other-birds-out-of-your-patio-balcony-or-garden | 2026-09-09 | |
| 15 | 조류 퇴치 방법 스틸 버드 스파이크 특허제품 아파트 베란다 실외기 까치 비둘기 퇴치법 | https://excoa.shop/product/조류-퇴치-방법-스틸-버드-스파이크-특허제품-아파트-베란다-실외기-까치-비둘기-퇴치법/244/ | 2026-09-09 | |
| 16 | 알까고 푸드덕… 아파트 점령한 '비둘기 떼' — 머니투데이 | https://www.mt.co.kr/society/2019/05/25/2019052410081667242 | 2026-09-09 | |
| 17 | GitHub - adamp87/pigeon: Pigeon Repellent with Artificial Intelligence | https://github.com/adamp87/pigeon | 2026-09-09 | |
| 18 | YOLO26 on Raspberry Pi Setup & Benchmarks \| Ultralytics | https://docs.ultralytics.com/guides/raspberry-pi/ | 2026-09-09 | |
| 19 | Object Detection with XIAO ESP32S3 Sense | https://tinyml4d.gitbook.io/edge-machine-learning/computer-vision-cv/object-detection-with-xiao-esp32s3-sense | 2026-09-09 | |
| 20 | Sleep Modes - ESP32-S3 — ESP-IDF Programming Guide | https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/sleep_modes.html | 2026-09-09 | |
| 21 | HLK-LD2410 24Ghz Human Presence Body Induction Distance Detection Radar Sensor Module support GPIO and UART ports | https://www.hlktech.net/index.php?id=988 | 2026-09-09 | |
| 22 | Plastic Water Solenoid Valve - 12V - 1/2 Nominal : Adafruit Industries | https://www.adafruit.com/product/997 | 2026-09-09 | |
| 23 | COCO Detection Dataset \| Ultralytics | https://docs.ultralytics.com/datasets/detect/coco/ | 2026-09-09 | |
| 24 | Matter 1.5 Introduces Cameras, Closures, and Enhanced Energy Management Capabilities | https://csa-iot.org/newsroom/matter-1-5-introduces-cameras-closures-and-enhanced-energy-management-capabilities/ | 2026-09-09 | |
| 25 | The Fabric | https://developers.home.google.com/matter/primer/fabric | 2026-09-09 | |
| 26 | Multicontroller Ecosystem \| Matter Ecosystems \| Silicon Labs Matter | https://docs.silabs.com/matter/latest/matter-ecosystems/multicontroller-ecosystem | 2026-09-09 | |
| 27 | Overview of the Matter Ecosystems (matter.js ECOSYSTEMS.md) | https://github.com/matter-js/matter.js/blob/main/docs/ECOSYSTEMS.md | 2026-09-09 | |
| 28 | Supported device types \| Matter \| Google Home Developers | https://developers.home.google.com/matter/supported-devices | 2026-09-09 | |
| 29 | Matter Troubleshooting | https://developers.home.google.com/matter/troubleshooting | 2026-09-09 | |
| 30 | Matter — Home Assistant | https://www.home-assistant.io/integrations/matter/ | 2026-09-09 | |
| 31 | Matter: Light bulb (sdk-nrf v3.2.0 samples/matter/light_bulb/README.rst) | https://raw.githubusercontent.com/nrfconnect/sdk-nrf/v3.2.0/samples/matter/light_bulb/README.rst | 2026-09-09 | |
| 32 | 조문정보 \| 국가법령정보센터 — 야생생물 보호 및 관리에 관한 법률 제19조(야생생물의 포획ㆍ채취 금지 등) | https://www.law.go.kr/LSW//lsLinkProc.do?lsNm=%EC%95%BC%EC%83%9D%EC%83%9D%EB%AC%BC+%EB%B3%B4%ED%98%B8+%EB%B0%8F+%EA%B4%80%EB%A6%AC%EC%97%90+%EA%B4%80%ED%95%9C+%EB%B2%95%EB%A5%A0&chrClsCd=010202&joNo=0019000000&mode=10&datClsCd=010102 | 2026-09-09 | |
| 33 | 조문정보 \| 국가법령정보센터 — 야생생물 보호 및 관리에 관한 법률 제8조(야생동물의 학대금지) | https://www.law.go.kr/LSW//lsLinkProc.do?lsNm=%EC%95%BC%EC%83%9D%EC%83%9D%EB%AC%BC+%EB%B3%B4%ED%98%B8+%EB%B0%8F+%EA%B4%80%EB%A6%AC%EC%97%90+%EA%B4%80%ED%95%9C+%EB%B2%95%EB%A5%A0&chrClsCd=010202&joNo=0008000000&mode=10&datClsCd=010102 | 2026-09-09 | |
| 34 | 국가법령정보센터 — 야생생물 보호 및 관리에 관한 법률 개정문 목록(법률 제21126호, 제23조의3) | https://www.law.go.kr/LSW/lsRvsDocListP.do?lsId=009683&chrClsCd=010102 | 2026-09-09 | |
| 35 | 국가법령정보센터 — 전체 제정·개정이유(야생생물 보호 및 관리에 관한 법률, 법률 제20119호) | https://www.law.go.kr/LSW/lsRvsRsnListP.do?lsId=009683&chrClsCd=010102 | 2026-09-09 | |
| 36 | 조문정보 — 동물보호법 제10조(동물학대 등의 금지) | https://www.law.go.kr/LSW//lsLinkProc.do?lsNm=%EB%8F%99%EB%AC%BC%EB%B3%B4%ED%98%B8%EB%B2%95&chrClsCd=010202&joNo=0010000000&mode=10&datClsCd=010102 | 2026-09-09 | |
| 37 | 개인정보 보호법 제25조(고정형 영상정보처리기기의 설치·운영 제한) | https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=900079397&lsId=011357&chrClsCd=010202&print=print | 2026-09-09 | |
| 38 | 조문정보 — 공동주택관리법 시행령 제19조(관리규약의 준칙) | https://www.law.go.kr/LSW//lsLinkProc.do?lsNm=%EA%B3%B5%EB%8F%99%EC%A3%BC%ED%83%9D%EA%B4%80%EB%A6%AC%EB%B2%95+%EC%8B%9C%ED%96%89%EB%A0%B9&chrClsCd=010202&joNo=0019000000&mode=10&datClsCd=010102 | 2026-09-09 | |
| 39 | Thread tools (sdk-nrf v3.2.0 doc/nrf/protocols/thread/tools.rst) | https://raw.githubusercontent.com/nrfconnect/sdk-nrf/v3.2.0/doc/nrf/protocols/thread/tools.rst | 2026-09-09 | |
| 40 | OpenThread Co-Processor sample (sdk-nrf v3.2.0 samples/openthread/coprocessor/sample.yaml) | https://raw.githubusercontent.com/nrfconnect/sdk-nrf/v3.2.0/samples/openthread/coprocessor/sample.yaml | 2026-09-09 | |
