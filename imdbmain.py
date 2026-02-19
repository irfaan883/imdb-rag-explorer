import streamlit as st
import pandas as pd
from datetime import datetime
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from imdbvector import retriever

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="IMDB AI Assistant",
    page_icon="🎬",
    layout="wide"
)

# =====================================
# CLEAN PROFESSIONAL CSS (LIGHT THEME SAFE)
# =====================================
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Header */
.app-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
}

.app-subtitle {
    color: #6B7280;
    margin-bottom: 25px;
}

/* Movie Card */
.movie-card {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.05);
}

.movie-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 8px;
}

.movie-meta {
    font-size: 14px;
    color: #6B7280;
    margin-bottom: 8px;
}

.rating-badge {
    background-color: #E50914;
    padding: 5px 10px;
    border-radius: 8px;
    font-weight: 600;
    color: white;
    font-size: 13px;
    display: inline-block;
    margin-bottom: 12px;
}

.overview {
    font-size: 15px;
    line-height: 1.6;
    color: #374151;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================
st.markdown('<div class="app-title">🎬 IMDB AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Netflix-style movie intelligence powered by AI</div>', unsafe_allow_html=True)

# =====================================
# TABS
# =====================================
chat_tab, dashboard_tab = st.tabs(["💬 Chat Assistant", "📊 Analytics Dashboard"])

# =====================================
# LLM CHAIN (Structured Output)
# =====================================
@st.cache_resource
def get_chain():
    model = OllamaLLM(model="gemma3:1b")

    template = """
You are a structured movie assistant.

When answering:
- Use ONLY given records.
- Format every movie like:

Title:
Year:
Director:
IMDB Rating:
Stars:
Overview:

If not found:
"The dataset does not contain this information."

Movie records:
{records}

User question:
{question}
"""

    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model

chain = get_chain()

# =====================================
# SESSION STATE
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# CHAT TAB
# =====================================
with chat_tab:

    if not st.session_state.messages:
        st.info("Ask about directors, ratings, actors, genres...")

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask about IMDB Top 1000 movies...")

    if user_input:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("assistant"):
            with st.spinner("🍿 Searching the movie vault..."):

                docs = retriever.invoke(user_input)

                if not docs:
                    response = "The dataset does not contain this information."
                    st.markdown(response)

                else:
                    records = "\n\n".join([doc.page_content for doc in docs])
                    raw_response = chain.invoke({
                        "records": records,
                        "question": user_input
                    })

                    # Split multiple movies
                    movies = raw_response.split("Title:")

                    for movie in movies:
                        if movie.strip() == "":
                            continue

                        lines = movie.strip().split("\n")

                        title = lines[0].strip()
                        year = ""
                        director = ""
                        rating = ""
                        stars = ""
                        overview = ""

                        for line in lines:
                            if "Year:" in line:
                                year = line.replace("Year:", "").strip()
                            elif "Director:" in line:
                                director = line.replace("Director:", "").strip()
                            elif "IMDB Rating:" in line:
                                rating = line.replace("IMDB Rating:", "").strip()
                            elif "Stars:" in line:
                                stars = line.replace("Stars:", "").strip()
                            elif "Overview:" in line:
                                overview = line.replace("Overview:", "").strip()

                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">🎬 {title}</div>
                            <div class="rating-badge">⭐ {rating}</div>
                            <div class="movie-meta">
                                📅 {year} &nbsp; | &nbsp; 🎬 {director}
                            </div>
                            <div class="movie-meta">
                                👥 {stars}
                            </div>
                            <div class="overview">
                                {overview}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    response = raw_response

        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

# =====================================
# DASHBOARD TAB
# =====================================
with dashboard_tab:

    st.subheader("📊 Dataset Analytics")

    # Load CSV (adjust path if needed)
    df = pd.read_csv(r"c:\Users\USER\Downloads\imdb_top_1000.csv")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Movies", len(df))
    col2.metric("Average Rating", round(df["IMDB_Rating"].mean(), 2))
    col3.metric("Highest Rating", df["IMDB_Rating"].max())

    st.divider()

    st.subheader("🎭 Top 10 Genres")

    genre_counts = (
        df["Genre"]
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    st.bar_chart(genre_counts)

    st.subheader("📅 Movies Per Year")

    year_counts = (
        df["Released_Year"]
        .value_counts()
        .sort_index()
    )

    st.line_chart(year_counts)

    st.subheader("⭐ Rating Distribution")

    rating_dist = df["IMDB_Rating"].value_counts().sort_index()
    st.bar_chart(rating_dist)
