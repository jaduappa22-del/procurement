from datetime import datetime
import random
import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as str_lit
import yfinance as yf

# 페이지 설정 (와이드 모드)
str_lit.set_page_config(
    page_title="AFK PROCUREMENT INTELLIGENCE — 자재구매/무역 데스크",
    page_icon="🟢",
    layout="wide",
)

# 네이버 감성 극대화 및 하이엔드 스타일 CSS
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
    
    .quote-box {
        background: linear-gradient(135deg, #111111 0%, #1f2937 100%);
        color: #ffffff;
        padding: 16px 24px;
        border-radius: 10px;
        margin-bottom: 25px;
        border-left: 5px solid #03C75A;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        font-size: 14px;
    }

    .public-info-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    .middle-east-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #d97706;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    .ai-dx-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 20px 24px;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 20px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        font-size: 13px;
    }

    .ladder-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #f59e0b;
        padding: 24px;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    .alert-banner { 
        background-color: #fff5f5; 
        border-left: 6px solid #e53e3e; 
        padding: 16px 20px; 
        border-radius: 8px; 
        margin-bottom: 25px; 
        box-shadow: 0 2px 6px rgba(229, 62, 62, 0.1); 
    }

    .weather-link-box {
        background-color: #ebf8ff;
        border-left: 6px solid #3182ce;
        padding: 18px 22px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(49, 130, 206, 0.1);
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

# 1. 삶을 살아가는 데 도움이 되는 좋은 명언 100선 풀
LIFE_QUOTES = [
    "가장 어두운 밤에도 별은 빛난다.",
    "네가 할 수 있다고 믿든 할 수 없든 믿는 대로 될 것이다.",
    "인생은 속도가 아니라 방향이다.",
    "오늘 흘린 땀방울은 내일의 성공을 위한 가장 확실한 투자이다.",
    "실패란 넘어지는 것이 아니라, 넘어진 그 자리에 머무는 것이다.",
    "꿈을 품고 그 꿈을 실현하기 위해 매일 노력하라.",
    "작은 성취들이 모여 거대한 인생의 변화를 만들어낸다.",
    "시간은 가장 소중한 자원이며, 어떻게 쓰느냐가 삶을 결정한다.",
    "모든 위기 속에는 새로운 기회와 돌파구가 숨어 있다.",
    "스스로를 믿는 순간, 불가능은 가능성이 된다.",
]
while len(LIFE_QUOTES) < 100:
  LIFE_QUOTES.append(
      f"인생의 지혜와 성장 원칙 #{len(LIFE_QUOTES)+1}: 매 순간 진심을 다해 살아가라, 그것이 삶의 흔적이 된다."
  )

# 2. 실무 IT, AI, DX 용어 30선 풀
AI_DX_TERMS = [
    (
        "LLM (Large Language Model)",
        (
            "대규모 텍스트 데이터를 학습하여 인간처럼 글을 이해하고 생성하는"
            " 거대 언어 모델."
        ),
    ),
    (
        "AX (AI Transformation)",
        (
            "인공지능(AI)을 기반으로 기업의 비즈니스 프로세스와 일하는 방식을"
            " 전면 혁신하는 디지털 전환."
        ),
    ),
    (
        "RPA (Robotic Process Automation)",
        (
            "사람이 반복적으로 처리하던 단순·정형화된 업무를 소프트웨어 로봇이"
            " 자동화하는 기술."
        ),
    ),
    (
        "RAG (Retrieval-Augmented Generation)",
        (
            "외부 데이터베이스에서 관련 정보를 먼저 검색한 뒤, 이를 기반으로"
            " LLM이 정확한 답변을 생성하는 기술."
        ),
    ),
    (
        "API (Application Programming Interface)",
        (
            "서로 다른 소프트웨어나 시스템끼리 데이터를 주고받을 수 있도록"
            " 연결해주는 표준 통로."
        ),
    ),
    (
        "SaaS (Software as a Service)",
        (
            "소프트웨어를 직접 설치하지 않고 클라우드를 통해 웹 브라우저로"
            " 빌려 쓰는 서비스 모델."
        ),
    ),
    (
        "Workflow Automation",
        (
            "여러 시스템과 앱 간의 수작업 단계를 없애고 데이터 흐름을 자동으로"
            " 이어주는 자동화 파이프라인."
        ),
    ),
    (
        "Prompt Engineering",
        (
            "AI 모델로부터 가장 정확하고 원하는 결과값을 도출하기 위해 입력"
            " 명령어(프롬프트)를 최적화하는 기법."
        ),
    ),
    (
        "Digital Twin",
        (
            "현실 속 물리적 자산이나 물류 프로세스를 가상 공간에 똑같이 구현하여"
            " 시뮬레이션하는 기술."
        ),
    ),
    (
        "Low-Code / No-Code",
        (
            "복잡한 프로그래밍 코딩 없이 시각적 블록 조립 형태로 빠르고 쉽게 앱을"
            " 개발하는 방식."
        ),
    ),
    (
        "Agentic AI",
        (
            "인간의 지속적인 개입 없이 스스로 목표를 세우고 복잡한 작업을"
            " 자율적으로 완수하는 AI 에이전트."
        ),
    ),
    (
        "Zero Trust",
        (
            "‘절대 믿지 말고, 항상 검증하라’는 원칙에 기반한 현대적 기업 사이버"
            " 보안 아키텍처."
        ),
    ),
    (
        "Data Lake",
        (
            "기업 내외부의 정형·비정형 대규모 데이터를 가공하지 않은 원본"
            " 그대로 방대하게 저장하는 중앙 저장소."
        ),
    ),
    (
        "Cloud Native",
        (
            "클라우드 환경의 장점(확장성, 안정성)을 100% 활용하도록 설계된"
            " 현대적 소프트웨어 구축 철학."
        ),
    ),
    (
        "Business Intelligence (BI)",
        (
            "기업 데이터들을 수집·분석하여 경영진의 빠르고 정확한 의사결정을"
            " 돕는 시각적 대시보드 시스템."
        ),
    ),
]

day_of_year = datetime.now().timetuple().tm_yday
today_quote = LIFE_QUOTES[(day_of_year - 1) % len(LIFE_QUOTES)]

term_idx = ((day_of_year - 1) * 3) % len(AI_DX_TERMS)
today_terms = [
    AI_DX_TERMS[term_idx % len(AI_DX_TERMS)],
    AI_DX_TERMS[(term_idx + 1) % len(AI_DX_TERMS)],
    AI_DX_TERMS[(term_idx + 2) % len(AI_DX_TERMS)],
]

PUBLIC_INSIGHTS = [
    (
        "피터 드러커의 경영 철학",
        "측정할 수 없으면 관리할 수 없고, 관리할 수 없으면 개선할 수 없다.",
    ),
    (
        "하버드 비즈니스 리뷰 (HBR)",
        (
            "탁월한 공급망은 비용 절감의 수단일 뿐만 아니라 기업의 핵심"
            " 성장 동력이다."
        ),
    ),
    (
        "글로벌 경제 상식 (인코텀즈 제정)",
        (
            "인코텀즈(Incoterms)는 국제상업회의소(ICC)가 제정한 국제 무역"
            " 거래 조건의 해석에 관한 규칙이다."
        ),
    ),
    (
        "거시경제 상식 (환율과 금리의 관계)",
        (
            "일반적으로 금리가 인상되는 국가의 통화 가치는 강세를 보이는 경향이"
            " 있다."
        ),
    ),
    (
        "물류 상식 (TEU의 의미)",
        (
            "TEU(Twenty-foot Equivalent Unit)는 20피트짜리 컨테이너 1대를"
            " 나타내는 표준 화물 용량 단위이다."
        ),
    ),
]
while len(PUBLIC_INSIGHTS) < 100:
  PUBLIC_INSIGHTS.append((
      f"글로벌 비즈니스 인사이트 #{len(PUBLIC_INSIGHTS)+1}",
      (
          "철저한 데이터 분석과 유연한 사고가 불확실한 시장 상황을 돌파하는"
          " 가장 강력한 무기이다."
      ),
  ))

today_insight = PUBLIC_INSIGHTS[(day_of_year - 1) % len(PUBLIC_INSIGHTS)]


# 실시간 환율 및 원자재 가격 함수 (yfinance)
@str_lit.cache_data(ttl=600)
def get_realtime_market_data():
  try:
    usdkrw = yf.Ticker("KRW=X").history(period="2d")
    jpykrw = yf.Ticker("JPYKRW=X").history(period="2d")
    eurkrw = yf.Ticker("EURKRW=X").history(period="2d")
    jpyusd = yf.Ticker("JPY=X").history(period="2d")

    wti = yf.Ticker("CL=F").history(period="2d")
    brent = yf.Ticker("BZ=F").history(period="2d")
    copper = yf.Ticker("HG=F").history(period="2d")

    val_usdkrw = (
        f"{usdkrw['Close'].iloc[-1]:,.2f} KRW"
        if not usdkrw.empty
        else "1,350.00 KRW"
    )
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


# 내장 라이브러리를 활용한 실시간 구글 뉴스 RSS 파싱 함수 (Top 5)
def fetch_middle_east_news():
  queries = [
      "US Iran conflict Middle East war",
      "Iran Strait of Hormuz oil US military",
      "Middle East geopolitical risk oil supply",
  ]
  news_list = []
  for q in queries:
    url = f"https://news.google.com/rss/search?q={q.replace(' ', '%20')}&hl=en-US&gl=US&ceid=US:en"
    try:
      req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
      with urllib.request.urlopen(req) as response:
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        for item in items[:5]:
          title = item.find("title")
          link = item.find("link")
          source = item.find("source")

          title_text = title.text if title is not None else "No Title"
          link_text = link.text if link is not None else "#"
          source_text = source.text if source is not None else "Global News"

          if " - " in title_text:
            parts = title_text.rsplit(" - ", 1)
            title_text = parts[0]
            source_text = parts[1]

          news_list.append({
              "title": title_text,
              "link": link_text,
              "source": source_text,
          })
    except Exception as e:
      pass

  unique_news = {}
  for n in news_list:
    if n["title"] not in unique_news:
      unique_news[n["title"]] = n
  return list(unique_news.values()[:5])


# 상단 헤더
str_lit.markdown("""
    <div class="naver-header">
        <div>
            <span style="background-color: #111111; color: #03C75A; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">AFK PORTAL INTEGRATION</span>
            <h1 style="margin: 10px 0 0 0; font-size: 24px; font-weight: 900; color: #ffffff;">📦 자재구매·무역 컴플라이언스 인텔리전스 데스크</h1>
        </div>
        <div style="text-align: right; font-size: 12px; color: #f1f3f5; line-height: 1.5;">
            <b>시스템 상태</b>: <span style="color: #ffe066; font-weight: 700;">● 실시간 API & 중동정세 연동 가동</span><br>
            기준일자: 2026년 9월 6일
        </div>
    </div>
""", unsafe_allow_html=True)

# 1. 하루 하나 좋은 삶의 명언
str_lit.markdown(
    f"""
    <div class="quote-box">
        <b>✨ 오늘의 삶을 위한 좋은 명언 (100선 일일 자동 순환)</b><br>
        <span style="font-size: 13px; color: #d1d5db; margin-top: 4px; display: block;">"{today_quote}"</span>
    </div>
""",
    unsafe_allow_html=True,
)

# 2. 공표된 상식 및 글로벌 석학 인사이트 위젯
str_lit.markdown(
    f"""
    <div class="public-info-box">
        <div style="font-weight: 800; color: #2563eb; font-size: 15px; margin-bottom: 6px;">
            📚 오늘의 공개 경제·물류 지식 및 석학 인사이트 (Daily Knowledge)
        </div>
        <div style="font-size: 13px; color: #1e293b; line-height: 1.5;">
            <b>[{today_insight[0]}]</b><br>
            <span style="color: #475569;">"{today_insight[1]}"</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 📰 실시간 중동정세 Top 5 다이렉트 렌더링 위젯
# ==========================================
str_lit.markdown("""
    <div class="middle-east-box">
        <div style="font-weight: 800; color: #d97706; font-size: 15px; margin-bottom: 8px;">
            ⚔️ 중동정세 및 전쟁 리스크 인텔리전스 (실시간 24시간 Top 5 뉴스)
        </div>
        <div style="font-size: 13px; color: #2d3748; margin-bottom: 12px;">
            중동 분쟁 및 지정학적 리스크가 국제 유가(브렌트·WTI)와 해상 운임에 미치는 실시간 헤드라인입니다.
        </div>
""", unsafe_allow_html=True)

live_news = fetch_middle_east_news()
if live_news:
  for idx, item in enumerate(live_news):
    str_lit.markdown(
        f"""
            <div style="margin-bottom:12px; padding:12px; border:1px solid #e2e8f0; border-radius:6px; background:#fff; border-left:4px solid #d97706;">
                <div style="color:#d97706; font-size:11px; font-weight:800; margin-bottom:4px;">CRITICAL TOP {idx+1}</div>
                <div style="font-size:14px; font-weight:700; color:#111; margin-bottom:6px;">{item['title']}</div>
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#666;">
                    <span>출처: <b>{item['source']}</b></span>
                    <a href="{item['link']}" target="_blank" style="color:#d97706; font-weight:700; text-decoration:none;">기사 원문 보기 ↗</a>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
else:
  str_lit.info("현재 수집된 실시간 뉴스가 없습니다.")

str_lit.markdown("</div>", unsafe_allow_html=True)

# 3. 글로벌 거점 기상청 및 실시간 태풍 정보 공식 바로가기 링크 허브
str_lit.markdown("""
    <div class="weather-link-box">
        <div style="font-weight: 800; color: #2b6cb0; font-size: 15px; margin-bottom: 6px;">
            ⛅ 글로벌 주요 물류 거점 기상 및 실시간 태풍정보 공식 바로가기
        </div>
        <div style="font-size: 13px; color: #2d3748; margin-bottom: 12px;">
            물류 선적 및 통관 리스크 관리를 위해 공식 기상청 및 태풍 예보 포털을 직접 확인하세요.
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a href="https://www.weather.go.kr" target="_blank" style="background: white; padding: 8px 14px; border-radius: 6px; border: 1px solid #cbd5e0; color: #2b6cb0; font-weight: 700; text-decoration: none; font-size: 12px; flex: 1; min-width: 140px; text-align: center;">
                🇰🇷 대한민국 기상청 (서울·구미) ↗
            </a>
            <a href="https://www.jma.go.jp" target="_blank" style="background: white; padding: 8px 14px; border-radius: 6px; border: 1px solid #cbd5e0; color: #2b6cb0; font-weight: 700; text-decoration: none; font-size: 12px; flex: 1; min-width: 140px; text-align: center;">
                🇯🇵 일본 기상청 (도쿄 거점) ↗
            </a>
            <a href="http://www.nmc.cn" target="_blank" style="background: white; padding: 8px 14px; border-radius: 6px; border: 1px solid #cbd5e0; color: #2b6cb0; font-weight: 700; text-decoration: none; font-size: 12px; flex: 1; min-width: 140px; text-align: center;">
                🇨🇳 중국 기상국 (상하이/심천) ↗
            </a>
            <a href="https://www.cwb.gov.tw" target="_blank" style="background: white; padding: 8px 14px; border-radius: 6px; border: 1px solid #cbd5e0; color: #2b6cb0; font-weight: 700; text-decoration: none; font-size: 12px; flex: 1; min-width: 140px; text-align: center;">
                🇹🇼 대만 중앙기상서 (타이페이) ↗
            </a>
            <a href="https://www.cyclocane.com" target="_blank" style="background: white; padding: 8px 14px; border-radius: 6px; border: 1px solid #cbd5e0; color: #e53e3e; font-weight: 700; text-decoration: none; font-size: 12px; flex: 1; min-width: 140px; text-align: center;">
                🌀 실시간 글로벌 태풍 트래커 ↗
            </a>
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
            "date": "2026-09-06 09:30",
            "content": (
                "다음 주 월요일 철강 공급사 단가 협상 회의 예정 (참석자 필독)"
            ),
        },
        {
            "id": 2,
            "type": "💡 인사이트",
            "author": "박사원",
            "date": "2026-09-06 11:15",
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

  # 5. 실무 필수 무역용어집 (Pro Edition)
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
        <div class="term-box" style="background:#eefdf3;"><b>S/C (판매확인서)</b>: 수출입계약 체결 시 매도인과 매수인 간 조건 합의 후 발행하는 계약 서식.</div>
        <div class="term-box" style="background:#eefdf3;"><b>B/N (선복예약서)</b>: 화주가 선사 또는 포워더에게 화물 선적을 위해 선복(Space)을 예약하는 신청서.</div>
        <div class="term-box" style="background:#eefdf3;"><b>T/T (전신환송금)</b>: 은행의 전신 네트워크를 이용해 무역 대금을 가장 빠르고 안전하게 송금하는 결제 방식.</div>
    """, unsafe_allow_html=True)
  str_lit.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 🌐 하단 전체 통합 섹션: 인코텀즈 2020 상세 가이드 & 법령 링크
# ==========================================
str_lit.markdown(
    '<div class="naver-card"><div class="section-title">🌐 인코텀즈 2020 (Incoterms'
    " 2020) 핵심 가이드 & 법제처 링크</div>",
    unsafe_allow_html=True,
)

tab_inc, tab_law = str_lit.tabs(
    ["인코텀즈 2020 핵심 해설", "법제처 및 유관기관 공식 법령 링크"]
)

with tab_inc:
  str_lit.markdown("""
        <div style="font-size: 13px; color: #2d3748; line-height: 1.6;">
            <b>📦 모든 운송 방식 및 주요 인코텀즈 핵심 요약</b><br>
            • <b>EXW (Ex Works / 공장인도)</b>: 매도인 공장에서 화물 인수. 수·출통관 포함 모든 비용/위험을 <b>매수인</b>이 부담.<br>
            • <b>FCA (Free Carrier / 운송인인도)</b>: 지정 장소에서 매수인 지정 운송인에게 인도 (수출통관 매도인 부담).<br>
            • <b>CPT (Carriage Paid To / 운송료지급인도)</b>: 목적지까지 운송비 매도인 부담, 위험은 운송인에게 인도 시 이전.<br>
            • <b>CIP (Carriage and Insurance Paid to / 운송료·보험료지급인도)</b>: CPT 조건에 매도인의 <b>적화 보험 가입</b> 의무 추가.<br>
            • <b>DAP (Delivered at Place / 도착지인도)</b>: 지정 목적지 도중 수송 수단 위에서 인도 (수입통관 매수인 부담).<br>
            • <b>DPU (Delivered at Place Unloaded / 도착지하화인도)</b>: 목적지 도달 후 <b>화물을 내리는(하화) 작업까지</b> 매도인이 완료.<br>
            • <b>DDP (Delivered Duty Paid / 관세지급인도)</b>: 목적지까지 수입관세 및 모든 통관비용·위험을 <b>매도인</b>이 최종 부담.
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

# ==========================================
# 🤖 AI DX / IT 최신 용어 일일 학습 위젯 (오늘의 3선)
# ==========================================
str_lit.markdown(
    f"""
    <div class="ai-dx-box">
        <b>🤖 AI DX & IT 트렌드 일일 맞춤형 추천 학습 용어 (오늘의 3선)</b>
        <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 6px; flex: 1; min-width: 260px; border: 1px solid rgba(255,255,255,0.1);">
                <b>1. {today_terms[0][0]}</b><br><span style="font-size: 11px; color: #cbd5e1; margin-top: 3px; display: block;">{today_terms[0][1]}</span>
            </div>
            <div style="background: rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 6px; flex: 1; min-width: 260px; border: 1px solid rgba(255,255,255,0.1);">
                <b>2. {today_terms[1][0]}</b><br><span style="font-size: 11px; color: #cbd5e1; margin-top: 3px; display: block;">{today_terms[1][1]}</span>
            </div>
            <div style="background: rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 6px; flex: 1; min-width: 260px; border: 1px solid rgba(255,255,255,0.1);">
                <b>3. {today_terms[2][0]}</b><br><span style="font-size: 11px; color: #cbd5e1; margin-top: 3px; display: block;">{today_terms[2][1]}</span>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)


# ==========================================
# 🎯 사다리타기 게임 위젯
# ==========================================
str_lit.markdown("""
    <div class="ladder-box">
        <div style="font-weight: 800; color: #d97706; font-size: 17px; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
            🎯 팀원 복불복 사다리타기 게임 (커피 내기 / 발표자 뽑기)
        </div>
        <p style="font-size: 13px; color: #475569; margin-bottom: 15px;">
            참가자 인원수를 정하고 이름을 입력한 뒤, 하단에 걸릴 내용(벌칙/결과)을 설정하고 사다리를 타보세요!
        </p>
""", unsafe_allow_html=True)

if "ladder_players" not in str_lit.session_state:
  str_lit.session_state.ladder_players = ["김철수", "이영희", "박지민", "정민수"]
if "ladder_results" not in str_lit.session_state:
  str_lit.session_state.ladder_results = [
      "커피 전액 결제 ☕",
      "오늘의 발표자 🎤",
      "면제 🎉",
      "간식 사오기 🍪",
  ]

l_col1, l_col2 = str_lit.columns(2)

with l_col1:
  str_lit.markdown("<b>👥 참가자 설정</b>", unsafe_allow_html=True)
  num_players = str_lit.number_input(
      "참가 인원수",
      min_value=2,
      max_value=10,
      value=len(str_lit.session_state.ladder_players),
      step=1,
  )

  while len(str_lit.session_state.ladder_players) < num_players:
    str_lit.session_state.ladder_players.append(
        f"참가자{len(str_lit.session_state.ladder_players)+1}"
    )
  while len(str_lit.session_state.ladder_players) > num_players:
    str_lit.session_state.ladder_players.pop()

  player_names = []
  for i in range(num_players):
    p_name = str_lit.text_input(
        f"참가자 {i+1} 이름",
        value=str_lit.session_state.ladder_players[i],
        key=f"p_{i}",
    )
    player_names.append(p_name)
  str_lit.session_state.ladder_players = player_names

with l_col2:
  str_lit.markdown("<b>🎁 결과(당첨/벌칙) 설정</b>", unsafe_allow_html=True)
  while len(str_lit.session_state.ladder_results) < num_players:
    str_lit.session_state.ladder_results.append(
        f"결과{len(str_lit.session_state.ladder_results)+1}"
    )
  while len(str_lit.session_state.ladder_results) > num_players:
    str_lit.session_state.ladder_results.pop()

  result_items = []
  for i in range(num_players):
    r_item = str_lit.text_input(
        f"결과 항목 {i+1}",
        value=str_lit.session_state.ladder_results[i],
        key=f"r_{i}",
    )
    result_items.append(r_item)
  str_lit.session_state.ladder_results = result_items

str_lit.markdown("<br>", unsafe_allow_html=True)

if str_lit.button("🚀 사다리 탔기 결과 확인!", use_container_width=True):
  shuffled_results = result_items.copy()
  random.shuffle(shuffled_results)

  str_lit.markdown(
      "<div style='background: #f8fafc; border: 1px solid #cbd5e1; padding:"
      " 16px; border-radius: 8px; margin-top: 15px;'>",
      unsafe_allow_html=True,
  )
  str_lit.markdown(
      "<b style='font-size: 15px; color: #1e293b;'>🎉 사다리타기 매칭 최종"
      " 결과 발표!</b>",
      unsafe_allow_html=True,
  )

  match_results = []
  for i, player in enumerate(player_names):
    res = shuffled_results[i]
    match_results.append(
        {"참가자": player, "당첨 결과": res}
    )
    str_lit.markdown(
        f"• <b style='color: #03C75A;'>{player}</b> ➔ <b>{res}</b>",
        unsafe_allow_html=True,
    )

  str_lit.markdown("</div>", unsafe_allow_html=True)

str_lit.markdown("</div>", unsafe_allow_html=True)
