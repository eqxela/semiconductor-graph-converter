# 📊 일괄 그래프 변환기 (Batch Graph Converter) 사용 설명서

이 툴은 반도체 소자 특성 엑셀 데이터를 논문 피겨(Paper Figure) 가이드라인에 맞춘 고품질 벡터 그래픽(**SVG**)으로 일괄 변환해 주는 자동화 도구입니다.

연구원들이 복잡한 Matplotlib 코드를 만지지 않고도 논문 서식에 완벽히 부합하는 그래프를 클릭 한 번으로 제작할 수 있도록 최적화되어 있습니다.

---

## ✨ 핵심 기능 (Key Features)

1. **Adobe Illustrator / PowerPoint 편집 호환성 극대화 (`svg.fonttype: "none"`, SVG & PDF 동시 저장)**
   * Matplotlib에서 그래프를 저장할 때 글자가 그림(path)으로 쪼개지지 않고 **실제 텍스트(Arial 폰트) 그대로 저장**됩니다.
   * PPT나 키노트 발표 자료에 바로 삽입 가능한 고품질 **PDF** 파일과 일러스트레이터용 **SVG** 파일이 **동시에 생성**됩니다.
2. **발표용 프리셋 모드 (Presentation Preset Mode) 지원**
   * 논문용 대비 폰트 크기, 선 두께, 마커 크기 및 축 테두리 두께가 대폭 증가하여 빔프로젝터나 원격 미팅 화면에서도 멀리서 한눈에 잘 보이도록 그래프 스타일이 최적화됩니다.
3. **전달특성(TC) Hysteresis 구분 및 간소화**
   * Drain Current ($I_D$)는 굵은 실선(Forward)과 1점 쇄선(Backward)으로 구분하고, sweep 방향 화살표(`▶`/`◀`)를 표시하여 히스테리시스 방향성을 확실히 보여줍니다.
   * Gate Current ($I_G$, Gate leakage)는 얇은 반투명 점선(gray)으로 표시하여 dual-axis 없이 한 평면 위에 겹치지 않게 직관적으로 배치하고 시각적 복잡도를 최소화했습니다. (Gate Current에는 화살표 생략)
4. **의존성 패키지 자동 설치**
   * 파이썬이 설치된 환경이라면 스크립트 실행 시 필요한 라이브러리(`pandas`, `numpy`, `matplotlib`, `xlrd`, `openpyxl`)를 감지하여 없는 패키지를 **자동으로 설치**합니다.
5. **지능형 파일 분류 및 파싱**
   * 파일의 컬럼(Column) 구조와 파일명을 분석하여 **TC, IV, CV, CF, Retention, Transient** 특성을 자동으로 판별하고 그에 맞는 축 스케일(로그/리니어), 라벨, 범례를 설정합니다.
6. **전류/커패시턴스 단위 자동 Scaling**
   * 원본 데이터 전류가 $10^{-6}\text{ A}$ 수준이면 Y축 단위를 자동으로 $\mu\text{A}$로 변환하고 스케일을 보정합니다. (로그 스케일 제외)
7. **어닐링(Annealing) 조건별 테마 컬러 자동 지정**
   * 열처리 전(Before Annealing): **Blue (`#2F4EA2`)** 테마 컬러 적용
   * 열처리 후(After Annealing): **Red (`#D62728`)** 테마 컬러 적용
8. **GUI 실시간 로그 및 멈춤(Freezing) 방지**
   * 파일이 수백 개로 많아도 GUI 화면이 응답 없음으로 굳지 않고, 실시간으로 변환 성공 여부를 로그창에 업데이트합니다.

---

## 🚀 초보자를 위한 설치 및 실행 가이드 (Step-by-Step Guide for Beginners)

파이썬(Python)이나 깃허브(GitHub)를 다뤄본 적이 없는 연구원 분들을 위해 처음부터 실행하는 상세 방법입니다.

### 1단계. 프로그램 다운로드하기
1. 깃허브 페이지 우측 상단의 초록색 **`Code`** 버튼을 클릭합니다.
2. 메뉴에서 **`Download ZIP`**을 클릭하여 압축 파일을 다운로드합니다.
3. 다운로드한 `semiconductor-graph-converter-main.zip` 파일의 압축을 풀고 원하는 작업용 폴더에 배치합니다.

### 2단계. 파이썬(Python) 설치하기
프로그램을 실행하려면 컴퓨터에 파이썬이 설치되어 있어야 합니다.

#### 윈도우(Windows) 환경:
1. [파이썬 공식 다운로드 페이지](https://www.python.org/downloads/)에 접속하여 최신 버전(Windows용)을 다운로드하고 설치 프로그램을 실행합니다.
2. **[매우 중요]** 설치 첫 화면 맨 아래에 있는 **`Add python.exe to PATH`** 체크박스를 **반드시 체크**해 주세요. (체크하지 않으면 실행 시 오류가 발생합니다.)
3. `Install Now`를 누르고 잠시 기다려 설치를 완료합니다.

#### 맥(macOS) 환경:
1. 키보드의 `Cmd + Space`를 눌러 Spotlight 검색창을 켜고, **`Terminal`**을 입력하여 터미널 앱을 실행합니다.
2. 터미널 창에 `python3 --version`을 타이핑한 뒤 엔터를 누릅니다.
3. 파이썬이 설치되어 있지 않다면 자동으로 명령줄 개발자 도구 및 파이썬을 설치하라는 팝업 창이 뜹니다. **`설치`** 버튼을 눌러 설치를 완료해 주세요. (또는 파이썬 홈페이지에서 macOS용 설치 프로그램을 다운로드해 실행하셔도 됩니다.)

---

### 3단계. 프로그램 실행하기

#### 윈도우(Windows) 환경:
* 압축을 푼 폴더 안에 있는 **`run_windows.bat`** 파일을 마우스 더블클릭합니다.
* 자동으로 필요한 라이브러리 검사/설치가 진행된 후 GUI 프로그램 창이 실행됩니다.

#### 맥(macOS) 환경:
1. 터미널(Terminal) 앱을 실행합니다.
2. `cd ` (cd 뒤에 한 칸 띄움)를 타이핑한 뒤, 압축을 푼 폴더 자체를 터미널 창 안으로 **드래그 앤 드롭**하고 엔터를 칩니다.
   * *예시: `cd /Users/username/Downloads/semiconductor-graph-converter-main`*
3. 터미널 창에 아래 명령어를 입력하고 엔터를 칩니다:
   ```bash
   python3 convert_all_gui.py
   ```
4. 자동으로 필요한 라이브러리 검사/설치가 진행된 후 GUI 프로그램 창이 실행됩니다.

---

### 4단계. 그래프 변환하기 (GUI 조작)
1. GUI 창 상단의 **`찾아보기... (Browse...)`** 버튼을 클릭하여 소자 엑셀 데이터 파일(`.xls`, `.xlsx`)들이 모여 있는 대상 폴더를 선택합니다.
2. 랩미팅이나 PPT 발표용으로 가독성을 대폭 키우고 싶다면 **`발표용 (Presentation) 프리셋 모드 적용`** 체크박스를 체크합니다.
3. **`그래프 변환 시작 (Run Convert)`** 버튼을 클릭합니다.
4. 변환 완료 팝업이 뜨면 데이터 폴더에 고해상도 **SVG**(일러스트레이터 수정용) 및 **PDF**(PPT 슬라이드 삽입용) 그래프가 생성되어 있습니다.

---

## 💻 개발자용 CLI 모드 실행 (Command Line Interface)

터미널이나 명령 프롬프트 명령어로 더 빠르게 다량의 파일을 변환할 때 사용합니다.

* **기본 모드 실행:**
  ```bash
  python3 convert_all.py "/Users/username/Desktop/Data_Folder"
  ```

* **발표용 프리셋 적용 실행** (`-p` 또는 `--presentation` 플래그 추가):
  ```bash
  python3 convert_all.py -p "/Users/username/Desktop/Data_Folder"
  ```

---

## 📁 파일 이름 정의 및 분류 규칙

프로그램이 데이터를 완벽하게 인식하도록 하려면 **엑셀 파일명**과 **경로 이름**을 아래 규칙에 맞추어 주시기 바랍니다.

### 1. 샘플 이름 (Device / Sample Name) 추적 규칙

* **우선순위 1:** 파일의 전체 경로에 `sample 1` / `sample1`, `sample 2` 등이나 `thinner` 같은 단어가 있으면 자동으로 **"Sample 1"**, **"Sample 2"**, **"Thinner MoS2"** 등으로 분류합니다.
* **우선순위 2 (폴백):** 경로에 샘플명이 명시되어 있지 않은 일반 파일(예: `MoS2_deviceA_before_tc.xls`)인 경우, 확장자와 접미사를 뺀 앞부분인 **`MoS2_deviceA`**를 샘플명으로 추출하여 그래프 타이틀로 사용합니다.

### 2. 열처리 상태 (Annealing Status) 인식 규칙

* 경로 및 파일명에 `after`, `heating`, `150c` 중 하나라도 포함되어 있으면 그래프 타이틀에 **(After Annealing)**로 표시되고 **빨간색 계열 테마**로 그려집니다.
* 그렇지 않은 경우 기본값으로 **(Before Annealing)**와 **파란색 계열 테마**로 그려집니다.

### 3. 데이터 타입별 매칭 규칙

| 데이터 타입 | 판별 조건 (컬럼명 또는 파일명) | X축 라벨 | Y축 라벨 | 축 스케일 (X / Y) | 타이틀 접미사 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC** (전달특성) | `GateV` & `DrainI` 컬럼 포함 | Gate Voltage ($V_G$) | Current (A) | Linear / **Log** | Transfer Characteristics |
| **IV** (출력특성) | `DrainI(1)` 등 다중 Sweep 컬럼 포함 | Drain Voltage ($V_D$) | Drain Current ($I_D$) | Linear / Linear | Output Characteristics |
| **CV** (용량-전압) | `Capacitance` & `Voltage` 컬럼 포함 | Gate Voltage ($V_G$) | Capacitance (F) | Linear / Linear | Capacitance-Voltage (C-V) |
| **CF** (용량-주파수) | `Capacitance` & `Frequency` 컬럼 포함 | Frequency (Hz) | Capacitance (F) | **Log** / Linear | Capacitance-Frequency (C-f) |
| **Retention** | 파일명에 `retention` 포함 & `Time` 포함 | Time (s) | Current (A) 또는 Capacitance (F) | **Log** / Linear | Retention Characteristics |
| **Transient** | `Time` 컬럼 포함 | Time (s) | Current (A) 또는 Capacitance (F) | Linear / Linear | Transient Characteristics |

* *참고: 만약 데이터 계측기 로우 데이터상에 노이즈나 `0` 값이 있어 $log_{10}$ 연산 시 에러가 날 수 있는 TC 데이터의 경우, 안전장치 코드가 적용되어 최하단 전류가 `1e-15 A`로 자동 클리핑되어 에러 없이 매끄럽게 그려집니다.*

---

## 🎨 논문용 일러스트레이터(Adobe Illustrator) 편집 팁

변환 완료된 **SVG 파일**을 일러스트레이터에서 편집할 때 아래의 팁을 참고하면 눈 깜짝할 사이에 퀄리티 높은 피겨를 완성할 수 있습니다.

1. **텍스트 편집성 보존**
   * 그래프를 일러스트레이터로 불러온 뒤 단축키 `T`를 누르고 축 라벨이나 타이틀을 클릭하면 바로 텍스트 수정이 가능합니다.
   * 논문용 표준 서식인 **Arial** 폰트가 기본 지정되어 있으므로, 폰트가 깨지지 않게 Arial 폰트를 사용하세요.
2. **범례(Legend) 및 라벨 이동**
   * 범례 상자나 텍스트가 데이터 선을 가릴 경우, 마우스로 드래그하여 적절한 빈 공간으로 자유롭게 이동시키면 됩니다.
3. **선 두께 및 심볼 디테일 조정**
   * 변환된 그래프의 모든 선은 **벡터 패스(Vector Path)**입니다. 굵기가 마음에 들지 않으면 해당 선만 선택하여 획(Stroke) 두께를 간편하게 조절할 수 있습니다.

---

## 🛠️ 유지보수 & 문제 해결 (Troubleshooting)

### Q1. 파이썬 라이브러리 자동 설치에 실패했다는 문구가 뜹니다

PC의 권한 문제이거나 파이썬 환경이 꼬여 있을 수 있습니다. 터미널을 열고 직접 아래 명령어를 실행하여 수동으로 설치해 주세요:

```bash
pip install pandas numpy matplotlib xlrd openpyxl
```

### Q2. 특정 파일이 변환되지 않고 스킵되거나 그래프 축 이름이 이상하게 나옵니다

* 데이터 계측기에서 엑셀 파일로 출력할 때 컬럼 이름(예: `Gate V`, `Drain I` 등)에 오타가 있거나 공백이 비표준으로 들어간 경우일 수 있습니다.
* 데이터 컬럼 헤더가 `GateV`, `DrainI`, `GateI`, `Capacitance` 등으로 표준화되어 있는지 엑셀을 열어 확인하고 이름을 매칭해 주면 해결됩니다.

### Q3. 기본 색상이나 폰트 크기를 바꾸고 싶어요

* **`convert_all_gui.py`** (또는 `convert_all.py`)의 `set_paper_style()` 함수 내의 Matplotlib `rcParams` 값들을 수정하면 기본 폰트 사이즈 및 축 두께 등을 일괄 변경할 수 있습니다.
* 어닐링 전/후 색상 상수는 코드 최상단의 `VSET_COLOR` (열처리 후, Red) 및 `VRESET_COLOR` (열처리 전, Blue) 변수값을 변경하면 됩니다.
