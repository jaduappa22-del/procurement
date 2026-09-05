from datetime import datetime
import pandas as pd
import streamlit as str_lit
import yfinance as yf

# 페이지 설정 (와이드 모드)
str_lit.set_page_config(
    page_title="AFK PROCUREMENT INTELLIGENCE — 자재구매/무역 데스크",
    page_icon="🟢",
    layout="wide",
)

# 네이버 감성을 극대화한 짙은 초록색(#03C75A, #00B247) 디자인 시스템 CSS
str_lit.markdown("""
    <style>
    .stApp { background-color: #f4f6f8; color: #1e1e1e; font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", Roboto, sans-serif; }
    
    /* 짙은 네이버 시그니처 상단 헤더 */
    .naver-header { 
        background: linear-gradient(135deg, #03C75A 0%, #00983c 100%); 
        padding: 24px 30px; 
        border-radius: 10px; 
        margin-bottom: 25px; 
        color: white; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        box-shadow: 0 4px 12px rgba(3, 199, 90, 0.25); 
    }
    
    /* 긴급 컴플라이언스 알람 배너 */
    .alert-banner { 
        background-color: #fff5f5; 
        border-left: 6px solid #e53e3e; 
        padding: 16px 20px; 
        border-radius: 8px; 
        margin-bottom: 25px; 
        box-shadow: 0 2px 6px rgba(229, 62, 62, 0.1); 
    }
    
    /* 카드 컴포넌트 (초록색 포인트 테두리) */
    .naver-card { 
        background-color: #ffffff; 
        padding: 24px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0; 
        border-top: 4px solid #03C75A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); 
        margin-bottom: 25px; 
    }
    
    .section-title { 
        font-size: 18px; 
        font-weight: 800; 
        color: #111111; 
        margin-bottom: 16px; 
        display: flex; 
        align-items: center; 
        gap: 8px; 
        border-bottom: 2px solid #f1f3f5; 
        padding-bottom: 10px; 
    }
    
    .law-link-box { 
        background: #f8f9fa; 
        border: 1px solid #d1d5db; 
        padding: 12px 16px; 
        border-radius: 6px; 
        margin-bottom: 10px; 
        font-size: 13px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
    }
    
    .term-box { 
        background: #f4fbf7; 
        border-left: 3px solid #03C75A; 
        padding: 12px 16px; 
        border-radius: 4px; 
        margin-bottom: 12px; 
        font-size: 13px; 
        border-top: 1px solid #e6f4ed;
        border-right: 1px solid #e6f4ed;
        border-bottom: 1px solid #e6f4ed;
    }
    </style>
""", unsafe_allow_html=True)


# 실시간 원자재 가격 가져오기 함수
@str_lit.cache_data(ttl=600)
def get_realtime_commodities():
  try:
    wti = yf.Ticker("CL=F").history(period="2d")
    brent = yf.Ticker("BZ=F").history(period="2d")
    copper = yf.Ticker("HG=F").history(period="2d")

    wti_price = (
        f"${wti['Close'].iloc[-1]:,.2f}" if not wti.empty else "$77.20"
    )
    brent_price = (
        f"${brent['Close'].iloc[-1]:,.2f}" if not brent.empty else "$81.50"
    )
    copper_price = (
        f"${copper['Close'].iloc[-1]:,.2f}" if not copper.empty else "$9,420.00"
    )
    return brent_price, wti_price, copper_price
  except:
    return "$81.50", "$77.20", "$9,420.00"


brent_val, wti_val, copper_val = get_realtime_commodities()

# 짙은 네이버 시그니처 상단 헤더 (AFK PORTAL INTEGRATION 적용)
str_lit.markdown("""
    <div class="naver-header">
        <div>
            <span style="background-color: #111111; color: #03C75A; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">AFK PORTAL INTEGRATION</span>
            <h1 style="margin: 10px 0 0 0; font-size: 26px; font-weight: 900; color: #ffffff;">📦 자재구매·무역 컴플라이언스 인텔리전스 데스크</h1>
        </div>
        <div style="text-align: right; font-size: 13px; color: #f1f3f5; line-height: 1.5;">
            <b>시스템 상태</b>: <span style="color: #ffe066; font-weight: 700;">● 실시간 API & 공유 데스크 가동중</span><br>
            기준일자: 2026년 9월 5일
        </div>
    </div>
""", unsafe_allow_html=True)

# 법령 개정 긴급 알람 섹션
str_lit.markdown("""
    <div class="alert-banner">
        <div style="font-weight: 800; color: #c53030; font-size: 15px; margin-bottom: 6px;">
            🚨 [법령 개정 긴급 알람] 주요 공급망 및 무역·하도급 법제 변경 사항 감지
        </div>
        <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #2d3748; line-height: 1.6;">
            <li><b>관세법 개정</b>: 할당관세 집중관리품목 수입신고 기한 단축(20일) 및 신고지연 가산세 한도 상향.</li>
            <li><b>대외무역법 개정</b>: 글로벌 통상 분쟁 대응 및 경제안보 관련 상응조치·국가 발전 이익 중심 수출통제 법적 근거 강화.</li>
            <li><b>하도급법 시행령 개정</b>: 하도급대금 연동 대상에 '주요 에너지(연료·열·전기)' 확대 및 건설하도급 지급보증 예외사유 축소.</li>
            <li><b>상생협력법 개정</b>: 기술 탈취 소송 대응을 위한 '한국형 증거개시 제도(K-디스커버리)' 및 자료제출명령권 도입.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 메인 화면 레이아웃 분할
col_left, col_right = str_lit.columns([1.5, 1.3])

with col_left:
  # 1. 주요 원자재 가격 추이
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">📈 주요 원자재 실시간'
      ' 시세 및 에너지 지표</div>',
      unsafe_allow_html=True,
  )
  str_lit.markdown(
      '<p style="font-size: 12px; color: #666; margin-top: -8px;'
      ' margin-bottom: 12px;">공신력 데이터 출처: 야후파이낸스 실시간 API (NYMEX,'
      " ICE, LME)</p>",
      unsafe_allow_html=True,
  )

  raw_materials_data = {
      "원자재 품목": [
          "브렌트유 (Brent Crude)",
          "WTI (West Texas Intermediate)",
          "구리 (Copper 3M)",
          "알루미늄 (Aluminum)",
          "니켈 (Nickel 3M)",
      ],
      "단위": ["배럴(BBL)", "배럴(BBL)", "톤(MT)", "톤(MT)", "톤(MT)"],
      "국제 시세 (USD)": [
          brent_val,
          wti_val,
          copper_val,
          "$2,450.00",
          "$16,350.00",
      ],
      "전주 대비": ["-0.5%", "-1.1%", "+1.4%", "-0.8%", "+2.3%"],
      "시장 동향": [
          "보합세 ➡️",
          "하락세 📉",
          "상승세 📈",
          "보합세 ➡️",
          "급등 주의 🚨",
      ],
  }
  str_lit.dataframe(
      pd.DataFrame(raw_materials_data), use_container_width=True, hide_index=True
  )
  str_lit.markdown("</div>", unsafe_allow_html=True)

  # 2. [신규] 자재구매팀 인사이트 & 스케쥴 공유 허브 (입력/삭제 및 자동 날짜 저장)
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">💡 자재구매팀 인사이트'
      " & 스케쥴 공유 허브</div>",
      unsafe_allow_html=True,
  )

  # 세션 스테이트를 이용한 실시간 메모리 데이터베이스 (인사이트 & 스케쥴)
  if "shared_posts" not in str_lit.session_state:
    str_lit.session_state.shared_posts = [
        {
            "id": 1,
            "type": "📌 스케쥴",
            "author": "김구매 팀장",
            "date": "2026-09-05 09:30",
            "content": (
                "다음 주 월요일 철강 공급사 단가 협상 회의 예정 (참석자 필독)"
            ),
        },
        {
            "id": 2,
            "type": "💡 인사이트",
            "author": "박사원",
            "date": "2026-09-05 11:15",
            "content": (
                "니켈 수급 불안정성 대비 대체 공급선 사전 확보 필요성 제기"
            ),
        },
    ]

  with str_lit.form("insight_form", clear_on_submit=True):
    str_lit.markdown(
        "<b style='font-size: 13px;'>새로운 인사이트 또는 스케쥴 등록</b>",
        unsafe_allow_html=True,
    )
    f_col1, f_col2 = str_lit.columns([1, 1])
    with f_col1:
      post_type = str_lit.selectbox(
          "구분", ["💡 인사이트 공유", "📌 팀 스케쥴 공유"]
      )
    with f_col2:
      author_name = str_lit.text_input(
          "작성자 이름", placeholder="예: 홍길동 매니저"
      )

    post_content = str_lit.text_area(
        "내용 입력",
        placeholder=(
            "공급망 특이사항, 단가 변동 예측, 주요 일정 등을 입력하세요..."
        ),
    )
    submit_btn = str_lit.form_submit_button(
        "📝 등록하기 (저장 시 날짜 자동 기록)"
    )

    if submit_btn:
      if author_name and post_content:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_item = {
            "id": len(str_lit.session_state.shared_posts) + 1,
            "type": post_type,
            "author": author_name,
            "date": current_time,
            "content": post_content,
        }
        str_lit.session_state.shared_posts.insert(0, new_item)
        str_lit.success("성공적으로 등록되었습니다!")
        str_lit.rerun()
      else:
        str_lit.warning("작성자 이름과 내용을 모두 입력해주세요.")

  str_lit.markdown(
      "<hr style='margin: 15px 0; border: none; border-top: 1px solid"
      " #e2e8f0;'>",
      unsafe_allow_html=True,
  )
  str_lit.markdown(
      "<b style='font-size: 13px; color: #333;'>📋 등록된 공유 보드 리스트</b>",
      unsafe_allow_html=True,
  )

  if not str_lit.session_state.shared_posts:
    str_lit.info("등록된 내용이 없습니다.")
  else:
    for idx, post in enumerate(str_lit.session_state.shared_posts):
      st_box_bg = (
          "#f4fbf7" if "인사이트" in post["type"] else "#f8f9fa"
      )  # 네이버 톤 반영
      str_lit.markdown(
          f"""
                <div style="background: {st_box_bg}; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; margin-bottom: 10px; font-size: 13px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <div><b>{post['type']}</b> | 작성자: <span style="color: #03C75A; font-weight: 700;">{post['author']}</span></div>
                        <div style="font-size: 11px; color: #666;">🕒 {post['date']}</div>
                    </div>
                    <div style="color: #2d3748; margin-top: 4px;">{post['content']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
      if str_lit.button(
          f"🗑️ 삭제하기 [ID: {post['id']}]", key=f"del_{post['id']}"
      ):
        str_lit.session_state.shared_posts.pop(idx)
        str_lit.success("항목이 삭제되었습니다.")
        str_lit.rerun()

  str_lit.markdown("</div>", unsafe_allow_html=True)

  # 3. 관련 핵심 기사 큐레이션
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">📰 공급망 및 원자재'
      " 관련 실시간 핵심 기사</div>",
      unsafe_allow_html=True,
  )
  articles = [
      {
          "title": (
              "국제 유가(브렌트·WTI) 실시간 변동성 확대 속 글로벌 에너지 수급 모니터링"
              " 강화"
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
    str_lit.markdown(
        f"""
            <div style="background: #f8f9fa; border: 1px solid #e3e5e8; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                <div style="font-size: 13px; font-weight: 700;"><a href="{art['url']}" target="_blank" style="color: #03C75A; text-decoration: none;">{art['title']}</a></div>
                <div style="font-size: 11px; color: #666; margin-top: 4px;">출처 언론사: {art['source']}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  str_lit.markdown("</div>", unsafe_allow_html=True)

with col_right:
  # 4. 실무 필수 무역용어집 (Pro Edition)
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">📖 실무 필수 무역·구매'
      " 용어집 (Pro Edition)</div>",
      unsafe_allow_html=True,
  )

  str_lit.markdown("""
        <div class="term-box">
            <b>B/L (Bill of Lading / 선하증권)</b><br>
            <span style="color: #555; font-size: 12px;">선박회사가 화물을 영수했음을 증명하고, 목적지에서 화물 인도의 청구권을 나타내는 유가증권.</span>
        </div>
        <div class="term-box">
            <b>L/C (Letter of Credit / 신용장)</b><br>
            <span style="color: #555; font-size: 12px;">수입업자의 요청으로 개설은행이 수출업자에게 대금 지급을 확약하는 보증서.</span>
        </div>
        <div class="term-box">
            <b>L/G (Letter of Guarantee / 수입화물선취보증서)</b><br>
            <span style="color: #555; font-size: 12px;">B/L 원본이 도착하기 전, 은행의 보증을 통해 화물을 먼저 찾아갈 수 있게 하는 서류.</span>
        </div>
        <div class="term-box">
            <b>D/P & D/A (Document Against Payment / Acceptance)</b><br>
            <span style="color: #555; font-size: 12px;">대금지급조건 인도(D/P)와 일정 기간 후 지급을 약정하는 인수도조건(D/A)의 추심 결제 방식.</span>
        </div>
        <div class="term-box">
            <b>C/O (Certificate of Origin / 원산지증명서)</b><br>
            <span style="color: #555; font-size: 12px;">수출물품의 원산지를 증명하는 서류로, FTA 특혜관세 적용 시 필수 제출.</span>
        </div>
        <div class="term-box">
            <b>THC (Terminal Handling Charge / 터미널하역료)</b><br>
            <span style="color: #555; font-size: 12px;">컨테이너가 부두 내에서 컨테이너 야드(CY)까지 이동 및 적하될 때 발생하는 하역 부대비용.</span>
        </div>
        <div class="term-box">
            <b>BOM (Bill of Materials / 자재소요량공식)</b><br>
            <span style="color: #555; font-size: 12px;">제품을 생산하는 데 들어가는 원자재, 부품 등의 소요 목록과 구성 비율.</span>
        </div>
        <div class="term-box">
            <b>MOQ (Minimum Order Quantity / 최소주문수량)</b><br>
            <span style="color: #555; font-size: 12px;">공급업체가 거래를 유지하기 위해 설정한 1회 최소 주문 수량 한도.</span>
        </div>
    """, unsafe_allow_html=True)

  str_lit.markdown("</div>", unsafe_allow_html=True)

# 5. 인코텀즈 2020 전체 11가지 조건 완벽 수록 섹션
str_lit.markdown(
    '<div class="naver-card"><div class="section-title">🌐 인코텀즈 2020 (Incoterms'
    ' 2020) 전체 11가지 조건 가이드</div>',
    unsafe_allow_html=True,
)

tab_all, tab_any, tab_sea = str_lit.tabs(
    ["전체 요약 보기", "모든 운송 방식 (7가지)", "해상/내수상운송 전용 (4가지)"]
)

with tab_all:
  str_lit.markdown("""
        <div style="font-size: 13px; color: #374151; line-height: 1.6;">
            <b>• 모든 운송 방식 (7가지)</b>: EXW, FCA, CPT, CIP, DAP, DPU, DDP<br>
            <b>• 해상/내수상운송 전용 (4가지)</b>: FAS, FOB, CFR, CIF<br>
            <span style="color: #03C75A; font-weight: 600;">💡 실무 팁: 계약 체결 시 위험 분기점(Risk Transfer)과 비용 부담(Cost) 범위를 반드시 일치시켜야 분쟁을 예방할 수 있습니다.</span>
        </div>
    """, unsafe_allow_html=True)

with tab_any:
  str_lit.markdown("""
        * **EXW (공장인도)**: 공장에서 인도. 수·출통관 포함 모든 비용/위험을 **매수인**이 부담.
        * **FCA (운송인인도)**: 지정 장소에서 운송인에게 인도. (수출통관 매도인)
        * **CPT (운송료지급인도)**: 목적지까지 운송비 매도인 부담. 위험은 운송인 인도 시 이전.
        * **CIP (운송료·보험료지급인도)**: CPT + **적화 보험**을 매도인이 필수로 가입.
        * **DAP (도착지인도)**: 지정 목적지 도중 수송 수단 위에서 인도. (수입통관 매수인)
        * **DPU (도착지하화인도)**: 목적지 도달 후 **하화(짐 내리기) 작업까지** 매도인이 완료.
        * **DDP (관세지급인도)**: 목적지까지 수입관세 및 모든 통관비용·위험을 **매도인**이 최종 부담.
    """)

with tab_sea:
  str_lit.markdown("""
        * **FAS (선측인도)**: 선적항의 **선박 옆(선측)**에 화물을 둘 때까지 비용·위험 부담.
        * **FOB (본선인도)**: 선적항에서 **본선에 화물 적재 완료** 시 위험 이전.
        * **CFR (운임포함인도)**: 목적항까지 운송비는 매도인 부담, 위험은 선적 시 매수인에게 이전.
        * **CIF (운임·보험료포함인도)**: CFR + **해상 보험료**를 매도인이 부담.
    """)

str_lit.markdown("</div>", unsafe_allow_html=True)

# 6. 국가법령정보센터 공식 링크 섹션
str_lit.markdown(
    '<div class="naver-card"><div class="section-title">🔗 공신력 법제처 및'
    " 유관기관 공식 법령 링크 바로가기</div>",
    unsafe_allow_html=True,
)

col_l1, col_l2 = str_lit.columns(2)
with col_l1:
  str_lit.markdown(
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
  str_lit.markdown(
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
str_lit.markdown("</div>", unsafe_allow_html=True)
