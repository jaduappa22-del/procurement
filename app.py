from datetime import datetime
import urllib.parse
import pandas as pd
import streamlit as st

# 페이지 설정 (와이드 모드)
st.set_page_config(
    page_title="GLOBAL PROCUREMENT DESK — 자재구매 인텔리전스",
    page_icon="🏭",
    layout="wide",
)

# 하이엔드 구매 다크/라이트 하이브리드 스타일 CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .hero-banner { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 35px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2); }
    .card { background-color: #ffffff; padding: 24px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-bottom: 20px; }
    .section-title { font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
    .metric-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 16px; border-radius: 10px; text-align: center; }
    .incoterms-card { background: #eff6ff; border: 1px solid #bfdbfe; padding: 14px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 상단 히어로 배너
st.markdown("""
    <div class="hero-banner">
        <span style="background-color: #3b82f6; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;">PROCUREMENT INTELLIGENCE DESK</span>
        <h1 style="margin: 10px 0 6px 0; font-size: 28px; font-weight: 900;">🏭 글로벌 원자재 시세 및 공급망 인텔리전스</h1>
        <p style="margin: 0; color: #94a3b8; font-size: 14px;">공신력 있는 기관의 원자재 가격 추이, 실시간 환율 계산, 인코텀즈 2020 가이드 및 스프레드시트 연동 허브입니다.</p>
    </div>
""", unsafe_allow_html=True)

# 사이드바 설정 허브
st.sidebar.markdown("### ⚙️ 구매 및 환율 설정")
target_currency = st.sidebar.selectbox(
    "결제 통화 선택", ["USD ($)", "EUR (€)", "JPY (¥ 100엔당)", "CNY (¥)"]
)
custom_exchange_rate = st.sidebar.number_input(
    "적용 환율 (원화 기준 입력)",
    min_value=1.0,
    value=1350.0 if "USD" in target_currency else 1450.0,
    step=10.0,
)
sheet_mode = st.sidebar.radio(
    "데이터 소스 연동 모드",
    ["기본 내장 데이터 (Standard)", "구글 스프레드시트 연동 (Live CSV)"],
)

if sheet_mode == "구글 스프레드시트 연동 (Live CSV)":
  sheet_csv_url = st.sidebar.text_input(
      "구글 시트 CSV 내보내기 URL 입력",
      placeholder=(
          "https://docs.google.com/spreadsheets/d/.../export?format=csv"
      ),
  )

# 메인 레이아웃 분할 (좌: 원자재 및 시세 / 우: 무역 상식 및 인코텀즈)
col_left, col_right = st.columns([1.6, 1.2])

with col_left:
  # 1. 주요 원자재 가격 추이 및 공신력 있는 출처 표기
  st.markdown(
      '<div class="card"><div class="section-title">📈 주요 원자재 가격 추이 및'
      " 시장 지표</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p style="font-size: 12px; color: #64748b; margin-top: -10px;'
      ' margin-bottom: 14px;">출처 공신력 기관: 조달청 비축물자웹사이트, 한국수입협회'
      " (KOIMA 국제원자재가격정보), LME(런던금속거래소)</p>",
      unsafe_allow_html=True,
  )

  # 원자재 샘플 데이터 (스프레드시트 연동 시 대체 가능)
  raw_materials_data = {
      "원자재 품목": [
          "구리 (Copper 3M)",
          "알루미늄 (Aluminum)",
          "니켈 (Nickel 3M)",
          "두바이유 (Dubai Crude)",
      ],
      "단위": ["톤(MT)", "톤(MT)", "톤(MT)", "배럴(BBL)"],
      "국제 시세 (USD)": ["$9,420.00", "$2,450.00", "$16,350.00", "$78.40"],
      "전주 대비 등락률": ["+1.4%", "-0.8%", "+2.3%", "-1.5%"],
      "시장 상태": ["상승세 📈", "보합세 ➡️", "급등 주의 🚨", "하락세 📉"],
  }
  df_materials = pd.DataFrame(raw_materials_data)
  st.dataframe(df_materials, use_container_width=True, hide_index=True)

  # 2. 관련 핵심 경제/원자재 뉴스 및 기사 큐레이션
  st.markdown(
      '<div class="card"><div class="section-title">📰 최신 공급망 및 원자재 관련'
      " 핵심 기사 큐레이션</div>",
      unsafe_allow_html=True,
  )
  articles = [
      {
          "title": (
              "글로벌 공급망 리스크 완화 조짐... 주요 비철금속 가격 변동성"
              " 주목"
          ),
          "source": "한국경제 원자재 데스크",
          "date": "2026-09-05",
          "url": "https://datacenter.hankyung.com/commodities",
      },
      {
          "title": "조달청, 주요 원자재 비축 물량 방출 및 수급 안정화 대책 발표",
          "source": "조달청 보도자료",
          "date": "2026-09-04",
          "url": "https://www.pps.go.kr",
      },
  ]

  for art in articles:
    st.markdown(
        f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b;"><a href="{art['url']}" target="_blank" style="color: #2563eb; text-decoration: none;">{art['title']}</a></div>
                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">출처: {art['source']} | 일자: {art['date']}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  st.markdown("</div>", unsafe_allow_html=True)

with col_right:
  # 3. 무역 실무 가이드: 인코텀즈 (Incoterms 2020) 핵심 요약
  st.markdown(
      '<div class="card"><div class="section-title">🌐 무역 실무 & 인코텀즈'
      " (Incoterms 2020)</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      """
        <div class="incoterms-card">
            <b>🚢 FOB (Free on Board / 본선인도조건)</b><br>
            <span style="font-size: 12px; color: #334155;">매도인이 화물을 지정 선박에 적재할 때까지의 비용과 위험을 부담. 이후 비용은 매수인 부담.</span>
        </div>
        <div class="incoterms-card" style="background: #f0fdf4; border-color: #bbf7d0;">
            <b>⚓ CIF (Cost, Insurance and Freight / 운임·보험료포함인도조건)</b><br>
            <span style="font-size: 12px; color: #334155;">매도인이 목적지 항구까지의 운임과 적화 보험료를 모두 부담하는 조건.</span>
        </div>
        <div class="incoterms-card" style="background: #fef2f2; border-color: #fecaca;">
            <b>🏭 EXW (Ex Works / 공장인도조건)</b><br>
            <span style="font-size: 12px; color: #334155;">매도인의 공장에서 화물을 인수하는 조건으로, 매수인이 수출 통관부터 모든 비용과 위험을 책임짐.</span>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown("</div>", unsafe_allow_html=True)

  # 4. 실시간 구매 예산 / 단가 환산 계산기
  st.markdown(
      '<div class="card"><div class="section-title">🧮 외화 자재 단가 원화 환산기</div>',
      unsafe_allow_html=True,
  )
  unit_price_foreign = st.number_input(
      "외화 기준 단가 입력", min_value=0.0, value=1500.0, step=10.0
  )
  quantity = st.number_input("구매 수량 (QTY)", min_value=1, value=500, step=10)

  # 환산 로직
  if "JPY" in target_currency:
    total_krw = (unit_price_foreign / 100) * custom_exchange_rate * quantity
  else:
    total_krw = unit_price_foreign * custom_exchange_rate * quantity

  st.metric(label="총 환산 예상 금액 (KRW)", value=f"{total_krw:,.0f} 원")
  st.markdown(
      f"<div style='font-size: 12px; color: #64748b; text-align: right;'>적용"
      f" 환율: 1 {target_currency.split(' ')[0]} = {custom_exchange_rate:,.1f}"
      " KRW</div>",
      unsafe_allow_html=True,
  )
  st.markdown("</div>", unsafe_allow_html=True)
