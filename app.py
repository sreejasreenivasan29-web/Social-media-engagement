import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Social Media Engagement Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement.csv")
    df['post_time'] = pd.to_datetime(df['post_time'])
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Filters")

platform = st.sidebar.multiselect(
    "Select Platform",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)

post_type = st.sidebar.multiselect(
    "Select Post Type",
    options=df["post_type"].unique(),
    default=df["post_type"].unique()
)

sentiment = st.sidebar.multiselect(
    "Select Sentiment",
    options=df["sentiment_score"].unique(),
    default=df["sentiment_score"].unique()
)

filtered_df = df[
    (df["platform"].isin(platform)) &
    (df["post_type"].isin(post_type)) &
    (df["sentiment_score"].isin(sentiment))
]

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4F46E5;'>
    Social Media Engagement Analysis
    </h1>
    <p style='text-align: center; font-size:18px;'>
    Analyze likes, comments, and shares across platforms and content types
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric(
    label="👍 Total Likes",
    value=f"{filtered_df['likes'].sum():,}"
)

col2.metric(
    label="💬 Total Comments",
    value=f"{filtered_df['comments'].sum():,}"
)

col3.metric(
    label="🔁 Total Shares",
    value=f"{filtered_df['shares'].sum():,}"
)

st.markdown("---")

# ---------------- CHARTS ----------------
col4, col5 = st.columns(2)

# Likes by Platform
fig1 = px.bar(
    filtered_df.groupby("platform", as_index=False)["likes"].sum(),
    x="platform",
    y="likes",
    title="Total Likes by Platform",
    color="platform"
)
col4.plotly_chart(fig1, use_container_width=True)

# Engagement by Post Type
fig2 = px.pie(
    filtered_df,
    names="post_type",
    values="likes",
    title="Likes Distribution by Post Type"
)
col5.plotly_chart(fig2, use_container_width=True)

# ---------------- SENTIMENT ANALYSIS ----------------
st.markdown("### 📈 Sentiment-wise Engagement")

fig3 = px.box(
    filtered_df,
    x="sentiment_score",
    y="likes",
    color="sentiment_score",
    title="Likes vs Sentiment"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- DATA PREVIEW ----------------
with st.expander("🔍 View Dataset"):
    st.dataframe(filtered_df)