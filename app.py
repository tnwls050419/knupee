import streamlit as st
if st.session_state.login =='':
    st.error('로그인을 먼저해')

def filteringApp(df,userid):
    if userid == 'zxcvb':
        return df
    else:
       return df[df['userid']==userid]

if st.session_state.login != '':
    if st.sidebar.button('로그아웃'):
         st.session_state.login = ''
    

    # ---------------------------
    # 2. 페이지 제목 및 수업 개요
    # ---------------------------
    st.title("1차시 : 자율주행자동차의 등장")

    st.markdown(
        """
    **수업 흐름 요약**

    1. 도입 : 전시학습확인/흥미유발/학습목표제시 
    2. 전개 : 활동 1 + 활동 2 + 활동 3 
    3. 정리 : 형성 평가 및 다음 차시 예고
    """
    )

    st.markdown("---")

    # ---------------------------
    # 3. 도입 / 전개 / 정리 탭 나누기
    # ---------------------------
    tab_intro, tab_develop, tab_summary = st.tabs(["도입", "전개", "정리"])

    # ===========================
    # [탭 1] 도입
    # ===========================
    with tab_intro:
        st.subheader("🔹 도입 : 전시학습확인/흥미유발/학습목표제시")

        st.write(
            """
    수업을 시작하기 전에, 짧은 영상이나 이미지를 보여주고  
    학생들에게 생각을 묻는 '발문'을 던지는 공간입니다.
    (여기 내용은 나중에 수업 주제에 맞게 바꿔 쓰면 돼!)
    """
        )

        st.markdown("---")

        # 1-1. 도입 영상
        st.markdown("#### 1) 영상 시청")
        video_url = "https://vodm.tsherpa.co.kr/vod/_definst_/mp4:202455/M202455525_800k.mp4/playlist.m3u8"  # 👉 수업 영상 링크로 교체
        st.video(video_url)

        st.markdown("---")

        # 1-2. 발문
        st.markdown("#### 2) 발문")
        st.markdown(
            """
    발문 1) 자율주행 자동차가 스스로 멈추거나 방향을 바꾸는 걸 본 적이 있나요?  
    발문 2) 그렇다면 이런 자율주행 자동차의 ‘판단력’은 어떻게 만들어질까요?                   
    발문 3) 인공지능의 원리와 센서가 어떤 역할을 하는지 함께 알아볼까요?
    """
        )

        st.markdown("---")
        
        # 1-3. 학습 목표
        st.markdown("#### 3) 오늘의 학습 목표")

        col1 = st.columns(1)[0]   # ← 리스트에서 첫 번째 요소만 가져오기
        with col1:
            st.markdown(
                """
        1. 인공지능의 개념과 원리를 이해한다 
        2. 인공지능 센서를 기반으로한 지능적 판단과정을 탐구한다.
        """
            )

        st.markdown("---")

        # 1-4. 교사용 메모
        with st.expander("AI (Tech) 및 유의점"):
            st.write(
                """
    - 도입 목표: 학생들이 '자율주행'을 일상과 연결해서 흥미를 느끼게 한다.
    - 예상 학생 반응: '무섭다', '신기하다', '사고 나면 어떡해요?' 등
    - 추가 질문: '그럼 그런 위험을 줄이려면 어떤 규칙/기술이 필요할까?'
    """
            )

    # ===========================
    # [탭 2] 전개
    # ===========================
    with tab_develop:
        st.subheader("🔹 전개 : 활동1 + 활동2 + 활동3 + 활동4")

        # 2-1. 모둠 활동 안내
        st.markdown("#### 1) AI 개념 이해하기 ")

        st.markdown(
            """
    **데이터 수집 → 분석 → 지능적 판단 과정으로 이루어진 AI의 작동 원리를 자율주행 자동차 사례로 학습한다.**

    """
        )

        st.markdown("---")

        # 2-2. 개념 학습
        st.markdown("#### 2) 센서의 종류와 원리 탐구")

        with st.expander("자율주행에서 사용하는 라이다, 레이더, 카메라 센서의 역할과 원리"):
            st.markdown(
                """
                - 라이다: 빛(레이저) 반사로 거리 측정                      
                - 레이더: 전파 반사로 거리/속도 측정                          
                - 카메라: 영상 인식으로 사물 및 차선 인식
                
                """
            )

        st.markdown("###### 교사 발문 예시")

        st.write(
            """
    (발문 1) 왜 자율주행 자동차는 센서를 여러 가지 사용하는 걸까요?                             
    (발문 2) 각 센서의 장단점을 비교해볼까요?)
    """
        )
    
        st.markdown("---")

        # 2-4. 실습 체크리스트
        st.markdown("#### 3) 모둠별 학습지 작성 ")
        st.markdown(
            """
    **모둠별로 탐구한 내용을 학습지에 정리하고 자율주행 AI의 판단 과정에 어떤 센서들이 어떤 역할을 하는지 정리한다.**
    """)
        
        step1 = st.checkbox("1단계: 오늘 배운 개념(자율주행 + AI 역할) 정리하기", key="step1")
        step2 = st.checkbox("2단계: 모둠별 상황 카드 작성 완료", key="step2")
        step3 = st.checkbox("3단계: 다른 모둠 상황 카드에 대한 해결 방안 토의", key="step3")

        st.markdown("---")

        # 2-5. 전개 파트 한 줄 소감
        st.markdown("#### 4) 발표 및 피드백")
        reflection_mid = st.text_input("모둠별로 정리한 내용을 발표", key="reflection_mid")

        st.markdown("---")

        # 2-6. 교사용 메모
        with st.expander("교사용 : 발표 내용을 기반으로 피드백 제공"):
            st.write(
                """
    - 센서의 원리 설명이 정확한가?
    - AI 판단 과정과의 연계가 잘 드러나는가?
    - 표현이 명확하고 논리적인가?
    """
            )

        st.markdown("---")

    # ===========================
    # [탭 3] 정리
    # ===========================
    with tab_summary:
        st.subheader("🔹 정리 : 형성 평가 및 다음 차시 예고")

        # 3-1 활동 (정리용)
        st.markdown("#### 1) 오늘 배운 내용 정리")

        col_a, col_b = st.columns(2)

        with col_a:
            three_things = st.text_area("1) 오늘 새로 알게 된 점", key="three_things", height=120)
        with col_b:
            two_questions = st.text_area("2) 더 알고 싶은 점", key="two_questions", height=120)
       
        st.markdown("---")

        # 3-3. 자기 평가 슬라이더
        st.markdown("#### 2) 자기 평가")

        self_score = st.slider(
            "오늘 수업 내용을 얼마나 이해했다고 느끼나요?",
            min_value=0,
            max_value=10,
            value=7,
            step=1,
            key="self_score",
        )
        st.write(f"👉 자기 평가 점수 : **{self_score} / 10**")

        st.markdown("---")

        # 3-4. 다음 차시 예고
        st.markdown("#### 3) 다음 차시 예고")

        st.info(
            """
    **2차시 '컴퓨터 비전' 예고**  
    - 컴퓨터 비전의 이해와 활용 사례을 조사한다.
    - 컴퓨터 비전 객체 탐지 기술을 이해한다.
    """
        )

        activity_idea = st.text_area(
            "수업 내용 필기",
            key="activity_idea",
            height=120,
        )

        st.markdown("---")

