import streamlit as st
import random


# =========================================================
# DEINE EINSTELLUNGEN
# =========================================================

APP_NAME = "Lichtblick"

MY_MESSAGE = "Das Leben hat schöne Momente."

MY_QUESTION = "Was Schönes könnte heute passieren?"

MY_COLOR = "#7B61FF"


# =========================================================
# SEITE
# =========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💡",
    layout="centered"
)


# =========================================================
# SPEICHER
# =========================================================

if "memories" not in st.session_state:
    st.session_state.memories = []


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: #fff8e8;
    }}

    .title {{
        text-align: center;
        color: {MY_COLOR};
        font-size: 3rem;
        font-weight: bold;
        margin-top: 20px;
    }}

    .subtitle {{
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }}

    .card {{
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
        border: 2px solid #eeeeee;
    }}

    .memory-title {{
        color: {MY_COLOR};
        font-size: 1.4rem;
        font-weight: bold;
    }}

    .memory-text {{
        color: #333;
        font-size: 1.1rem;
        margin-top: 10px;
    }}

    .question {{
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITEL
# =========================================================

st.markdown(
    f'<div class="title">💡 {APP_NAME}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{MY_MESSAGE}</div>',
    unsafe_allow_html=True
)


# =========================================================
# ERINNERUNG SPEICHERN
# =========================================================

st.markdown("### 🌱 Einen schönen Moment speichern")

title = st.text_input(
    "Titel",
    placeholder="Zum Beispiel: Mein Geburtstag"
)

memory = st.text_area(
    "Was möchtest du erinnern?",
    placeholder="Schreibe hier deinen schönen Moment..."
)


if st.button(
    "💾 Erinnerung speichern",
    use_container_width=True
):

    if title.strip() == "":
        st.warning("Bitte gib einen Titel ein.")

    elif memory.strip() == "":
        st.warning("Bitte schreibe etwas über deinen Moment.")

    else:

        st.session_state.memories.append(
            {
                "title": title.strip(),
                "text": memory.strip()
            }
        )

        st.success("✨ Deine Erinnerung wurde gespeichert!")

        st.rerun()


# =========================================================
# LICHTBLICK
# =========================================================

st.markdown("---")

st.markdown("### 🔔 Dein Lichtblick")

if st.button(
    "💡 Erinnere mich an etwas Schönes",
    use_container_width=True
):

    if len(st.session_state.memories) == 0:

        st.info(
            "Du hast noch keine Erinnerung gespeichert."
        )

    else:

        chosen = random.choice(
            st.session_state.memories
        )

        st.markdown(
            f"""
            <div class="card">

                <div class="memory-title">
                    ✨ {chosen["title"]}
                </div>

                <div class="memory-text">
                    {chosen["text"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="question">
                💭 {MY_QUESTION}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# MEINE ERINNERUNGEN
# =========================================================

st.markdown("---")

st.markdown("### 🌟 Meine Erinnerungen")

if len(st.session_state.memories) == 0:

    st.write(
        "Du hast noch keine Erinnerungen gespeichert."
    )

else:

    for item in reversed(
        st.session_state.memories
    ):

        st.markdown(
            f"""
            <div class="card">

                <div class="memory-title">
                    {item["title"]}
                </div>

                <div class="memory-text">
                    {item["text"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )
