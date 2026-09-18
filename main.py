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

    # 수치형 데이터 변환 및 결측치 처리
    numeric_cols = [
        "total_audi",
        "first_scrn",
        "first_week_audi",
        "days_in_top10",
        "first_show",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 개봉월(Month) 추출 전처리
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), errors="coerce")
    df["open_month"] = (
        df["openDt"].dt.month.fillna(0).astype(int).astype(str) + "월"
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
# 1. 장르별 영화 편수 (도넛 차트)
# ==============================================================================
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 비율",
)
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 2. 장르 및 영화별 총 관객수 (트리맵)
# ==============================================================================
st.subheader("2. 장르별 영화 계층 및 총 관객수")

fig2 = px.treemap(
    df_tree,
    path=["genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 트리맵",
)
fig2.update_traces(hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명")

st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. 총 관객수(total_audi) 히스토그램
# ==============================================================================
st.subheader("3. 총 관객수 분포 히스토그램")

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
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 4. 개봉일 스크린수 vs 총 관객수 (산점도)
# ==============================================================================
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 대 총 관객수 산점도",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "genre": "장르",
    },
)
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 5. 영화 10편 이상 장르의 총 관객수 상자 그림 (박스플롯)
# ==============================================================================
st.subheader("5. 주요 장르별 총 관객수 분포 (박스플롯)")

top_genres = df["genre"].value_counts()[lambda x: x >= 10].index
df_top_genres = df[df["genre"].isin(top_genres)]

fig5 = px.box(
    df_top_genres,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="주요 장르별(10편 이상) 총 관객수 분포 및 이상치",
    labels={"genre": "장르", "total_audi": "총 관객수(명)"},
)
fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{x}<br>관객수: %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 6. 스크린수 vs 총 관객수 (버블 차트 - 크기: 첫 주 관객수)
# ==============================================================================
st.subheader("6. 스크린수, 총 관객수 및 첫 주 관객수 (버블 차트)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린수 대 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "first_week_audi": "첫 주 관객수(명)",
        "genre": "장르",
    },
)
fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명"
)

st.plotly_chart(fig6, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 7. 제작 국가별 장르 분포 (선버스트)
# ==============================================================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

df_sunburst = (
    df.groupby(["nation", "genre"]).size().reset_index(name="movie_count")
)

fig7 = px.sunburst(
    df_sunburst,
    path=["nation", "genre"],
    values="movie_count",
    color="nation",
    title="제작 국가 ➔ 장르 계층별 영화 편수 선버스트 차트",
)
fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}"
)

st.plotly_chart(fig7, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 8. 영화가 개봉한 월에 따라 평균 관객수 차이가 클까 (나만의 질문)
# ==============================================================================
st.subheader("8. 영화가 개봉한 월에 따라 평균 관객수 차이가 클까")

# 개봉월별 평균 총 관객수 집계 (0월 제외 및 1월~12월 순서 정렬)
df_valid_month = df[df["open_month"] != "0월"].copy()
month_order = [f"{i}월" for i in range(1, 13)]

df_month_audi = (
    df_valid_month.groupby("open_month", as_index=False)["total_audi"]
    .mean()
    .rename(columns={"total_audi": "avg_total_audi"})
)

fig8 = px.bar(
    df_month_audi,
    x="open_month",
    y="avg_total_audi",
    category_orders={"open_month": month_order},
    color="avg_total_audi",
    color_continuous_scale="Blues",
    title="영화가 개봉한 월에 따라 평균 관객수 차이가 클까",
    labels={"open_month": "개봉월", "avg_total_audi": "평균 총 관객수(명)"},
)

fig8.update_traces(
    hovertemplate="<b>%{x}</b><br>평균 총 관객수: %{y:,.0f}명"
)

st.plotly_chart(fig8, use_container_width=True)
st.markdown("---")
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("")
