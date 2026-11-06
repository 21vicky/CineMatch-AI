
import streamlit as st
import html
import textwrap
from recommender import movies, recommend_movies


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. SESSION STATE
# ==========================================

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None


# ==========================================
# 3. CLASSIC CINEMA CSS
# ==========================================

st.markdown(textwrap.dedent("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background: #10141c;
    color: #eee9df;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Hide default Streamlit elements */

#MainMenu, footer, header {
    visibility: hidden;
}

/* NAVIGATION BAR */

.navbar {
    position: sticky;
    top: 0;
    z-index: 999999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1b2029;
    border: 1px solid #62533a;
    border-radius: 10px;
    padding: 16px 25px;
    margin-bottom: 45px;
}

.nav-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 25px;
    font-weight: 700;
    color: #d6b477;
    letter-spacing: 2px;
    white-space: nowrap;
}

.nav-links {
    display: flex;
    gap: 28px;
    align-items: center;
}

.nav-links a {
    color: #ddd4c4;
    text-decoration: none;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    transition: 0.3s ease;
}

.nav-links a:hover,
.nav-links a.active {
    color: #d6b477;
}

.nav-status {
    color: #c9a96e;
    font-size: 11px;
    letter-spacing: 1px;
    white-space: nowrap;
}

/* NAVIGATION TARGETS */

#home,
#discover,
#recommendations,
#about {
    scroll-margin-top: 30px;
}

/* HERO SECTION */

.brand {
    text-align: center;
    color: #c9a96e;
    font-size: 12px;
    letter-spacing: 5px;
    font-weight: 600;
    margin-bottom: 15px;
}

.hero-title {
    text-align: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 72px;
    font-weight: 700;
    color: #f4ead7;
    letter-spacing: 2px;
    margin: 0;
}

.hero-subtitle {
    text-align: center;
    color: #aaa69e;
    font-size: 15px;
    margin-top: 8px;
    margin-bottom: 25px;
}

.gold-line {
    width: 65px;
    height: 2px;
    background: #c9a96e;
    margin: 20px auto 40px auto;
}

/* HEADINGS */

h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #e8d5b3 !important;
}

h2 {
    font-size: 34px !important;
}

/* SELECT BOX */

.stSelectbox label {
    color: #d4c5a5 !important;
    font-weight: 600;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #1b2230;
    border: 1px solid #62533a;
    border-radius: 8px;
    color: #f4ead7;
}

/* BUTTON */

.stButton button {
    background: #c9a96e;
    color: #151820;
    border: none;
    border-radius: 7px;
    font-weight: 700;
    padding: 12px;
    transition: 0.3s ease;
}

.stButton button:hover {
    background: #e1c18a;
    color: #151820;
    transform: translateY(-2px);
}

/* MOVIE CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1a202b;
    border: 1px solid #393c42;
    border-radius: 12px;
    padding: 10px;
    transition: 0.3s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #c9a96e;
}

/* MOVIE DETAILS */

.movie-number {
    color: #c9a96e;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
}

.movie-genre {
    color: #c9a96e;
    font-size: 12px;
    letter-spacing: 1px;
}

.movie-description {
    color: #b9b7b1;
    font-size: 13px;
    line-height: 1.7;
    min-height: 100px;
}

.similarity-text {
    color: #e0c48e;
    font-size: 13px;
    font-weight: 600;
}

/* ALERTS */

div[data-testid="stAlert"] {
    background: #1b2a27;
    border: 1px solid #526c5e;
    color: #e7e4d9;
}

/* DIVIDER */

hr {
    border-color: #34343a;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #827f79;
    font-size: 12px;
    line-height: 2;
    letter-spacing: 1px;
}

/* RESPONSIVE DESIGN */

@media(max-width: 850px) {

    .navbar {
        flex-direction: column;
        gap: 15px;
        padding: 15px 10px;
    }

    .nav-links {
        gap: 15px;
        flex-wrap: wrap;
        justify-content: center;
    }

    .nav-links a {
        font-size: 10px;
    }

    .hero-title {
        font-size: 48px;
    }
}

</style>
"""), unsafe_allow_html=True)


# ==========================================
# 4. NAVIGATION BAR
# ==========================================

# IMPORTANT:
# textwrap.dedent prevents HTML from becoming
# a Markdown code block.

navbar_html = textwrap.dedent("""
<div class="navbar">
<div class="nav-logo">🎬 CINEMATCH</div>
<div class="nav-links">
<a href="#home" class="active">HOME</a>
<a href="#discover">DISCOVER</a>
<a href="#recommendations">RECOMMENDATIONS</a>
<a href="#about">ABOUT</a>
</div>
<div class="nav-status">✦ AI POWERED</div>
</div>
""")

st.markdown(navbar_html, unsafe_allow_html=True)


# ==========================================
# 5. HOME / HERO SECTION
# ==========================================

st.markdown(
    '<div id="home"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand">THE ART OF DISCOVERING FILMS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<h1 class="hero-title">CineMatch AI</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Every great film leads to another.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True
)


# ==========================================
# 6. DISCOVER MOVIES
# ==========================================

st.markdown(
    '<div id="discover"></div>',
    unsafe_allow_html=True
)

st.markdown("## Discover your next film")

st.write(
    "Choose a movie you love. Let our recommendation engine "
    "find films with similar stories and characteristics."
)

movie_list = sorted(
    movies["title"].dropna().unique().tolist()
)

selected_movie = st.selectbox(
    "SELECT YOUR FAVOURITE MOVIE",
    movie_list,
    index=None,
    placeholder="Search for a movie..."
)

recommend_clicked = st.button(
    "✦  FIND MY NEXT MOVIE",
    use_container_width=True
)


# ==========================================
# 7. GENERATE RECOMMENDATIONS
# ==========================================

if recommend_clicked:

    if selected_movie:

        results = recommend_movies(selected_movie, 5)

        st.session_state.recommendations = results
        st.session_state.selected_movie = selected_movie

    else:

        st.warning("Please select a movie first.")


# ==========================================
# 8. DISPLAY RECOMMENDATIONS
# ==========================================

st.markdown(
    '<div id="recommendations"></div>',
    unsafe_allow_html=True
)

results = st.session_state.recommendations

if results is not None:

    st.markdown("---")

    st.markdown("## Selected for you")

    st.caption(
        f"Films inspired by your choice: "
        f"{st.session_state.selected_movie}"
    )

    if results:

        columns = st.columns(3)

        for i, movie in enumerate(results):

            with columns[i % 3]:

                overview = (
                    movie.get("overview")
                    or "No description available."
                )

                short_overview = (
                    overview[:200] + "..."
                    if len(overview) > 200
                    else overview
                )

                title = html.escape(str(movie.get("title", "Untitled")))
                genre = html.escape(
                    str(movie.get("genres") or "GENRE UNAVAILABLE")
                )
                description = html.escape(str(short_overview))

                similarity = movie.get("similarity", 0)

                with st.container(border=True):

                    st.markdown(
                        f'<div class="movie-number">'
                        f'FILM NO. {i + 1:02d}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"### {title}"
                    )

                    st.markdown(
                        f'<div class="movie-genre">'
                        f'{genre}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.write("")

                    st.markdown(
                        f'<div class="movie-description">'
                        f'{description}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.divider()

                    st.markdown(
                        f'<div class="similarity-text">'
                        f'✦ {similarity}% CONTENT SIMILARITY'
                        f'</div>',
                        unsafe_allow_html=True
                    )

    else:

        st.warning("No recommendations found.")


# ==========================================
# 9. ABOUT SECTION
# ==========================================

st.markdown(
    '<div id="about"></div>',
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("## About CineMatch AI")

st.write(
    """
    CineMatch AI is an intelligent movie recommendation platform
    designed to help movie lovers discover films based on their
    favourite movies.

    Our recommendation engine analyses movie characteristics
    and content similarities to suggest your next watch.
    """
)


# ==========================================
# 10. FOOTER
# ==========================================

st.markdown("---")

st.markdown(textwrap.dedent("""
<div class="footer">
MADE WITH PASSION FOR CINEMA
<br>
CINE MATCH AI · DAY 06 · 30 DAYS 30 AI PROJECTS
<br>
PYTHON · MACHINE LEARNING · STREAMLIT
</div>
"""), unsafe_allow_html=True)
