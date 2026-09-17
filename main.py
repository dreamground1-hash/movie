import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 데이터 불러오기 및 전처리 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre: 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if '|' in x else x)
    
    return df

df = load_data()

# 데이터 미리보기
with st.expander("📄 데이터셋 미리보기"):
    st.dataframe(df)

# Section 1: 장르별 영화 편수 (도넛 그래프)
st.header("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    values='count',
    names='genre',
    title='장르별 영화 비율 및 편수',
    hole=0.4,  # 도넛 형태 지정
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 호버 툴팁 및 표시 레이블 설정 (편수와 비율 표시)
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}'
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 영화 중 특정 주요 장르의 비중이 높게 형성되어 있으며, 인기 장르 몇 개가 전체 박스오피스 진입작의 과반수를 차지하고 있음을 알 수 있습니다.")

st.markdown("---")

# Section 2: 개봉일 스크린수와 총 관객수의 관계 (산점도)
st.header("2. 개봉일 스크린수와 총 관객수의 관계")

fig2 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title='개봉일 스크린수 vs 총 관객수',
    labels={'first_scrn': '개봉일 스크린수', 'total_audi': '총 관객수', 'genre': '장르'},
    opacity=0.8
)

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 총 관객수가 대체로 증가하는 양의 상관관계를 보이지만, 스크린수에 비해 이례적으로 높은 관객수를 기록한 입소문 흥행작들도 존재합니다.")

st.markdown("---")

# Section 3: 10위권 유지 기간 분포 (히스토그램)
st.header("3. 10위권 진입 기간(일수) 분포")

fig3 = px.histogram(
    df,
    x='days_in_top10',
    nbins=20,
    title='TOP 10 유지 일수 분포',
    labels={'days_in_top10': '10위권에 머문 날수'},
    color_discrete_sequence=['#636EFA']
)

st.plotly_chart(fig3, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 TOP 10에 짧은 기간 머무르고 하락하지만, 일부 장기 흥행작은 한 달 이상 상위권을 유지하는 양극화 현상을 나타냅니다.")
