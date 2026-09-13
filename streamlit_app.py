import streamlit as st
import sqlite3
import random
import html


# ==================================================
# 🌟 HIER KANNST DU DEINE APP ÄNDERN
# ==================================================

APP_NAME = "Lichtblick"

MY_COLOR = "purple"

MY_MESSAGE = "Das Leben hat schöne Momente."

MY_QUESTION = "Was Schönes könnte heute passieren?"


# ==================================================
# 🔴 AB HIER NICHT ÄNDERN
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💡",
    layout="centered"
)


# ==================================================
# DATENBANK
# ==================================================

DATABASE = "lichtblick.db"


def get_connection():
    return sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_code TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


create_database()


# ==================================================
# ERINNERUNG SPEICHERN
# ==================================================

def save_memory(child_code, title, text):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memories
        (child_code, title, text)
        VALUES (?, ?, ?)
        """,
        (child_code, title, text)
    )

    conn.commit()
    conn.close()


# ==================================================
# ERINNERUNGEN LADEN
# ==================================================

def load_memories(child_code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, text, created_at
        FROM memories
        WHERE child_code = ?
        ORDER BY created_at DESC
        """,
        (child_code,)
    )

    memories = cursor.fetchall()

    conn.close()

    return memories


# ==================================================
# FARBEN
# ==================================================

COLORS = {
    "purple": "#9b59b6",
    "blue": "#3498db",
    "green": "#2ecc71",
    "orange": "#e67e22",
    "red": "#e74c3c",
    "pink": "#e91e63"
}

COLOR = COLORS.get(
    MY_COLOR,
    "#9b59b6"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: #fff8e8;
    }}

    .title {{
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }}

    .subtitle {{
        text-align: center;
        font-size: 20px;
        color: #6f6256;
    }}

    .light {{
        text-align: center;
        font-size: 75px;
    }}

    .memory {{
        background-color: #fffdf5;
        border: 3px solid {COLOR};
        border-radius: 20px;
        padding: 20px;
        margin-top: 15px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# START
# ==================================================

st.markdown(
    '<div class="light">💡</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="title">{html.escape(APP_NAME)}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{html.escape(MY_MESSAGE)}</div>',
    unsafe_allow_html=True
)

st.write("")


# ==================================================
# KIND AUSWÄHLEN
# ==================================================

st.header("👋 Wer bist du?")

child_code = st.selectbox(
    "Wähle deinen Code:",
    [
        "K01",
        "K02",
        "K03",
        "K04",
        "K05",
        "K06",
        "K07",
        "K08",
        "K09",
        "K10",
        "K11",
        "K12"
    ]
)


# ==================================================
# ERINNERUNG SPEICHERN
# ==================================================

st.header("💛 Eine schöne Erinnerung")

title = st.text_input(
    "Was war schön?",
    placeholder="Zum Beispiel: Mein Geburtstag"
)

text = st.text_area(
    "Erzähl mir davon …",
    placeholder="Warum war dieser Moment schön?"
)


if st.button(
    "💛 Erinnerung speichern",
    use_container_width=True
):

    if title.strip() and text.strip():

        save_memory(
            child_code,
            title.strip(),
            text.strip()
        )

        st.success(
            "💛 Deine Erinnerung wurde gespeichert!"
        )

        st.rerun()

    else:

        st.warning(
            "Bitte fülle beide Felder aus."
        )


# ==================================================
# DAS LEBEN RUFT
# ==================================================

st.divider()

st.header("🌿 Das Leben ruft")

if st.button(
    "✨ Das Leben ruft",
    use_container_width=True
):

    memories = load_memories(child_code)

    if memories:

        memory = random.choice(memories)

        memory_title = html.escape(memory[1])
        memory_text = html.escape(memory[2])

        st.markdown(
            f"""
            <div class="memory">

            <h2>❤️ Erinnerst du dich?</h2>

            <h3>{memory_title}</h3>

            <p>{memory_text}</p>

            <h3>🌿 Das Leben ruft dir zu:</h3>

            <p>{html.escape(MY_MESSAGE)}</p>

            <h3>❓ {html.escape(MY_QUESTION)}</h3>

            <div class="light">
            ✨💡✨
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "🌱 Du hast noch keine Erinnerung gespeichert."
        )


# ==================================================
# MEINE ERINNERUNGEN
# ==================================================

st.divider()

st.header("📖 Meine Erinnerungen")

memories = load_memories(child_code)

if memories:

    for memory in memories:

        memory_title = html.escape(memory[1])
        memory_text = html.escape(memory[2])

        st.markdown(
            f"""
            <div class="memory">

            <h3>💛 {memory_title}</h3>

            <p>{memory_text}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.write(
        "Noch keine Erinnerungen. 🌱"
    )
