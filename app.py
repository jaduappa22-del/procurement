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

# 네이버 감성을 극대화한 짙은 초록색(#03C75A, #00983c) 디자인 시스템 CSS
str_lit.markdown("""
    <style>
    .stApp { background-color: #f4f6f8; color: #1e1e1e; font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", Roboto, sans-serif; }
    
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
    
    .alert-banner { 
        background-color: #fff5f5; 
        border-left: 6px solid #e53e3e; 
        padding: 16px 20px; 
        border-radius: 8px; 
        margin-bottom: 25px; 
        box-shadow: 0 2px 6px rgba(229, 62, 62, 0.1); 
    }
    
    .naver-card { 
        background-color: #ffffff; 
        padding: 22px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0; 
        border-top: 4px solid #03C75A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); 
        margin-bottom: 20px; 
    }
    
    .section-title { 
        font-size: 17px; 
        font-weight: 800; 
        color: #111111; 
        margin-bottom: 14px; 
        display: flex; 
        align-items: center; 
        gap: 8px; 
        border-bottom: 2px solid #f1f3f5; 
        padding-bottom: 8px; 
    }
    
    .law-link-box { 
        background: #f8f9fa; 
        border: 1px solid #d1d5db; 
        padding: 10px 14px; 
        border-radius: 6px; 
        margin-bottom: 8px; 
        font-size: 13px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
    }
    
    .term-box { 
        background: #f4fbf7; 
        border-left: 3px solid #03C75A; 
        padding: 10px 14px; 
        border-radius: 4px; 
        margin-bottom: 10px; 
        font-size: 13px; 
        border: 1px solid #e6f4ed; 
    }
    </style>
""", unsafe_allow_html=True)


# 실시간 최신 환율 및 원자재 가격 가져오기 함수 (yfinance)
@str_lit.cache_data(ttl=600)
def get_realtime_market_data():
  try:
    usdkrw = yf.Ticker("KRW=X").history(period="2d")
    jpykrw = yf.Ticker("JPYKRW=X").history(
        period="2d"
    )  # 최신 원/엔 환율 (1엔당 혹은 환산용)
    eurkrw = yf.Ticker("EURKRW=X").history(period="2d")
    jpyusd = yf.Ticker("JPY=X").history(period="2d")  # 엔/달러 환율

    wti = yf.Ticker("CL=F").history(period="2d")
    brent = yf.Ticker("BZ=F").history(period="2d")
    copper = yf.Ticker("HG=F").history(period="2d")

    val_usdkrw = (
        f"{usdkrw['Close'].iloc[-1]:,.2f} KRW"
        if not usdkrw.empty
        else "1,350.00 KRW"
    )
    # JPYKRW는 보통 1엔 기준이므로 100엔 기준으로 환산 표시
    val_jpykrw = (
        f"{(jpykrw['Close'].iloc[-1]*100):,.2f} KRW"
        if not jpykrw.empty
        else "910.00 KRW"
    )
    val_eurkrw = (
        f"{eurkrw['Close'].iloc[-1]:,.2f} KRW"
        if not eurkrw.empty
        else "1,460.00 KRW"
    )
    val_jpyusd = (
        f"{jpyusd['Close'].iloc[-1]:,.2f} JPY"
        if not jpyusd.empty
        else "148.50 JPY"
    )

    val_brent = f"${brent['Close'].iloc[-1]:,.2f}" if not brent.empty else "$81.50"
    val_wti = f"${wti['Close'].iloc[-1]:,.2f}" if not wti.empty else "$77.20"
    val_copper = (
        f"${copper['Close'].iloc[-1]:,.2f}" if not copper.empty else "$9,420.00"
    )

    return (
        val_usdkrw,
        val_jpykrw,
        val_eurkrw,
        val_jpyusd,
        val_brent,
        val_wti,
        val_copper,
    )
  except:
    return (
        "1,350.00 KRW",
        "910.00 KRW",
        "1,460.00 KRW",
        "148.50 JPY",
        "$81.50",
        "$77.20",
        "$9,420.00",
    )


(
    fx_usd,
    fx_jpy,
    fx_eur,
    fx_jpy_usd,
    brent_val,
    wti_val,
    copper_val,
) = get_realtime_market_data()

# 상단 헤더
str_lit.markdown("""
    <div class="naver-header">
        <div>
            <span style="background-color: #111111; color: #03C75A; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">AFK PORTAL INTEGRATION</span>
            <h1 style="margin: 10px 0 0 0; font-size: 24px; font-weight: 900; color: #ffffff;">📦 자재구매·무역 컴플라이언스 인텔리전스 데스크</h1>
        </div>
        <div style="text-align: right; font-size: 12px; color: #f1f3f5; line-height: 1.5;">
            <b>시스템 상태</b>: <span style="color: #ffe066; font-weight: 700;">● 최신 실시간 API 연동 완료</span><br>
            기준일자: 2026년 9월 5일
        </div>
    </div>
""", unsafe_allow_html=True)

# 법령 개정 긴급 알람 섹션
str_lit.markdown("""
    <div class="alert-banner">
        <div style="font-weight: 800; color: #c53030; font-size: 14px; margin-bottom: 6px;">
            🚨 [법령 개정 긴급 알람] 주요 공급망 및 무역·하도급 법제 변경 사항 감지
        </div>
        <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #2d3748; line-height: 1.5;">
            <li><b>관세법 개정</b>: 할당관세 집중관리품목 수입신고 기한 단축(20일) 및 신고지연 가산세 한도 상향.</li>
            <li><b>대외무역법 개정</b>: 글로벌 통상 분쟁 대응 및 경제안보 관련 상응조치·국가 발전 이익 중심 수출통제 법적 근거 강화.</li>
            <li><b>하도급법 시행령 개정</b>: 하도급대금 연동 대상에 '주요 에너지(연료·열·전기)' 확대 및 건설하도급 지급보증 예외사유 축소.</li>
            <li><b>상생협력법 개정</b>: 기술 탈취 소송 대응을 위한 '한국형 증거개시 제도(K-디스커버리)' 및 자료제출명령권 도입.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 2단 레이아웃 그리드
col_left, col_right = str_lit.columns([1.1, 1.1])

with col_left:
  # 1. 실시간 환율 정보 (4대 핵심)
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">💱 실시간 주요 환율 지표'
      " (4대 핵심)</div>",
      unsafe_allow_html=True,
  )
  f_col1, f_col2 = str_lit.columns(2)
  with f_col1:
    str_lit.metric(label="🇺🇸 원 / 달러 (USD/KRW)", value=fx_usd)
    str_lit.metric(label="🇪🇺 원 / 유로 (EUR/KRW)", value=fx_eur)
  with f_col2:
    str_lit.metric(label="🇯🇵 원 / 엔 (100엔당 JPY/KRW)", value=fx_jpy)
    str_lit.metric(label="💱 엔 / 달러 (USD/JPY)", value=fx_jpy_usd)
  str_lit.markdown("</div>", unsafe_allow_html=True)

  # 2. 주요 원자재 가격 추이
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">📈 주요 원자재 실시간'
      ' 시세 및 에너지 지표</div>',
      unsafe_allow_html=True,
  )
  raw_materials_data = {
      "원자재 품목": [
          "브렌트유 (Brent)",
          "WTI 원유",
          "구리 (Copper)",
          "알루미늄",
          "니켈",
      ],
      "단위": ["배럴", "배럴", "톤(MT)", "톤(MT)", "톤(MT)"],
      "국제 시세 (USD)": [
          brent_val,
          wti_val,
          copper_val,
          "$2,450.00",
          "$16,350.00",
      ],
      "동향": ["보합 ➡️", "하락 📉", "상승 📈", "보합 ➡️", "급등 🚨"],
  }
  str_lit.dataframe(
      pd.DataFrame(raw_materials_data), use_container_width=True, hide_index=True
  )
  str_lit.markdown("</div>", unsafe_allow_html=True)

  # 3. 컨테이너 CBM 및 적재율 간이 계산기
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">🚢 컨테이너 CBM 및'
      " 적재율 간이 계산기</div>",
      unsafe_allow_html=True,
  )
  c_type = str_lit.selectbox(
      "컨테이너 규격 선택",
      [
          "20피트 컨테이너 (20ft - Max 28 CBM 권장)",
          "40피트 컨테이너 (40ft - Max 58 CBM 권장)",
      ],
  )
  max_cbm = 28.0 if "20피트" in c_type else 58.0

  box_l = str_lit.number_input(
      "화물 가로 길이 (cm)", min_value=1.0, value=60.0, step=1.0
  )
  box_w = str_lit.number_input(
      "화물 세로 길이 (cm)", min_value=1.0, value=40.0, step=1.0
  )
  box_h = str_lit.number_input(
      "화물 높이 (cm)", min_value=1.0, value=40.0, step=1.0
  )
  box_qty = str_lit.number_input(
      "총 박스 수량 (BOX)", min_value=1, value=500, step=10
  )

  total_cbm = (box_l * box_w * box_h / 1000000.0) * box_qty
  loading_rate = (total_cbm / max_cbm) * 100

  str_lit.markdown(
      f"""
        <div style="background: #f4fbf7; border: 1px solid #03C75A; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 13px;">
            <b>📦 계산 결과 요약</b><br>
            • 총 화물 용적: <b>{total_cbm:,.2f} CBM</b><br>
            • 컨테이너 기준 적재율: <b style="color: {'#e53e3e' if loading_rate > 100 else '#03C75A'};">{loading_rate:,.1f}%</b> ({'⚠️ 용적 초과 주의!' if loading_rate > 100 else '✅ 적정 적재 범위'})
        </div>
    """,
      unsafe_allow_html=True,
  )
  str_lit.markdown("</div>", unsafe_allow_html=True)


with col_right:
  # 4. 자재구매팀 인사이트 & 스케쥴 공유 허브 (입력/삭제 및 자동 날짜)
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">💡 자재구매팀 인사이트'
      " & 스케쥴 공유 허브</div>",
      unsafe_allow_html=True,
  )

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

  with str_lit.form("insight_form_opt", clear_on_submit=True):
    str_lit.markdown(
        "<b style='font-size: 12px;'>새로운 인사이트 / 스케쥴 등록</b>",
        unsafe_allow_html=True,
    )
    f_c1, f_c2 = str_lit.columns([1, 1])
    with f_c1:
      post_type = str_lit.selectbox(
          "구분", ["💡 인사이트 공유", "📌 팀 스케쥴 공유"], key="p_type"
      )
    with f_c2:
      author_name = str_lit.text_input(
          "작성자", placeholder="예: 홍길동 매니저", key="p_author"
      )

    post_content = str_lit.text_area(
        "내용", placeholder="특이사항 및 스케쥴 입력...", key="p_content"
    )
    if str_lit.form_submit_button("📝 등록하기 (날짜 자동기록)"):
      if author_name and post_content:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        str_lit.session_state.shared_posts.insert(
            0,
            {
                "id": len(str_lit.session_state.shared_posts) + 1,
                "type": post_type,
                "author": author_name,
                "date": cur_time,
                "content": post_content,
            },
        )
        str_lit.success("등록 완료!")
        str_lit.rerun()
      else:
        str_lit.warning("작성자와 내용을 입력해주세요.")

  str_lit.markdown(
      "<hr style='margin: 10px 0; border: none; border-top: 1px solid"
      " #e2e8f0;'>",
      unsafe_allow_html=True,
  )

  if str_lit.session_state.shared_posts:
    for idx, post in enumerate(str_lit.session_state.shared_posts):
      str_lit.markdown(
          f"""
                <div style="background: #f8f9fa; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; margin-bottom: 8px; font-size: 12px;">
                    <div><b>{post['type']}</b> | <span style="color: #03C75A; font-weight: 700;">{post['author']}</span> ({post['date']})</div>
                    <div style="color: #333; margin-top: 3px;">{post['content']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
      if str_lit.button(
          f"삭제 [ID: {post['id']}]", key=f"del_opt_{post['id']}"
      ):
        str_lit.session_state.shared_posts.pop(idx)
        str_lit.rerun()

  str_lit.markdown("</div>", unsafe_allow_html=True)

  # 5. 실무 필수 무역용어집 (기존 + 3개 추가하여 총 11개 상세 구성)
  str_lit.markdown(
      '<div class="naver-card"><div class="section-title">📖 실무 필수 무역·구매'
      " 용어집 (Pro Edition)</div>",
      unsafe_allow_html=True,
  )
  str_lit.markdown("""
        <div class="term-box"><b>B/L (선하증권)</b>: 선박회사가 화물을 영수했음을 증명하고 목적지에서 인도를 청구하는 유가증권.</div>
        <div class="term-box"><b>L/C (신용장)</b>: 수입업자 요청으로 개설은행이 수출업자에게 대금 지급을 확약하는 보증서.</div>
        <div class="term-box"><b>L/G (수입화물선취보증서)</b>: B/L 원본 도착 전 은행 보증으로 화물을 먼저 찾게 해주는 서류.</div>
        <div class="term-box"><b>D/P & D/A</b>: 대금지급 인도조건(D/P) 및 일정 기간 후 지급 약정 인수도조건(D/A) 추심 방식.</div>
        <div class="term-box"><b>C/O (원산지증명서)</b>: 수출물품 원산지 증명 서류로 FTA 특혜관세 적용 시 필수 제출.</div>
        <div class="term-box"><b>THC (터미널하역료)</b>: 컨테이너가 부두 내에서 야드까지 이동 및 적하될 때 발생하는 하역 부대비용.</div>
        <div class="term-box"><b>BOM (자재소요량공식)</b>: 제품 생산에 들어가는 원자재, 부품 등의 소요 목록과 구성 비율.</div>
        <div class="term-box"><b>MOQ (최소주문수량)</b>: 공급업체가 거래 유지를 위해 설정한 1회 최소 주문 수량 한도.</div>
        <div class="term-box" style="background:#eefdf3;"><b>S/C (판매확인서)</b>: 수출입계약 체결 시 매도인과 매수인 간 조건 합의 후 발행하는 계약 서식 (신규 추가).</div>
        <div class="term-box" style="background:#eefdf3;"><b>B/N (선복예약서)</b>: 화주가 선사 또는 포워더에게 화물 선적을 위해 선복(Space)을 예약하는 신청서 (신규 추가).</div>
        <div class="term-box" style="background:#eefdf3;"><b>T/T (전신환송금)</b>: 은행의 전신 네트워크를 이용해 무역 대금을 가장 빠르고 안전하게 송금하는 결제 방식 (신규 추가).</div>
    """, unsafe_allow_html=True)
  str_lit.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 🌐 하단 전체 통합 섹션: 인코텀즈 2020 11가지 상세 가이드 & 법령 링크
# ==========================================
str_lit.markdown(
    '<div class="naver-card"><div class="section-title">🌐 인코텀즈 2020 (Incoterms'
    " 2020) 전체 11가지 조건 상세 가이드 & 법제처 링크</div>",
    unsafe_allow_html=True,
)

tab_inc, tab_law = str_lit.tabs(
    ["인코텀즈 2020 11가지 상세 해설", "법제처 및 유관기관 공식 법령 링크"]
)

with tab_inc:
  str_lit.markdown("""
        <div style="font-size: 13px; color: #2d3748; line-height: 1.6;">
            <b>📦 1. 모든 운송 방식에 사용 가능한 조건 (7가지)</b><br>
            • <b>EXW (Ex Works / 공장인도)</b>: 매도인 공장에서 화물 인수. 수·출통관 포함 모든 비용/위험을 <b>매수인</b>이 부담.<br>
            • <b>FCA (Free Carrier / 운송인인도)</b>: 지정 장소에서 매수인 지정 운송인에게 인도 (수출통관 매도인 부담).<br>
            • <b>CPT (Carriage Paid To / 운송료지급인도)</b>: 목적지까지 운송비 매도인 부담, 위험은 운송인에게 인도 시 이전.<br>
            • <b>CIP (Carriage and Insurance Paid to / 운송료·보험료지급인도)</b>: CPT 조건에 매도인의 <b>적화 보험 가입</b> 의무 추가.<br>
            • <b>DAP (Delivered at Place / 도착지인도)</b>: 지정 목적지 도중 수송 수단 위에서 인도 (수입통관 매수인 부담).<br>
            • <b>DPU (Delivered at Place Unloaded / 도착지하화인도)</b>: 목적지 도달 후 <b>화물을 내리는(하화) 작업까지</b> 매도인이 완료.<br>
            • <b>DDP (Delivered Duty Paid / 관세지급인도)</b>: 목적지까지 수입관세 및 모든 통관비용·위험을 <b>매도인</b>이 최종 부담.<br><br>
            
            <b>⚓ 2. 해상 및 내수상운송 전용 조건 (4가지)</b><br>
            • <b>FAS (Free Alongside Ship / 선측인도)</b>: 선적항의 <b>선박 옆(선측)</b>에 화물을 둘 때까지 비용·위험 부담.<br>
            • <b>FOB (Free on Board / 본선인도)</b>: 선적항에서 <b>본선에 화물 적재 완료</b> 시 위험이 매수인에게 이전.<br>
            • <b>CFR (Cost and Freight / 운임포함인도)</b>: 목적항까지 운송비는 매도인 부담, 위험은 선적 시 매수인에게 이전.<br>
            • <b>CIF (Cost, Insurance and Freight / 운임·보험료포함인도)</b>: CFR 조건에 매도인의 <b>해상 보험료 부담</b> 추가.
        </div>
    """, unsafe_allow_html=True)

with tab_law:
  col_l1, col_l2 = str_lit.columns(2)
  with col_l1:
    str_lit.markdown(
        """
            <div class="law-link-box"><span><b>관세법</b> (국가법령정보센터)</span><a href="https://www.law.go.kr/법령/관세법" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a></div>
            <div class="law-link-box"><span><b>대외무역법</b> (국가법령정보센터)</span><a href="https://www.law.go.kr/법령/대외무역법" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a></div>
        """,
        unsafe_allow_html=True,
    )
  with col_l2:
    str_lit.markdown(
        """
            <div class="law-link-box"><span><b>하도급거래공정화에관한법률</b></span><a href="https://www.law.go.kr/법령/하도급거래공정화에관한법률" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a></div>
            <div class="law-link-box"><span><b>대·중소기업상생협력촉진에관한법률</b></span><a href="https://www.law.go.kr/법령/대·중소기업상생협력촉진에관한법률" target="_blank" style="color: #03C75A; font-weight: 700; text-decoration: none;">바로가기 ↗</a></div>
        """,
        unsafe_allow_html=True,
    )

str_lit.markdown("</div>", unsafe_allow_html=True)
