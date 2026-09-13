import streamlit as st
import random
import json
from streamlit_local_storage import LocalStorage


# ============================================================
# EINSTELLUNGEN
# ============================================================

APP_NAME = "Lichtblick"

MY_COLOR = "purple"

MY_MESSAGE = "Das Leben hat schöne Momente."

MY_QUESTION = "Was Schönes könnte heute passieren?"


# ============================================================
# SEITE
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💡",
    layout="centered"
)


# ============================================================
# LOCAL STORAGE
# ============================================================

@st.cache_resource
def get_local_storage():
    return LocalStorage()


localS = get_local_storage()

STORAGE_KEY = "lichtblick_memories"


# ============================================================
# ERINNERUNGEN LADEN
# ============================================================

def load_memories():

    try:
        data = localS.getItem(STORAGE_KEY)

        if not data:
            return []

        if isinstance(data, list):
            return data

        return json.loads(data)

    except Exception:
        return []


# ============================================================
# ERINNERUNGEN SPEICHERN
# ============================================================

def save_memories(memories):

    data = json.dumps(
        memories,
        ensure_ascii=False
    )

    localS.setItem(
        STORAGE_KEY,
        data
    )


# ============================================================
# FARBE
# ============================================================

colors = {
    "purple": "#7B61FF",
    "blue": "#4A90E2",
    "green": "#43A047",
    "orange": "#F39C12",
    "red": "#E85D5D"
}

main_color = colors.get(
    MY_COLOR,
    "#7B61FF"
)


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: #fff8e8;
    }}

    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: {main_color};
        margin-top: 20px;
    }}

    .subtitle {{
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 30px;
    }}

    .memory-card {{
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #eeeeee;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    .memory-title {{
        font-size: 1.4rem;
        font-weight: bold;
        color: {main_color};
        margin-bottom: 10px;
    }}

    .memory-text {{
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
    }}

    .question-card {{
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        font-size: 1.2rem;
        border: 2px solid #eeeeee;
        margin-top: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITEL
# ============================================================

st.markdown(
    f"""
    <div class="main-title">
        💡 {APP_NAME}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="subtitle">
        {MY_MESSAGE}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NEUE ERINNERUNG
# ============================================================

st.markdown("### 🌱 Einen schönen Moment speichern")

title = st.text_input(
    "Titel deiner Erinnerung",
    placeholder="Zum Beispiel: Mein Ausflug"
)

memory = st.text_area(
    "Was möchtest du später erinnern?",
    placeholder="Schreib hier deinen schönen Moment..."
)


if st.button(
    "💾 Erinnerung speichern",
    use_container_width=True
):

    if title.strip() == "":

        st.warning(
            "Bitte gib deiner Erinnerung einen Titel."
        )

    elif memory.strip() == "":

        st.warning(
            "Bitte schreibe etwas über deinen Moment."
        )

    else:

        memories = load_memories()

        memories.append(
            {
                "title": title.strip(),
                "memory": memory.strip()
            }
        )

        save_memories(memories)

        st.success(
            "✨ Deine Erinnerung wurde gespeichert!"
        )

        st.rerun()


# ============================================================
# LICHTBLICK
# ============================================================

st.markdown("---")

st.markdown("### 🔔 Dein Lichtblick")

if st.button(
    "💡 Erinnere mich an etwas Schönes",
    use_container_width=True
):

    memories = load_memories()

    if len(memories) == 0:

        st.info(
            "Du hast noch keine Erinnerung gespeichert."
        )

    else:

        chosen = random.choice(memories)

        st.markdown(
            f"""
            <div class="memory-card">

                <div class="memory-title">
                    ✨ {chosen["title"]}
                </div>

                <div class="memory-text">
                    {chosen["memory"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="question-card">
                💭 {MY_QUESTION}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MEINE ERINNERUNGEN
# ============================================================

st.markdown("---")

with st.expander("🌟 Meine Erinnerungen"):

    memories = load_memories()

    if len(memories) == 0:

        st.write(
            "Hier erscheinen deine gespeicherten Erinnerungen."
        )

    else:

        for item in reversed(memories):

            st.markdown(
                f"""
                <div class="memory-card">

                    <div class="memory-title">
                        {item["title"]}
                    </div>

                    <div class="memory-text">
                        {item["memory"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# INFO
# ============================================================

st.markdown("---")

st.caption(
    "💡 Deine Erinnerungen werden auf diesem Gerät gespeichert."
)
