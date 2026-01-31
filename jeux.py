import json
import time
from pathlib import Path
import streamlit as st

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="L’Œuvre en Jeu",
    page_icon="📚",
    layout="centered"
)

DATA_FILE = "data.json"

# =============================
# THEME TERRACOTTA (SANS IMAGE)
# =============================
def apply_terracotta_theme():
    st.markdown(
        """
        <style>
        :root {
            --terracotta: #C46A45;
            --terracotta-dark: #8F3E24;
            --sand: #F3E7D3;
            --cream: #FFF7EA;
            --ink: #2B1D14;
            --ink-soft: rgba(43,29,20,0.8);
            --card: #FFF9F0;
            --border: rgba(140, 95, 70, 0.25);
        }

        /* Fond général */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #F6EBDD 0%, #EFE0CF 100%);
        }

        .stApp {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        footer { visibility: hidden; }

        /* Container */
        .block-container {
            max-width: 950px;
            padding-top: 2.2rem;
            padding-bottom: 2rem;
        }

        /* TITRE */
        h1 {
            font-size: 44px !important;
            font-weight: 900;
            color: var(--terracotta-dark);
        }

        .subtitle {
            font-size: 18px;
            color: var(--ink-soft);
            margin-bottom: 22px;
        }

        /* BADGES */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            border-radius: 999px;
            background: var(--cream);
            border: 1px solid var(--border);
            color: var(--ink);
            font-weight: 800;
            font-size: 16px;
            margin: 0 10px 10px 0;
        }

        /* CARTE PRINCIPALE */
        .card {
            margin-top: 12px;
            padding: 34px;
            border-radius: 26px;
            background: var(--card);
            border: 1px solid var(--border);
            box-shadow: 0 12px 28px rgba(0,0,0,0.12);
        }

        /* QUESTION */
        .card h2, .card h3 {
            font-size: 30px !important;
            font-weight: 900 !important;
            color: var(--ink) !important;
            line-height: 1.3;
        }

        /* AIDE */
        .help {
            font-size: 17px;
            color: var(--ink-soft);
            margin-bottom: 16px;
        }

        /* REPONSES (RADIO) */
        div[role="radiogroup"] label {
            background: #FFFFFF;
            border: 1px solid var(--border);
            padding: 14px 16px;
            margin: 12px 0;
            border-radius: 18px;
        }

        div[role="radiogroup"] label p {
            font-size: 20px !important;
            font-weight: 700;
            color: var(--ink) !important;
        }

        /* BOUTONS */
        div.stButton > button {
            border-radius: 18px !important;
            padding: 1rem 1.2rem !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            background: var(--terracotta) !important;
            color: white !important;
            border: none !important;
        }

        div.stButton > button:hover {
            background: var(--terracotta-dark) !important;
        }

        /* ALERTES */
        .stAlert {
            font-size: 18px;
            border-radius: 18px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

apply_terracotta_theme()

# =============================
# LOAD QUESTIONS
# =============================
def load_questions():
    path = Path(__file__).parent / DATA_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()
N = len(questions)

# =============================
# SESSION STATE
# =============================
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "i" not in st.session_state:
    st.session_state.i = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "TIME_LIMIT" not in st.session_state:
    st.session_state.TIME_LIMIT = 30
if "last_choice" not in st.session_state:
    st.session_state.last_choice = None

# =============================
# HELPERS
# =============================
def reset_game():
    st.session_state.screen = "home"
    st.session_state.i = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.start_time = time.time()

def start_game(limit):
    st.session_state.screen = "quiz"
    st.session_state.i = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.TIME_LIMIT = limit
    st.session_state.start_time = time.time()

def next_question():
    st.session_state.i += 1
    st.session_state.answered = False
    st.session_state.start_time = time.time()
    if st.session_state.i >= N:
        st.session_state.screen = "end"

# =============================
# HEADER
# =============================
st.title("📚 L’Œuvre en Jeu")
st.markdown("<div class='subtitle'>Jeu éducatif de culture littéraire</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <span class='badge'>📘 {N} questions</span>
    <span class='badge'>⭐ Score : {st.session_state.score}</span>
    """,
    unsafe_allow_html=True
)

row = st.columns([6,2])
with row[1]:
    if st.button("🔁 Recommencer", use_container_width=True):
        reset_game()
        st.rerun()

# =============================
# HOME
# =============================
if st.session_state.screen == "home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎮 Bienvenue")
    st.write("Réponds aux questions avant la fin du temps ⏳.")

    mode = st.radio(
        "Temps par question :",
        ["30 secondes", "45 secondes", "60 secondes"]
    )
    limit = 30 if "30" in mode else 45 if "45" in mode else 60

    if st.button("🚀 Commencer le jeu", use_container_width=True):
        start_game(limit)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =============================
# END
# =============================
if st.session_state.screen == "end":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏁 Fin du jeu")
    st.write(f"Score final : **{st.session_state.score} / {N}**")

    st.text_area("🧠 Une œuvre qui t’a marqué ?", height=100)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =============================
# QUIZ
# =============================
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(st.session_state.TIME_LIMIT - elapsed, 0)

st.markdown(
    f"""
    <span class='badge'>⏳ {remaining}s</span>
    <span class='badge'>📊 {st.session_state.i+1}/{N}</span>
    """,
    unsafe_allow_html=True
)

if remaining == 0:
    next_question()
    st.rerun()

q = questions[st.session_state.i]
correct = q["options"][q["answer_index"]]

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader(q["question"])
st.markdown("<div class='help'>Choisis une réponse puis clique sur Valider.</div>", unsafe_allow_html=True)

choice = st.radio("Réponses", q["options"], disabled=st.session_state.answered)

colA, colB = st.columns(2)

with colA:
    if st.button("✅ Valider", disabled=st.session_state.answered, use_container_width=True):
        if choice == correct:
            st.success("Bonne réponse 🎉")
            st.session_state.score += 1
        else:
            st.error(f"Mauvaise réponse ❌ — {correct}")
        st.session_state.answered = True

with colB:
    if st.button("➡️ Suivant", disabled=not st.session_state.answered, use_container_width=True):
        next_question()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
