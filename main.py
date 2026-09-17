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

    # 관객수 데이터 숫자형 변환 및 결측치 처리
    df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce").fillna(
        0
    )

    # 트리맵 에러 방지: 장르와 영화명 기준 중복 제거/합산
    df_tree = (
        df.groupby(["genre", "movieNm"], as_index=False)["total_audi"]
        .sum()
        .query("total_audi > 0")
    )

    return df, df_tree


df, df_tree = load_data()

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

# 툴팁(마우스 오버) 설정
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

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

# 트리맵 생성 (정제된 df_tree 사용)
fig2 = px.treemap(
    df_tree,
    path=["genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 트리맵",
)

# 마우스 오버 툴팁 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명",
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르 전체의 시장 규모뿐만 아니라, 특정 장르 내에서 어떤 영화가 관객수를 독점하거나 크게 견인했는지 흥행 기여도를 직관적으로 알 수 있습니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 세 번째 그래프: 총 관객수(total_audi) 히스토그램
# ==============================================================================
st.subheader("3. 총 관객수 분포 히스토그램")

# 히스토그램 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객수 분포",
    labels={"total_audi": "총 관객수(명)", "count": "영화 수"},
)

fig3.update_traces(
    hovertemplate="<b>관객수 구간:</b> %{x}명<br><b>영화 수:</b> %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

# 데이터 분석값 계산 (최다 관객 영화, 관객 몰린 구간)
max_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = max_movie["movieNm"]
top_movie_audi = int(max_movie["total_audi"])

# 가장 밀집된 구간(하위 50% / 중앙값 기반) 계산
median_audi = df["total_audi"].median()

st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 총 관객수 **{int(median_audi):,}명 이하**의 상대적으로 낮은 흥행 구간에 밀집되어 있는 반면, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'** (총 {top_movie_audi:,}명)으로 극소수의 흥행 대작이 전체 관객수를 크게 견인하는 오른쪽 꼬리가 긴 분포를 보입니다."
)
