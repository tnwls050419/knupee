import streamlit as st

# --------------------------
# 0. 기본 페이지 설정
# --------------------------
st.set_page_config(
    page_title="Physical Ethic Engine (PEE)",
    page_icon="🚗",
)

st.title("🚗 Physical Ethic Engine (PEE)")
st.markdown(f"#### 윤리적 가치관이 고려된 자율주행자동차")
st.caption("주행이나 주차시 발생할 수 있는 문제들에 대해 자신의 윤리적 가치관을 설정해 보세요 !")

st.markdown("---")

# --------------------------
# 1. 윤리 이슈 데이터 정의
#   - 드롭다운에 보이는 title을
#     '보행자 우선', '탑승자 우선', '안전 속도', '효율 속도' 처럼 단일 이름으로 구성
# --------------------------

ETHICS_DATA = {
    "주행(Driving)": [
        {
            "id": "drive_pedestrian_first",
            "title": "보행자 우선",
            "core_question": "보행자가 갑자기 나타났을 때, 차는 보행자를 우선으로 보호하기 위해 급정지한다.",
            "description": "차량 내부의 운전자보다 도로 위의 **보행자**를 우선하는 가치.",
            "input":"충돌이 예상되면 차량이 손상되거나 탑승자가 위험해지더라도 강한 감속/정지를 선택한다.",
        },
        {
            "id": "drive_passenger_first",
            "title": "운전자 우선",
            "core_question": "어떠한 위험/돌발 상황에서도 차는 운전자의 안전을 최우선으로 생각한다.",
            "description": "차량 내부의 **운전자**를 그 무엇보다 우선하는 가치. ",
            "input":"보행자나 장애물로 인한 정지가 운전자에게 위험하다고 판단된다면, 진행/완만한 감속을 선택한다.",
        },
        {
             "id": "drive_child_zone",
            "title": "보호구역 감속",
            "core_question": "어린이/노인 보호구역에 진입할 때, 감속을 진행한 상태로 진입해야 한다.",
            "description": "어린이/노인 보호구역에서 감속을 통해 사고를 예방하고 보호대상의 안전을 우선하는 가치. ",
            "input": "보호구역 진입시에는 정해진 속도제한을 지켜야 한다.",
        },
        {
            "id": "drive_signal_obey",
            "title": "신호 준수",
            "core_question": "실제 위험이 보이지만 신호는 '진행'일 때, 신호를 우선해야 할까?",
            "description": "교통 신호를 절대적으로 지킬지, 주변 상황에 따라 신호를 잠시 무시할 수 있을지에 대한 가치. "
                           "신호 체계와 실제 상황 중 무엇을 더 신뢰할지 결정한다.",
            "input":"(가치관 설명)"
        },
    ],

    # 아래 카테고리들은 기존 구조 유지 (필요하면 나중에 이슈도 잘게 쪼개서 재구성 가능)
    "주차(Parking)": [
        {
            "id": "park_1",
            "title": "장애인 전용 주차구역",
            "core_question": "비어 있는 장애인 전용 주차구역이라 하더라도, 해당 구역에 주차를 해서는 안 된다.",
            "description": "장애인, 교통약자를 위해 비워 둔 공간을 다른 차량이 주차에 사용할 수 있는지에 대한 가치.",
            "input": "보행상 장애가 있는 사람이 운전자나 동승자로 탑승해 있는 경우만 주차가 가능하다."
        },
        {
            "id": "park_2",
            "title": "소방도로 앞 주차",
            "core_question": "소화전, 소화기, 소방호스 연결구 등 소방 활동 시설 주변 5m 이내에는 주정차가 금지된다.",
            "description": "개인의 편의보다 비상 상황 대비 공간의 공공성과 안전성을 우선하는 가치.",
            "input": "개인의 편의를 위해서 비상 상황을 대비하는 공간에 잠깐이라도 주차를 해서는 안된다."
        },
        {
            "id": "park_3",
            "title": "민폐 주차 (칸 두 개 차지하기)",
            "core_question": "빠르고 편하게 주차하기 위해서 주차공간을 두 칸 차지해서는 안된다.",
            "description": "개인의 시간, 편의보다 공동 이용 자원을 우선하는 가치.",
            "input": "개인 편의보다 공동 이용 자원을 공정하게 나누어 쓰는 것이 중요하다."
        },
    ],

    "사생활(Privacy)": [
        {
            "id": "priv_1",
            "title": "민감 구역 촬영",
            "core_question": "집, 병원, 학교 앞에서도 항상 촬영해야 할까?",
            "description": "사생활 보호를 위해 특정 구역에서는 촬영을 제한할지 결정하는 가치.",
        },
        {
            "id": "priv_2",
            "title": "위치 데이터 보관 기간",
            "core_question": "이동 경로를 얼마나 오래 보관해야 할까?",
            "description": "편의·분석을 위해 데이터를 오래 보관할지, 사생활 보호를 위해 빨리 삭제할지에 대한 가치.",
        },
        {
            "id": "priv_3",
            "title": "제3자 데이터 제공",
            "core_question": "수집된 데이터를 경찰·학교·회사 등 제3자에게 어느 정도까지 제공해도 될까?",
            "description": "데이터의 공익 활용과 개인 정보 보호 사이의 균형을 정하는 가치.",
        },
        {
            "id": "priv_4",
            "title": "얼굴/행동 인식 범위",
            "core_question": "얼굴, 나이, 행동까지 세부적으로 분석해도 될까?",
            "description": "필요 최소 정보만 인식할지, 안전을 위해 상세 정보까지 수집할지에 대한 가치.",
        },
        {
            "id": "priv_5",
            "title": "불필요한 데이터 수집",
            "core_question": "주행과 직접 관련 없는 정보도 함께 저장해도 될까?",
            "description": "향후 활용 가능성을 위해 폭넓게 수집할지, 목적 외 수집을 금지할지에 대한 가치.",
        },
        {
            "id": "priv_6",
            "title": "데이터 암호화/보안",
            "core_question": "속도·편의보다 강한 보안을 우선해야 할까?",
            "description": "암호화로 성능이 떨어져도 보안을 우선할지, 반대로 편의를 우선할지에 대한 가치.",
        },
    ],

    "사고(Safety & Accident)": [
        {
            "id": "acc_1",
            "title": "보행자 vs 탑승자 보호",
            "core_question": "피할 수 없는 사고에서 보행자와 탑승자 중 누구를 더 보호해야 할까?",
            "description": "총 피해를 줄이기 vs 내 차량의 사람을 우선 보호하기 사이의 가치 문제.",
        },
        {
            "id": "acc_2",
            "title": "1명 vs 다수 보호",
            "core_question": "1명을 희생해서 다수를 살리는 선택이 정당할까?",
            "description": "인원 수 기준으로 판단할지, 사람을 수치화하지 말아야 할지에 대한 가치.",
        },
        {
            "id": "acc_3",
            "title": "약자 우선 보호",
            "core_question": "어린이, 노인, 장애인을 우선 보호하도록 코딩해야 할까?",
            "description": "신체적으로 약한 사람을 더 우선 보호할지, 모두를 동등하게 볼지에 대한 가치.",
        },
        {
            "id": "acc_4",
            "title": "동물 vs 사람",
            "core_question": "동물을 피하다가 사람이 더 크게 다칠 수 있다면 어떻게 해야 할까?",
            "description": "사람과 동물의 생명을 어떻게 비교·판단할지에 대한 가치.",
        },
        {
            "id": "acc_5",
            "title": "2차 사고 고려",
            "core_question": "앞의 장애물을 피하다가 옆 차선 차량과 큰 사고가 날 수 있다면 어떻게 해야 할까?",
            "description": "즉각적인 위험 vs 더 큰 2차 사고 위험 중 무엇을 우선할지에 대한 가치.",
        },
        {
            "id": "acc_6",
            "title": "급정지와 뒤차 사고",
            "core_question": "앞사람을 보호하기 위해 급정지하면 뒤 차량과의 추돌 위험은 감수해야 할까?",
            "description": "직접 마주한 위험을 막을지, 뒤차와의 연쇄 사고를 줄일지에 대한 판단 가치.",
        },
        {
            "id": "acc_7",
            "title": "사고 책임 주체",
            "core_question": "사고가 났을 때 책임은 개발자·제작사, 사용자 중 누구에게 더 클까?",
            "description": "코드를 설계한 사람과, 설정을 선택하고 사용한 사람의 책임 비중을 정하는 가치.",
        },
    ],
}

# --------------------------
# 2. 사이드바: 카테고리 & 이슈 선택
# --------------------------

st.sidebar.header("⚙️ 상황별 윤리적 가치관 선택")

category = st.sidebar.selectbox(
    "카테고리를 선택하세요.",
    list(ETHICS_DATA.keys()),
)

issues = ETHICS_DATA[category]
issue_titles = [i["title"] for i in issues]

selected_title = st.sidebar.selectbox(
    "윤리적 가치관을 선택하세요.",
    issue_titles,
)

selected_issue = next(i for i in issues if i["title"] == selected_title)

# --------------------------
# 3. 선택된 윤리 이슈 정보 표시
# --------------------------

st.subheader(f" 카테고리 : {category}")
st.markdown(f"### 윤리적 가치관 : **{selected_issue['title']}**")

st.markdown(f"##### 핵심 개념")
st.info(selected_issue["core_question"])

st.markdown("**이 윤리 코드의 의미**")
st.write(selected_issue["description"])
st.write(selected_issue["input"])

st.markdown("---")

# --------------------------
# 4. 아두이노용 전체 코드 생성 (각 이슈별 단일 코드)
# --------------------------

st.markdown("### 아래 코드를 아두이노 IDE에 그대로 복붙하면 돼요")

issue_id = selected_issue["id"]
title = selected_issue["title"]

arduino_code = ""  # 기본값

# 공통으로 자주 쓰는 라인트레이서 + 초음파 기반 코드 패턴을
# 각 이슈마다 조금씩 다르게 변형해서 사용

# 1) 주행(Driving) 카테고리
if category.startswith("주행"):

    # 보행자 우선
    if issue_id == "drive_pedestrian_first":
        template = """\
/* =========================================================
   RC카 라인트레이서 + 보행자 우선 모드 (주행 윤리)
   이슈: {title}
   설명: 보행자 감지 거리를 넉넉하게 잡고, 강하게 정지하는 모드
   ========================================================= */

int LS = A0;   // Left line sensor
int CS = A1;   // Center line sensor
int RS = A2;   // Right line sensor

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

int TRIG = 2;
int ECHO = 3;

// 보행자 감지 안전 거리 (cm)
const int SAFE_STOP_DIST = 30;
// 기본 주행 속도
const int BASE_SPEED = 120;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void stopCar() {
  motor(0, 0);
}

long getDist() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duration = pulseIn(ECHO, HIGH);
  return duration / 58;   // cm 근사값
}

void lineDrive(int speed) {
  int l = digitalRead(LS);
  int c = digitalRead(CS);
  int r = digitalRead(RS);

  if (c == LOW) {
    motor(speed, speed);      // 직진
  } else if (l == LOW) {
    motor(speed / 2, speed);  // 왼쪽으로 조향
  } else if (r == LOW) {
    motor(speed, speed / 2);  // 오른쪽으로 조향
  } else {
    motor(0, 0);              // 선을 놓치면 잠시 정지
  }
}

void setup() {
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);

  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.begin(9600);
  Serial.println("Driving Mode: 보행자 우선");
}

void loop() {
  long d = getDist();

  // 보행자 우선: 넉넉한 거리에서 정지
  if (d > 0 && d < SAFE_STOP_DIST) {
    stopCar();
  } else {
    lineDrive(BASE_SPEED);
  }

  delay(10);
}
"""
        arduino_code = template.replace("{title}", title)

    # 탑승자 우선
    elif issue_id == "drive_passenger_first":
        template = """\
/* =========================================================
   RC카 라인트레이서 + 탑승자 우선 모드 (주행 윤리)
   이슈: {title}
   설명: 탑승자의 안전과 빠른 이동을 우선. 아주 가까워졌을 때만 정지
   ========================================================= */

int LS = A0;
int CS = A1;
int RS = A2;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

int TRIG = 2;
int ECHO = 3;

// 정지 거리 (cm) - 더 짧게
const int STOP_DIST = 15;
// 더 빠른 주행 속도
const int BASE_SPEED = 180;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void stopCar() {
  motor(0, 0);
}

long getDist() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duration = pulseIn(ECHO, HIGH);
  return duration / 58;
}

void lineDrive(int speed) {
  int l = digitalRead(LS);
  int c = digitalRead(CS);
  int r = digitalRead(RS);

  if (c == LOW) {
    motor(speed, speed);
  } else if (l == LOW) {
    motor(speed / 2, speed);
  } else if (r == LOW) {
    motor(speed, speed / 2);
  } else {
    motor(0, 0);
  }
}

void setup() {
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);

  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.begin(9600);
  Serial.println("Driving Mode: 탑승자 우선");
}

void loop() {
  long d = getDist();

  // 탑승자 우선: 아주 가까울 때만 정지, 평소에는 빠르게 주행
  if (d > 0 && d < STOP_DIST) {
    stopCar();
  } else {
    lineDrive(BASE_SPEED);
  }

  delay(10);
}
"""
      
        arduino_code = template.replace("{title}", title)

    # 어린이 보호구역 감속 기준
    elif issue_id == "drive_child_zone":
        template = """\
/* =========================================================
   RC카 라인트레이서 + 어린이 보호구역 감속 모드
   이슈: {title}
   설명: '어린이 보호구역' 구간에서 미리 감속하는 주행
   (보호구역 여부는 예시로 버튼/스위치 입력으로 표현)
   ========================================================= */

int LS = A0;
int CS = A1;
int RS = A2;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

int TRIG = 2;
int ECHO = 3;

// 예시: 어린이 보호구역 ON/OFF 스위치
int CHILD_ZONE_SW = 4;

const int STOP_DIST = 25;
const int NORMAL_SPEED = 150;
const int CHILD_SPEED  = 90;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void stopCar() {
  motor(0, 0);
}

long getDist() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duration = pulseIn(ECHO, HIGH);
  return duration / 58;
}

void lineDrive(int speed) {
  int l = digitalRead(LS);
  int c = digitalRead(CS);
  int r = digitalRead(RS);

  if (c == LOW) {
    motor(speed, speed);
  } else if (l == LOW) {
    motor(speed / 2, speed);
  } else if (r == LOW) {
    motor(speed, speed / 2);
  } else {
    motor(0, 0);
  }
}

void setup() {
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);

  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(CHILD_ZONE_SW, INPUT_PULLUP);

  Serial.begin(9600);
  Serial.println("Driving Mode: 어린이 보호구역 감속");
}

void loop() {
  long d = getDist();
  int inChildZone = (digitalRead(CHILD_ZONE_SW) == LOW);  // 스위치 ON = 보호구역

  // 보호구역이면 속도 낮추기
  int speed = inChildZone ? CHILD_SPEED : NORMAL_SPEED;

  if (d > 0 && d < STOP_DIST) {
    stopCar();
  } else {
    lineDrive(speed);
  }

  delay(10);
}
"""
        arduino_code = template.replace("{title}", title)

    # 신호 준수
    elif issue_id == "drive_signal_obey":
        template = """\
/* =========================================================
   RC카 라인트레이서 + 신호 준수 모드
   이슈: {title}
   설명: '신호'가 우선인 주행. 예시로 버튼을 신호등으로 보고,
        신호가 빨강일 때는 무조건 정지, 초록일 때만 주행
   ========================================================= */

int LS = A0;
int CS = A1;
int RS = A2;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

// 예시: 신호등 입력 (스위치)
int SIGNAL_PIN = 4;  // LOW = 빨간불, HIGH = 초록불 (예시)

const int BASE_SPEED = 130;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void stopCar() {
  motor(0, 0);
}

void lineDrive(int speed) {
  int l = digitalRead(LS);
  int c = digitalRead(CS);
  int r = digitalRead(RS);

  if (c == LOW) {
    motor(speed, speed);
  } else if (l == LOW) {
    motor(speed / 2, speed);
  } else if (r == LOW) {
    motor(speed, speed / 2);
  } else {
    motor(0, 0);
  }
}

void setup() {
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);

  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(SIGNAL_PIN, INPUT_PULLUP);

  Serial.begin(9600);
  Serial.println("Driving Mode: 신호 준수");
}

void loop() {
  int signalState = digitalRead(SIGNAL_PIN); // LOW: 빨간불, HIGH: 초록불 (예시)

  if (signalState == LOW) {
    // 빨간불이면 주변 상황과 상관없이 무조건 정지
    stopCar();
  } else {
    // 초록불일 때만 라인을 따라 주행
    lineDrive(BASE_SPEED);
  }

  delay(10);
}
"""
      
        arduino_code = template.replace("{title}", title)

    else:
        arduino_code = "// TODO: 이 주행 이슈에 대한 코드를 추가로 설계해 보세요."


# 2) 주차(Parking) 카테고리 – 각 이슈별로 '주차 허용/금지' 행동 예시
elif category.startswith("주차"):

    # 장애인 주차구역 이용 여부
    if issue_id == "park_1":
        template = """\
/* =========================================================
   RC카 주차 시뮬레이션 + 장애인 주차구역 이용 여부
   이슈: {title}
   설명: '장애인 구역'을 RFID/마커 or 스위치로 표현하고,
        그 구역에는 절대 주차하지 않는 모드
   ========================================================= */

// 예시: RFID/마커 대신 스위치로 장애인 구역 여부 표현
int DISABLED_ZONE_SW = 4;  // LOW = 장애인 구역, HIGH = 일반 구역

int LED_OK  = 8;  // 주차 허용 표시
int LED_BAD = 9;  // 주차 금지 표시

void setup() {
  pinMode(DISABLED_ZONE_SW, INPUT_PULLUP);
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_BAD, OUTPUT);

  Serial.begin(9600);
  Serial.println("Parking Mode: 장애인 주차구역 이용 여부");
}

void loop() {
  int isDisabledZone = (digitalRead(DISABLED_ZONE_SW) == LOW);

  if (isDisabledZone) {
    // 장애인 구역이면 주차 금지
    digitalWrite(LED_OK, LOW);
    digitalWrite(LED_BAD, HIGH);
    Serial.println("장애인 구역 → 주차 금지");
  } else {
    // 일반 구역이면 주차 허용
    digitalWrite(LED_OK, HIGH);
    digitalWrite(LED_BAD, LOW);
    Serial.println("일반 구역 → 주차 허용");
  }

  delay(500);
}
"""
        arduino_code = template.replace("{title}", title)

    # 소방도로·출입구 앞 주차
    elif issue_id == "park_2":
        template = """\
/* =========================================================
   RC카 주차 시뮬레이션 + 소방도로·출입구 앞 주차
   이슈: {title}
   설명: '소방도로/출입구' 구간은 절대 주차하지 않는 모드
   ========================================================= */

int FIRE_ZONE_SW = 4;  // LOW = 소방도로/출입구, HIGH = 일반 도로

int LED_OK  = 8;  // 주차 허용
int LED_BAD = 9;  // 주차 금지

void setup() {
  pinMode(FIRE_ZONE_SW, INPUT_PULLUP);
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_BAD, OUTPUT);

  Serial.begin(9600);
  Serial.println("Parking Mode: 소방도로·출입구 앞 주차 금지");
}

void loop() {
  int isFireZone = (digitalRead(FIRE_ZONE_SW) == LOW);

  if (isFireZone) {
    digitalWrite(LED_OK, LOW);
    digitalWrite(LED_BAD, HIGH);
    Serial.println("소방도로/출입구 → 주차 금지");
  } else {
    digitalWrite(LED_OK, HIGH);
    digitalWrite(LED_BAD, LOW);
    Serial.println("일반 구역 → 주차 가능");
  }

  delay(500);
}
"""
        arduino_code = template.replace("{title}", title)

    # 민폐 주차(칸 두 개 차지하기)
    elif issue_id == "park_3":
        template = """\
/* =========================================================
   RC카 주차 시뮬레이션 + 민폐 주차(두 칸 차지하기)
   이슈: {title}
   설명: '자리가 충분해도 한 칸만 정확히 차지'하도록 유도하는 예시.
        센서로 칸 사이 중앙에 서도록 멈추는 로직.
   ========================================================= */

// 예시: 초음파로 앞 벽과의 거리, 라인 센서로 칸 중앙 맞추기 (간단 버전)

int LS = A0;
int CS = A1;
int RS = A2;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

int TRIG = 2;
int ECHO = 3;

const int TARGET_DIST = 15;  // 벽과의 적절한 거리

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void stopCar() {
  motor(0, 0);
}

long getDist() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duration = pulseIn(ECHO, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);

  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.begin(9600);
  Serial.println("Parking Mode: 한 칸 정확 주차 (민폐 주차 방지)");
}

void loop() {
  long d = getDist();

  // 벽과 너무 멀면 앞으로 조금 이동
  if (d > TARGET_DIST + 3) {
    motor(120, 120);
  }
  // 너무 가까우면 뒤로 조금
  else if (d > 0 && d < TARGET_DIST - 3) {
    motor(-120, -120);
  }
  else {
    // 거리 적당하면 멈추고 '한 칸'에 정확히 서 있다고 가정
    stopCar();
  }

  delay(50);
}
"""
        arduino_code = template.replace("{title}", title)

# 3) 사생활(Privacy) 카테고리 – 데이터 기록/삭제, 촬영 여부를 LED로 표현
elif category.startswith("사생활"):

    # 민감 구역 촬영
    if issue_id == "priv_1":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 민감 구역 촬영
   이슈: {title}
   설명: '민감 구역'에서는 촬영(기록) OFF로 전환하는 예시.
        스위치로 민감 구역 여부를 표현, LED로 촬영 ON/OFF 표시
   ========================================================= */

int SENSITIVE_SW = 4;   // LOW = 민감 구역, HIGH = 일반 구역
int LED_RECORD  = 8;    // 촬영/기록 ON
int LED_STOP    = 9;    // 촬영 중단 표시

void setup() {
  pinMode(SENSITIVE_SW, INPUT_PULLUP);
  pinMode(LED_RECORD, OUTPUT);
  pinMode(LED_STOP, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 민감 구역 촬영 제한");
}

void loop() {
  int isSensitive = (digitalRead(SENSITIVE_SW) == LOW);

  if (isSensitive) {
    // 민감 구역 → 촬영 중단
    digitalWrite(LED_RECORD, LOW);
    digitalWrite(LED_STOP, HIGH);
    Serial.println("민감 구역 → 촬영 OFF");
  } else {
    digitalWrite(LED_RECORD, HIGH);
    digitalWrite(LED_STOP, LOW);
    Serial.println("일반 구역 → 촬영 ON");
  }

  delay(500);
}
"""
        arduino_code = template.replace("{title}", title)

    # 위치 데이터 보관 기간
    elif issue_id == "priv_2":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 위치 데이터 보관 기간
   이슈: {title}
   설명: '데이터를 일정 시간 후 자동 삭제' 개념을
        타이머와 카운터로 단순화해서 표현
   ========================================================= */

unsigned long lastSaveTime = 0;
unsigned long lastDeleteTime = 0;

const unsigned long SAVE_INTERVAL   = 2000;  // 2초마다 '위치 저장'
const unsigned long DELETE_INTERVAL = 7000;  // 7초마다 '오래된 위치 삭제'

int LED_SAVE   = 8;
int LED_DELETE = 9;

void setup() {
  pinMode(LED_SAVE, OUTPUT);
  pinMode(LED_DELETE, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 위치 데이터 보관/삭제 주기");
}

void loop() {
  unsigned long now = millis();

  if (now - lastSaveTime > SAVE_INTERVAL) {
    lastSaveTime = now;
    digitalWrite(LED_SAVE, HIGH);
    Serial.println("위치 데이터 저장");
  } else {
    digitalWrite(LED_SAVE, LOW);
  }

  if (now - lastDeleteTime > DELETE_INTERVAL) {
    lastDeleteTime = now;
    digitalWrite(LED_DELETE, HIGH);
    Serial.println("오래된 위치 데이터 삭제");
  } else {
    digitalWrite(LED_DELETE, LOW);
  }

  delay(50);
}
"""
        arduino_code = template.replace("{title}", title)

    # 제3자 데이터 제공
    elif issue_id == "priv_3":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 제3자 데이터 제공
   이슈: {title}
   설명: '동의 여부'에 따라 제3자(예: 경찰/학교)에
        데이터를 제공하는지 여부를 나타내는 예시
   ========================================================= */

int CONSENT_SW = 4;   // LOW = 동의 O, HIGH = 동의 X (예시)
int REQUEST_SW = 7;   // LOW = 제3자가 데이터 요청

int LED_SEND = 8;     // 데이터 제공
int LED_DENY = 9;     // 제공 거부

void setup() {
  pinMode(CONSENT_SW, INPUT_PULLUP);
  pinMode(REQUEST_SW, INPUT_PULLUP);
  pinMode(LED_SEND, OUTPUT);
  pinMode(LED_DENY, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 제3자 데이터 제공 여부");
}

void loop() {
  int consent = (digitalRead(CONSENT_SW) == LOW);
  int request = (digitalRead(REQUEST_SW) == LOW);

  if (request) {
    if (consent) {
      digitalWrite(LED_SEND, HIGH);
      digitalWrite(LED_DENY, LOW);
      Serial.println("요청 발생 → 동의 있음 → 데이터 제공");
    } else {
      digitalWrite(LED_SEND, LOW);
      digitalWrite(LED_DENY, HIGH);
      Serial.println("요청 발생 → 동의 없음 → 데이터 제공 거부");
    }
  } else {
    digitalWrite(LED_SEND, LOW);
    digitalWrite(LED_DENY, LOW);
  }

  delay(100);
}
"""
        arduino_code = template.replace("{title}", title)

    # 얼굴/행동 인식 범위
    elif issue_id == "priv_4":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 얼굴/행동 인식 범위
   이슈: {title}
   설명: '최소 정보만 인식' vs '세부 정보까지 인식' 중
        여기서는 '최소 정보만 인식'을 구현한 예시.
        사람 감지(예: 센서)만 켜고, 자세한 정보는 저장하지 않는다는 개념
   ========================================================= */

// 예시: PIR 센서(동작 감지 센서)만 사용, 자세한 정보는 저장 X

int PIR = 4;        // 동작 감지 센서
int LED_DETECT = 8; // 누군가 있음을 나타내는 LED

void setup() {
  pinMode(PIR, INPUT);
  pinMode(LED_DETECT, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 최소 정보(존재 여부만) 인식");
}

void loop() {
  int motion = digitalRead(PIR);

  if (motion == HIGH) {
    digitalWrite(LED_DETECT, HIGH);
    Serial.println("사람 존재: YES (자세한 정보는 저장하지 않음)");
  } else {
    digitalWrite(LED_DETECT, LOW);
  }

  delay(300);
}
"""
        arduino_code = template.replace("{title}", title)

    # 불필요한 데이터 수집
    elif issue_id == "priv_5":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 불필요한 데이터 수집 금지
   이슈: {title}
   설명: '주행과 상관없는 데이터는 버린다'는 개념을 표현.
        버튼으로 '주행 관련' / '주행 무관' 데이터를 구분하는 예시
   ========================================================= */

int RELATED_SW   = 4;  // LOW = 주행 관련 데이터, HIGH = 관계 없음
int LED_STORE    = 8;  // 저장
int LED_IGNORE   = 9;  // 버림

void setup() {
  pinMode(RELATED_SW, INPUT_PULLUP);
  pinMode(LED_STORE, OUTPUT);
  pinMode(LED_IGNORE, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 불필요한 데이터 수집 금지");
}

void loop() {
  int related = (digitalRead(RELATED_SW) == LOW);

  if (related) {
    digitalWrite(LED_STORE, HIGH);
    digitalWrite(LED_IGNORE, LOW);
    Serial.println("주행 관련 데이터 → 저장");
  } else {
    digitalWrite(LED_STORE, LOW);
    digitalWrite(LED_IGNORE, HIGH);
    Serial.println("주행 무관 데이터 → 저장하지 않음");
  }

  delay(500);
}
"""
        arduino_code = template.replace("{title}", title)

    # 데이터 암호화/보안
    elif issue_id == "priv_6":
        template = """\
/* =========================================================
   RC카 사생활 윤리 + 데이터 암호화/보안
   이슈: {title}
   설명: '보안을 우선'하는 개념을 단순화해서 표현.
        데이터를 바로 보내지 않고, '암호화 완료' 후 전송하는 것처럼 시뮬레이션
   ========================================================= */

int LED_PROCESS = 8;  // 암호화/처리 중
int LED_SEND    = 9;  // 전송 완료

void setup() {
  pinMode(LED_PROCESS, OUTPUT);
  pinMode(LED_SEND, OUTPUT);

  Serial.begin(9600);
  Serial.println("Privacy Mode: 데이터 암호화/보안 우선");
}

void loop() {
  // 새 데이터가 생겼다고 가정
  Serial.println("새 데이터 생성 → 암호화 시작");
  digitalWrite(LED_PROCESS, HIGH);
  digitalWrite(LED_SEND, LOW);
  delay(1000);

  // 암호화 완료 후 전송
  Serial.println("암호화 완료 → 안전하게 전송");
  digitalWrite(LED_PROCESS, LOW);
  digitalWrite(LED_SEND, HIGH);
  delay(1000);

  // 다음 데이터까지 대기
  digitalWrite(LED_PROCESS, LOW);
  digitalWrite(LED_SEND, LOW);
  delay(1000);
}
"""
        arduino_code = template.replace("{title}", title)

    else:
        arduino_code = "// TODO: 이 사생활 이슈에 대한 코드를 추가로 설계해 보세요."


# 4) 사고(Safety & Accident) 카테고리 – 트롤리 딜레마/약자 우선 등
elif category.startswith("사고"):

    # 보행자 vs 탑승자 보호
    if issue_id == "acc_1":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 보행자 vs 탑승자 보호
   이슈: {title}
   설명: '보행자 보호 우선'을 구현한 예시.
        앞에 보행자(초음파), 옆에는 벽(차량)이라고 가정하고
        보행자 쪽을 피하는 방향으로 조향
   ========================================================= */

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

int TRIG_FRONT = 2;   // 앞(보행자)
int ECHO_FRONT = 3;
int TRIG_SIDE  = 7;   // 옆(차량/벽)
int ECHO_SIDE  = 8;

const int DANGER_DIST = 20;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

long getDist(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_SIDE, OUTPUT);
  pinMode(ECHO_SIDE, INPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 보행자 보호 우선");
}

void loop() {
  long dFront = getDist(TRIG_FRONT, ECHO_FRONT);
  long dSide  = getDist(TRIG_SIDE, ECHO_SIDE);

  // 앞에 보행자가 가까우면, 옆으로 피하는 선택
  if (dFront > 0 && dFront < DANGER_DIST) {
    // 보행자 쪽으로 돌지 않고, 반대 방향으로 회피
    motor(-150, 150);
    delay(500);
    motor(0, 0);
  }
  else {
    // 평소에는 천천히 앞으로 이동 (예시)
    motor(120, 120);
    delay(100);
  }
}
"""
        arduino_code = template.replace("{title}", title)

    # 1명 vs 다수 보호
    elif issue_id == "acc_2":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 1명 vs 다수 보호
   이슈: {title}
   설명: 좌측/우측에 '사람 수'를 센서 값으로 가정.
        더 적은 쪽으로 피하는(전체 피해 최소화) 예시
   ========================================================= */

// 예시: 포텐셔미터/스위치로 '왼쪽 사람 수', '오른쪽 사람 수'를 입력한다고 가정

int POT_LEFT  = A0;  // 왼쪽 사람 수 (0~1023)
int POT_RIGHT = A1;  // 오른쪽 사람 수

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 1명 vs 다수 보호 (다수 보호 우선)");
}

void loop() {
  int leftVal  = analogRead(POT_LEFT);
  int rightVal = analogRead(POT_RIGHT);

  int leftPeople  = map(leftVal,  0, 1023, 0, 5);
  int rightPeople = map(rightVal, 0, 1023, 0, 5);

  Serial.print("왼쪽 사람: ");
  Serial.print(leftPeople);
  Serial.print(" / 오른쪽 사람: ");
  Serial.println(rightPeople);

  if (leftPeople < rightPeople) {
    // 왼쪽으로 피한다(왼쪽 피해가 적음)
    motor(-150, 150);
    delay(500);
  } else if (rightPeople < leftPeople) {
    // 오른쪽으로 피한다
    motor(150, -150);
    delay(500);
  } else {
    // 같으면 정지 or 직진 (여기서는 정지)
    motor(0, 0);
    delay(500);
  }
}
"""
        arduino_code = template.replace("{title}", title)

    # 약자 우선 보호
    elif issue_id == "acc_3":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 약자 우선 보호
   이슈: {title}
   설명: '어린이/노인/장애인'을 우선 보호한다는 개념을
        단순하게 '약자 센서' vs '일반 센서'로 나누어 표현
   ========================================================= */

int TRIG_WEAK = 2;  // 약자(어린이 등) 위치
int ECHO_WEAK = 3;
int TRIG_NORMAL = 7; // 일반 성인 위치
int ECHO_NORMAL = 8;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

const int DANGER_DIST = 20;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

long getDist(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG_WEAK, OUTPUT);
  pinMode(ECHO_WEAK, INPUT);
  pinMode(TRIG_NORMAL, OUTPUT);
  pinMode(ECHO_NORMAL, INPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 약자 우선 보호");
}

void loop() {
  long dWeak   = getDist(TRIG_WEAK, ECHO_WEAK);
  long dNormal = getDist(TRIG_NORMAL, ECHO_NORMAL);

  if (dWeak > 0 && dWeak < DANGER_DIST) {
    // 약자가 가까우면 그 쪽으로 가지 않도록 회피
    motor(-150, 150);
    delay(500);
  } else if (dNormal > 0 && dNormal < DANGER_DIST) {
    // 일반인이 가까우면, 다른 방향으로 회피
    motor(150, -150);
    delay(500);
  } else {
    // 위험 없으면 직진 (예시)
    motor(130, 130);
    delay(100);
  }
}
"""
        arduino_code = template.replace("{title}", title)

    # 동물 vs 사람
    elif issue_id == "acc_4":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 동물 vs 사람
   이슈: {title}
   설명: '사람 우선'을 구현한 예시.
        앞 센서 2개를 사람/동물로 가정하고,
        사람이 있으면 사람을 우선 피하도록 설계
   ========================================================= */

int TRIG_HUMAN = 2;
int ECHO_HUMAN = 3;
int TRIG_ANIMAL = 7;
int ECHO_ANIMAL = 8;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

const int DANGER_DIST = 20;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

long getDist(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG_HUMAN, OUTPUT);
  pinMode(ECHO_HUMAN, INPUT);
  pinMode(TRIG_ANIMAL, OUTPUT);
  pinMode(ECHO_ANIMAL, INPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 사람 우선 (동물 vs 사람)");
}

void loop() {
  long dHuman  = getDist(TRIG_HUMAN, ECHO_HUMAN);
  long dAnimal = getDist(TRIG_ANIMAL, ECHO_ANIMAL);

  if (dHuman > 0 && dHuman < DANGER_DIST) {
    // 사람을 피하는 방향으로 이동
    motor(-150, 150);
    delay(500);
  } else if (dAnimal > 0 && dAnimal < DANGER_DIST) {
    // 동물도 가능하면 피하려고 노력
    motor(150, -150);
    delay(500);
  } else {
    motor(130, 130);
    delay(100);
  }
}
"""
        arduino_code = template.replace("{title}", title)

    # 2차 사고 고려
    elif issue_id == "acc_5":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 2차 사고 고려
   이슈: {title}
   설명: 앞 장애물을 피하려다 옆 차선과 충돌할 위험이 더 크면,
        앞 장애물과의 충돌을 감수할지 여부를 판단하는 예시
   ========================================================= */

int TRIG_FRONT = 2;
int ECHO_FRONT = 3;
int TRIG_SIDE  = 7;
int ECHO_SIDE  = 8;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

const int FRONT_DANGER = 15;
const int SIDE_DANGER  = 10;

void motor(int L, int R) {
  if (L > 0) { analogWrite(L1, L); analogWrite(L2, 0); }
  else if (L < 0) { analogWrite(L1, 0); analogWrite(L2, -L); }
  else { analogWrite(L1, 0); analogWrite(L2, 0); }

  if (R > 0) { analogWrite(R1, R); analogWrite(R2, 0); }
  else if (R < 0) { analogWrite(R1, 0); analogWrite(R2, -R); }
  else { analogWrite(R1, 0); analogWrite(R2, 0); }
}

long getDist(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_SIDE, OUTPUT);
  pinMode(ECHO_SIDE, INPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 2차 사고 고려");
}

void loop() {
  long dFront = getDist(TRIG_FRONT, ECHO_FRONT);
  long dSide  = getDist(TRIG_SIDE, ECHO_SIDE);

  if (dFront > 0 && dFront < FRONT_DANGER) {
    // 앞이 위험하지만, 옆 차선이 더 위험하면 회피하지 않고 멈추기
    if (dSide > 0 && dSide < SIDE_DANGER) {
      // 옆에 차가 너무 가까우면 급회피 X, 정지
      motor(0, 0);
      delay(500);
    } else {
      // 옆이 상대적으로 여유 있으면 회피
      motor(-150, 150);
      delay(500);
    }
  } else {
    motor(130, 130);
    delay(100);
  }
}
"""
        arduino_code = template.replace("{title}", title)

    # 급정지와 뒤차 사고
    elif issue_id == "acc_6":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 급정지와 뒤차 사고
   이슈: {title}
   설명: 앞의 위험과 뒤차와의 거리 둘 다 고려해서,
        완전 급정지 vs 강한 감속을 선택하는 예시
   ========================================================= */

int TRIG_FRONT = 2;
int ECHO_FRONT = 3;
int TRIG_BACK  = 7;
int ECHO_BACK  = 8;

int L1 = 5;
int L2 = 6;
int R1 = 9;
int R2 = 10;

const int FRONT_DANGER = 15;
const int BACK_TOO_CLOSE = 10;

int currentSpeed = 0;
const int TARGET_SPEED = 150;
const int DEC_STRONG   = 40;
const int DEC_SOFT     = 15;
const int ACC_STEP     = 5;

void motorDrive(int speed) {
  if (speed < 0) speed = 0;
  if (speed > 255) speed = 255;
  analogWrite(L1, speed);
  analogWrite(L2, 0);
  analogWrite(R1, speed);
  analogWrite(R2, 0);
}

long getDist(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration / 58;
}

void setup() {
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);

  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_BACK, OUTPUT);
  pinMode(ECHO_BACK, INPUT);

  Serial.begin(9600);
  Serial.println("Accident Mode: 급정지 vs 뒤차 사고 고려");
}

void loop() {
  long dFront = getDist(TRIG_FRONT, ECHO_FRONT);
  long dBack  = getDist(TRIG_BACK, ECHO_BACK);

  if (dFront > 0 && dFront < FRONT_DANGER) {
    // 앞이 위험한데 뒤차가 멀면 → 급정지(강한 감속)
    if (dBack == 0 || dBack > BACK_TOO_CLOSE) {
      currentSpeed -= DEC_STRONG;
      if (currentSpeed < 0) currentSpeed = 0;
    }
    // 앞이 위험하지만 뒤차도 너무 가까우면 → 완전 급정지 대신 완만 감속
    else {
      currentSpeed -= DEC_SOFT;
      if (currentSpeed < 0) currentSpeed = 0;
    }
  } else {
    // 위험 없으면 서서히 목표 속도까지 가속
    if (currentSpeed < TARGET_SPEED) currentSpeed += ACC_STEP;
    if (currentSpeed > TARGET_SPEED) currentSpeed = TARGET_SPEED;
  }

  motorDrive(currentSpeed);
  delay(50);
}
"""
        arduino_code = template.replace("{title}", title)

    # 사고 책임 주체
    elif issue_id == "acc_7":
        template = """\
/* =========================================================
   RC카 사고 윤리 + 사고 책임 주체
   이슈: {title}
   설명: 코드에는 '누가 설정을 했는지' 로그를 남겨,
        책임 소재(개발자 vs 사용자)를 토론할 수 있게 하는 예시
   ========================================================= */

String developer = "Dev_A";  // 개발자 이름 예시
String userName  = "User_A"; // 사용자 이름 예시

void setup() {
  Serial.begin(9600);
  Serial.println("Accident Mode: 사고 책임 주체");
  Serial.println("==== 시스템 설정 정보 ====");
  Serial.print("개발자: ");
  Serial.println(developer);
  Serial.print("사용자: ");
  Serial.println(userName);
  Serial.println("===========================");
}

void loop() {
  // 실제 주행/사고 로직이 있다면 여기에서 로그를 남길 수 있음.
  // 예)
  // Serial.println("충돌 발생! 설정자 기록: " + userName);

  delay(1000);
}
"""
        arduino_code = template.replace("{title}", title)

    else:
        arduino_code = "// TODO: 이 사고 이슈에 대한 코드를 추가로 설계해 보세요."

# 그 밖의 예외
else:
    arduino_code = "// 알 수 없는 카테고리/이슈입니다."


# 5) 화면에 코드 출력
st.code(arduino_code, language="c")

st.markdown("""
1. 위 코드를 **전체 복사**해서 아두이노 IDE 새 스케치에 붙여 넣고,  
2. 보드/포트를 설정한 뒤 업로드하면,  
3. 지금 선택한 윤리 이슈(예: *보행자 우선*, *탑승자 우선*, *어린이 보호구역*, *민감 구역 촬영*, *1명 vs 다수 보호* 등)에 맞는 행동만 실행돼요 🚗  
""")