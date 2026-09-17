import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")


# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열 전처리: '|' 기호로 구분된 복수 장르 중 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


df = load_data()

# ==============================================================================
# 첫 번째 그래프: 장르별 영화 편수 (도넛 차트)
# ==============================================================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 빈도수 계산
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 비율",
)

# 툴팁(마우스 오버) 설정: 장르명, 편수, 비율 표시
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}",
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 구분선 및 해석 구역
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info(
    "박스오피스 상위권에 진입한 영화 중 특정 대표 장르(예: 드라마, 액션 등)가 차지하는 비중을 한눈에 비교할 수 있습니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 두 번째 그래프: 장르 및 영화별 총 관객수 (트리맵)
# ==============================================================================
st.subheader("2. 장르별 영화 계층 및 총 관객수")

# Plotly 트리맵 생성 (계층: genre -> movieNm, 사각형 크기: total_audi)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 트리맵",
)

# 마우스 오버 툴팁 설정 (영화명 및 총 관객수 표시)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명",
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 구분선 및 해석 구역
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르 전체의 시장 규모뿐만 아니라, 특정 장르 내에서 어떤 영화가 관객수를 독점하거나 크게 견인했는지 흥행 기여도를 직관적으로 알 수 있습니다."
)
