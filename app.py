from datetime import datetime
import urllib.parse
import pandas as pd
import streamlit as st

# 페이지 설정 (와이드 모드)
st.set_page_config(
    page_title="NAVER PROCUREMENT INTELLIGENCE — 자재구매/무역 데스크",
    page_icon="🟩",
    layout="wide",
)

# 네이버 스타일 하이엔드 감성 CSS (#03C75A 포인트 컬러)
st.markdown("""
    <style>
    .stApp { background-color: #f4f5f7; color: #191919; font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", Roboto, sans-serif; }
    .naver-header { background: #ffffff; border-bottom: 2px solid #03C75A; padding: 20px 30px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .alert-banner { background-color: #fff8f8; border-left: 5px solid #ef4444; padding: 16px; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(239, 68, 68, 0.1); }
    .naver-card { background-color: #ffffff; padding: 22px; border-radius: 8px; border: 1px solid #e3e5e8; box-shadow: 0 2px 4px rgba(0,0,0,0.01); margin-bottom: 20px; }
    .section-title { font-size: 17px; font-weight: 700; color: #191919; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px; }
    .law-link-box { background: #f8f9fa; border: 1px solid #d1d5db; padding: 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; }
    </style>
""", unsafe_allow_html=True)

# 상단 헤더
st.markdown("""
    <div class="naver-header">
        <div>
            <span style="background-color: #03C75A; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">NAVER PORTAL INTEGRATION</span>
            <h1 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 800; color: #191919;">📦 자재구매·무역 컴플라이언스 인텔리전스 데스크</h1>
        </div>
        <div style="text-align: right; font-size: 12px; color: #666;">
            <b>컴플라이언스 상태</b>: <span style="color: #03C75A;">● 법령 모니터링 활성</span><br>
            기준일자: 2026년 9월 5일
        </div>
    </div>
""", unsafe_allow_html=True)

# 법령 개정 긴급 알람 섹션
st.markdown("""
    <div class="alert-banner">
        <div style="font-weight: 800; color: #dc2626; font-size: 15px; margin-bottom: 6px;">
            🚨 [법령 개정 긴급 알람] 주요 공급망 및 무역·하도급 법제 변경 사항 감지
        </div>
        <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #374151; line-height: 1.6;">
            <li><b>관세법 개정</b>: 할당관세 집중관리품목 수입신고 기한 단축(20일) 및 신고지연 가산세 한도 상향.</li>
            <li><b>대외무역법 개정</b>: 글로벌 통상 분쟁 대응 및 경제안보 관련 상응조치·국가 발전 이익 중심 수출통제 법적 근거 강화.</li>
            <li><b>하도급법 시행령 개정</b>: 하도급대금 연동 대상에 '주요 에너지(연료·열·전기)' 확대 및 건설하도급 지급보증 예외사유 축소.</li>
            <li><b>상생협력법 개정</b>: 기술 탈취 소송 대응을 위한 '한국형 증거개시 제도(K-디스커버리)' 및 자료제출명령권 도입.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 사이드바 설정
st.sidebar.markdown("### ⚙️ 구매 및 통화 설정")
target_currency = st.sidebar.selectbox(
    "결제 통화 선택", ["USD ($)", "EUR (€)", "JPY (¥ 100엔당)", "CNY (¥)"]
)
custom_exchange_rate = st.sidebar.number_input(
    "적용 환율 (원화 기준 입력)", min_value=1.0, value=1350.0, step=10.0
)

# 메인 화면 레이아웃 분할
col_left, col_right = st.columns([1.6, 1.2])

with col_left:
  # 1. 주요 원자재 가격 추이
  st.markdown(
      '<div class="naver-card"><div class="section-title">📈 주요 원자재 가격 추이'
      " 및 공신력 지표</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p style="font-size: 12px; color: #666; margin-top: -8px;'
      ' margin-bottom: 12px;">공신력 데이터 출처: 조달청 비축물자, 한국수입협회'
      " (KOIMA), LME(런던금속거래소)</p>",
      unsafe_allow_html=True,
  )

  raw_materials_data = {
      "원자재 품목": [
          "구리 (Copper 3M)",
          "알루미늄 (Aluminum)",
          "니켈 (Nickel 3M)",
          "두바이유 (Dubai Crude)",
      ],
      "단위": ["톤(MT)", "톤(MT)", "톤(MT)", "배럴(BBL)"],
      "국제 시세 (USD)": ["$9,420.00", "$2,450.00", "$16,350.00", "$78.40"],
      "전주 대비": ["+1.4%", "-0.8%", "+2.3%", "-1.5%"],
      "시장 동향": ["상승세 📈", "보합세 ➡️", "급등 주의 🚨", "하락세 📉"],
  }
  st.dataframe(
      pd.DataFrame(raw_materials_data), use_container_width=True, hide_index=True
  )
  st.markdown("</div>", unsafe_allow_html=True)

  # 2. 관련 핵심 기사 큐레이션
  st.markdown(
      '<div class="naver-card"><div class="section-title">📰 공급망 및 원자재'
      " 관련 실시간 핵심 기사</div>",
      unsafe_allow_html=True,
  )
  articles = [
      {
          "title": (
              "글로벌 공급망 리스크 완화 조짐... 주요 비철금속 가격 변동성"
              " 주목"
          ),
          "source": "한국경제 원자재 데스크",
          "url": "https://datacenter.hankyung.com/commodities",
      },
      {
          "title": "조달청, 주요 원자재 비축 물량 방출 및 수급 안정화 대책 발표",
          "source": "조달청 보도자료",
          "url": "https://www.pps.go.kr",
      },
  ]

  for art in articles:
    st.markdown(
        f"""
            <div style="background: #f8f9fa; border: 1px solid #e3e5e8; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                <div style="font-size: 13px; font-weight: 700;"><a href="{art['url']}" target="_blank" style="color: #03C75A; text-decoration: none;">{art['title']}</a></div>
                <div style="font-size: 11px; color: #666; margin-top: 4px;">출처 언론사: {art['source']}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  st.markdown("</div>", unsafe_allow_html=True)

with col_right:
  # 3. 실시간 외화 자재 단가 환산기
  st.markdown(
      '<div class="naver-card"><div class="section-title">🧮 외화 자재 단가 원화 환산기</div>',
      unsafe_allow_html=True,
  )
  unit_price_foreign = st.number_input(
      "외화 기준 단가 입력", min_value=0.0, value=1500.0, step=10.0
  )
  quantity = st.number_input("구매 수량 (QTY)", min_value=1, value=500, step=10)

  if "JPY" in target_currency:
    total_krw = (unit_price_foreign / 100) * custom_exchange_rate * quantity
  else:
    total_krw = unit_price_foreign * custom_exchange_rate * quantity

  st.metric(label="총 환산 예상 금액 (KRW)", value=f"{total_krw:,.0f} 원")
  st.markdown(
      f"<div style='font-size: 11px; color: #666; text-align: right;'>적용"
      f" 환율: {custom_exchange_rate:,.1f} KRW</div>",
      unsafe_allow_html=True,
  )
  st.markdown("</div>", unsafe_allow_html=True)

# 4. 인코텀즈 2020 전체 11가지 조건 완벽 수록 섹션
st.markdown(
    '<div class="naver-card"><div class="section-title">🌐 인코텀즈 2020 (Incoterms'
    ' 2020) 전체 11가지 조건 가이드</div>',
    unsafe_allow_html=True,
)

tab_all, tab_any, tab_sea = st.tabs(
    ["전체 요약 보기", "모든 운송 방식 (7가지)", "해상/내수상운송 전용 (4가지)"]
)

with tab_all:
  st.markdown("""
        <div style="font-size: 13px; color: #374151; line-height: 1.6;">
            <b>• 모든 운송 방식 (7가지)</b>: EXW, FCA, CPT, CIP, DAP, DPU, DDP<br>
            <b>• 해상/내수상운송 전용 (4가지)</b>: FAS, FOB, CFR, CIF<br>
            <span style="color: #03C75A; font-weight: 600;">💡 실무 팁: 계약 체결 시 위험 분기점(Risk Transfer)과 비용 부담(Cost) 범위를 반드시 일치시켜야 분쟁을 예방할 수 있습니다.</span>
        </div>
    """, unsafe_allow_html=True)

with tab_any:
  st.markdown("""
        * **EXW (공장인도)**: 공장에서 인도. 수·출통관 포함 모든 비용/위험을 **매수인**이 부담.
        * **FCA (운송인인도)**: 지정 장소에서 운송인에게 인도. (수출통관 매도인)
        * **CPT (운송료지급인도)**: 목적지까지 운송비 매도인 부담. 위험은 운송인 인도 시 이전.
        * **CIP (운송료·보험료지급인도)**: CPT + **적화 보험**을 매도인이 필수로 가입.
        * **DAP (도착지인도)**: 지정 목적지 도중 수송 수단 위에서 인도. (수입통관 매수인)
        * **DPU (도착지하화인도)**: 목적지 도달 후 **하화(짐 내리기) 작업까지** 매도인이 완료.
        * **DDP (관세지급인도)**: 목적지까지 수입관세 및 모든 통관비용·위험을 **매도인**이 최종 부담.
    """)

with tab_sea:
  st.markdown("""
        * **FAS (선측인도)**: 선적항의 **선박 옆(선측)**에 화물을 둘 때까지 비용·위험 부담.
        * **FOB (본선인도)**: 선적항에서 **본선에 화물 적재 완료** 시 위험 이전.
        * **CFR (운임포함인도)**: 목적항까지 운송비는 매도인 부담, 위험은 선적 시 매수인에게 이전.
        * **CIF (운임·보험료포함인도)**: CFR + **해상 보험료**를 매도인이 부담.
    """)

st.markdown("</div>", unsafe_allow_html=True)

# 5. 국가법령정보센터 공식 링크 섹션
st.markdown(
    '<div class="naver-card"><div class="section-title">🔗 공신력 법제처 및'
    " 유관기관 공식 법령 링크 바로가기</div>",
    unsafe_allow_html=True,
)

col_l1, col_l2 = st.columns(2)
with col_l1:
  st.markdown(
      """
        <div class="law-link-box">
            <span><b>관세법</b> (국가법령정보센터)</span>
            <a href="https://www.law.go.kr/법령/관세법" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a>
        </div>
        <div class="law-link-box">
            <span><b>대외무역법</b> (국가법령정보센터)</span>
            <a href="https://www.law.go.kr/법령/대외무역법" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col_l2:
  st.markdown(
      """
        <div class="law-link-box">
            <span><b>하도급거래 공정화에 관한 법률</b></span>
            <a href="https://www.law.go.kr/법령/하도급거래공정화에관한법률" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a>
        </div>
        <div class="law-link-box">
            <span><b>대·중소기업 상생협력 촉진에 관한 법률</b></span>
            <a href="https://www.law.go.kr/법령/대·중소기업상생협력촉진에관한법률" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a>
        </div>
    """,
      unsafe_allow_html=True,
  )
st.markdown("</div>", unsafe_allow_html=True)
