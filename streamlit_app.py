import streamlit as st
import random
import html
from supabase import create_client, Client


# ==================================================
# 🌟 MEIN LICHTBLICK – HIER PROGRAMMIERE ICH!
# ==================================================

# 🟢 ÄNDERE NUR DIE STELLEN IN DIESEM BEREICH!


# ✏️ 1. DEIN APP-NAME
APP_NAME = "Lichtblick"


# 🎨 2. DEINE FARBE
# Probiere:
# "purple", "blue", "green", "orange", "red", "pink"

MY_COLOR = "purple"


# 💬 3. DEINE SCHÖNE NACHRICHT
MY_MESSAGE = "Das Leben hat schöne Momente."


# ❓ 4. DEINE EIGENE FRAGE
MY_QUESTION = "Was Schönes könnte heute passieren?"


# ==================================================
# 🔴 AB HIER NICHT ÄNDERN!
# ==================================================


# --------------------------------
# APP EINSTELLUNGEN
# --------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💡",
    layout="centered"
)


# --------------------------------
# SUPABASE VERBINDUNG
# --------------------------------

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_PUBLISHABLE_KEY"]
    )


try:
    supabase = get_supabase()
except Exception:
    st.error(
        "⚠️ Die Datenbank ist noch nicht verbunden.\n\n"
        "Bitte überprüfe die Supabase-Einstellungen."
    )
    st.stop()


# --------------------------------
# DESIGN
# --------------------------------

COLORS = {
    "purple": "#9b59b6",
    "blue": "#3498db",
    "green": "#2ecc71",
    "orange": "#e67e22",
    "red": "#e74c3c",
    "pink": "#e91e63"
}

selected_color = COLORS.get(
    MY_COLOR,
    "#9b59b6"
)


st.markdown(
    f"""
    <style>

    body {{
        background-color: #fff8e8;
    }}

    .main-title {{
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
        font-size: 80px;
    }}

    .memory {{
        background-color: #fff8e8;
        padding: 20px;
        border-radius: 20px;
        margin-top: 15px;
        border: 3px solid {selected_color};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# KIND AUSWÄHLEN
# --------------------------------

st.markdown(
    '<div class="light">💡</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="main-title">{html.escape(APP_NAME)} …</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{html.escape(MY_MESSAGE)}</div>',
    unsafe_allow_html=True
)

st.write("")


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


# --------------------------------
# ERINNERUNGEN AUS DATENBANK LADEN
# --------------------------------

def load_memories(child_code):

    response = (
        supabase
        .table("memories")
        .select("id, title, text, created_at")
        .eq("child_code", child_code)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


memories = load_memories(child_code)


# --------------------------------
# ERINNERUNG SPEICHERN
# --------------------------------

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

    if title.strip() or text.strip():

        try:

            supabase.table("memories").insert(
                {
                    "child_code": child_code,
                    "title": title.strip()
                    if title.strip()
                    else "Ein schöner Moment",
                    "text": text.strip()
                    if text.strip()
                    else "💛"
                }
            ).execute()

            st.success(
                "Deine Erinnerung wurde dauerhaft gespeichert. 💛"
            )

            st.rerun()

        except Exception as e:

            st.error(
                "Die Erinnerung konnte nicht gespeichert werden."
            )

    else:

        st.warning(
            "Schreibe zuerst eine schöne Erinnerung."
        )


# --------------------------------
# DAS LEBEN RUFT
# --------------------------------

st.divider()

st.header("🌿 Das Leben ruft")


if st.button(
    "✨ Das Leben ruft",
    use_container_width=True
):

    # Datenbank neu laden
    memories = load_memories(child_code)

    if memories:

        memory = random.choice(memories)

        memory_title = html.escape(
            memory.get("title", "")
        )

        memory_text = html.escape(
            memory.get("text", "")
        )

        message = html.escape(
            MY_MESSAGE
        )

        question = html.escape(
            MY_QUESTION
        )

        st.markdown(
            f"""
            <div class="memory">

            <h2>❤️ Erinnerst du dich?</h2>

            <h3>{memory_title}</h3>

            <p>{memory_text}</p>

            <h3>
            🌿 Das Leben ruft dir zu:
            </h3>

            <p>
            {message}
            </p>

            <h3>
            ❓ {question}
            </h3>

            <div class="light">
            ✨💡✨
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "🌱 Speichere zuerst eine schöne Erinnerung."
        )


# --------------------------------
# ALLE ERINNERUNGEN
# --------------------------------

st.divider()

st.header("📖 Meine Erinnerungen")


memories = load_memories(child_code)


if memories:

    for memory in memories:

        memory_title = html.escape(
            memory.get("title", "")
        )

        memory_text = html.escape(
            memory.get("text", "")
        )

        st.markdown(
            f"""
            <div class="memory">

            <h3>
            💛 {memory_title}
            </h3>

            <p>
            {memory_text}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.write(
        "Noch keine Erinnerungen. 🌱"
    )
