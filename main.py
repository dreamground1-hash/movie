import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: 세로막대 기호(|)로 분리된 경우 첫 번째 장르만 사용
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if x != 'nan' else '미상')
        
    return df

try:
    df = load_data()
    
    # Header Info
    st.subheader("📊 장르별 영화 편수 분석")
    
    # 1. 장르별 영화 편수 집계
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'count']
    
    # 2. Plotly Donut Chart 생성
    fig = px.pie(
        genre_counts, 
        names='genre', 
        values='count', 
        hole=0.4,
        title="장르별 영화 편수 및 비율 도넛 그래프"
    )
    
    # 툴팁(마우스 호버) 설정: 장르명, 편수, 비율
    fig.update_traces(
        hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
        textinfo="label+percent"
    )
    
    fig.update_layout(
        margin=dict(t=50, b=20, l=20, r=20),
        legend_title_text="장르"
    )
    
    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 시각적 구역 구분을 위한 구분선
    st.markdown("---")
    
    # 그래프 설명 구역
    st.info("💡 **이 그래프로 알 수 있는 것:** 최근 1년간 박스오피스 상위권에 진입한 주요 영화들의 장르 분포 현황과 특정 인기 장르의 집중도를 한눈에 파악할 수 있습니다.")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
