import streamlit as st
import requests
import random
import html


# ==================================================
# 🌟 HIER KANNST DU PROGRAMMIEREN
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
# SUPABASE
# ==================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_PUBLISHABLE_KEY"]


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

COLOR = COLORS.get(MY_COLOR, "#9b59b6")


# ==================================================
# DESIGN
# ==================================================

st.markdown(
    f"""
    <style>

    .main {{
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
        background-color: #fff8e8;
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
# FUNKTION: DATENBANK ANSPRECHEN
# ==================================================

def supabase_request(method, table, params=None, data=None):

    url = f"{SUPABASE_URL}/rest/v1/{table}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=data,
        timeout=10
    )

    if response.status_code >= 400:
        raise Exception(response.text)

    if response.text:
        return response.json()

    return []


# ==================================================
# ERINNERUNGEN LADEN
# ==================================================

def load_memories(child_code):

    return supabase_request(
        "GET",
        "memories",
        params={
            "select": "id,child_code,title,text,created_at",
            "child_code": f"eq.{child_code}",
            "order": "created_at.desc"
        }
    )


# ==================================================
# ERINNERUNG SPEICHERN
# ==================================================

def save_memory(child_code, title, text):

    return supabase_request(
        "POST",
        "memories",
        data={
            "child_code": child_code,
            "title": title,
            "text": text
        }
    )


# ==================================================
# APP
# ==================================================

st.markdown(
    '<div class="light">💡</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="title">{html.escape(APP_NAME)} …</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{html.escape(MY_MESSAGE)}</div>',
    unsafe_allow_html=True
)


# ==================================================
# KIND
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
# SCHÖNE ERINNERUNG
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

    if not title.strip() and not text.strip():

        st.warning(
            "Schreibe zuerst eine schöne Erinnerung."
        )

    else:

        try:

            save_memory(
                child_code,
                title.strip() or "Ein schöner Moment",
                text.strip() or "💛"
            )

            st.success(
                "💛 Deine Erinnerung wurde gespeichert!"
            )

        except Exception as error:

            st.error(
                "Die Erinnerung konnte nicht gespeichert werden."
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

    try:

        memories = load_memories(child_code)

        if memories:

            memory = random.choice(memories)

            st.markdown(
                f"""
                <div class="memory">

                <h2>❤️ Erinnerst du dich?</h2>

                <h3>
                {html.escape(memory["title"])}
                </h3>

                <p>
                {html.escape(memory["text"])}
                </p>

                <h3>
                🌿 Das Leben ruft dir zu:
                </h3>

                <p>
                {html.escape(MY_MESSAGE)}
                </p>

                <h3>
                ❓ {html.escape(MY_QUESTION)}
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
                "🌱 Du hast noch keine Erinnerung gespeichert."
            )

    except Exception:

        st.error(
            "Die Erinnerungen konnten nicht geladen werden."
        )


# ==================================================
# MEINE ERINNERUNGEN
# ==================================================

st.divider()

st.header("📖 Meine Erinnerungen")


try:

    memories = load_memories(child_code)

    if memories:

        for memory in memories:

            st.markdown(
                f"""
                <div class="memory">

                <h3>
                💛 {html.escape(memory["title"])}
                </h3>

                <p>
                {html.escape(memory["text"])}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.write(
            "Noch keine Erinnerungen. 🌱"
        )

except Exception:

    st.error(
        "Die Erinnerungen konnten nicht geladen werden."
    )
