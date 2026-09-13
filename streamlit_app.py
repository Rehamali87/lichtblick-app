import streamlit as st
import pandas as pd
import random
import uuid
import datetime
import extra_streamlit_components as stx

from streamlit_gsheets import GSheetsConnection


# ============================================================
# KINDER-BEREICH – HIER KÖNNEN DIE KINDER IHRE APP ANPASSEN
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
# COOKIE MANAGER
# ============================================================

@st.cache_resource
def get_cookie_manager():
    return stx.CookieManager()


cookie_manager = get_cookie_manager()

COOKIE_NAME = "lichtblick_browser_id"

browser_id = cookie_manager.get(COOKIE_NAME)


# ------------------------------------------------------------
# Wenn dieser Browser noch keine ID hat:
# neue zufällige ID erzeugen
# ------------------------------------------------------------

if not browser_id:

    browser_id = str(uuid.uuid4())

    cookie_manager.set(
        COOKIE_NAME,
        browser_id,
        expires_at=datetime.datetime.now()
        + datetime.timedelta(days=3650)
    )

    st.session_state["new_browser"] = True

    st.rerun()


# ============================================================
# GOOGLE SHEETS
# ============================================================

@st.cache_resource
def get_connection():
    return st.connection(
        "gsheets",
        type=GSheetsConnection
    )


conn = get_connection()


# ============================================================
# DATEN LADEN
# ============================================================

def load_memories():

    try:

        df = conn.read(
            worksheet="Sheet1",
            ttl=0
        )

        if df is None or df.empty:
            return pd.DataFrame(
                columns=[
                    "browser_id",
                    "title",
                    "memory",
                    "created_at"
                ]
            )

        df = df.fillna("")

        # Nur Erinnerungen dieses Browsers
        own_memories = df[
            df["browser_id"].astype(str) == str(browser_id)
        ]

        return own_memories

    except Exception as e:

        st.error(
            "Die Datenbank konnte nicht geladen werden."
        )

        st.caption(str(e))

        return pd.DataFrame(
            columns=[
                "browser_id",
                "title",
                "memory",
                "created_at"
            ]
        )


# ============================================================
# DATEN SPEICHERN
# ============================================================

def save_memory(title, memory):

    try:

        df = conn.read(
            worksheet="Sheet1",
            ttl=0
        )

        if df is None or df.empty:

            df = pd.DataFrame(
                columns=[
                    "browser_id",
                    "title",
                    "memory",
                    "created_at"
                ]
            )

        df = df.fillna("")

        new_memory = pd.DataFrame(
            [{
                "browser_id": browser_id,
                "title": title,
                "memory": memory,
                "created_at": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }]
        )

        df = pd.concat(
            [df, new_memory],
            ignore_index=True
        )

        conn.update(
            worksheet="Sheet1",
            data=df
        )

        st.cache_data.clear()

        return True

    except Exception as e:

        st.error(
            "Die Erinnerung konnte nicht gespeichert werden."
        )

        st.caption(str(e))

        return False


# ============================================================
# DESIGN
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


st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: #fff8e8;
    }}

    .main-title {{
        text-align: center;
        font-size: 3.2rem;
        font-weight: 700;
        color: {main_color};
        margin-top: 20px;
        margin-bottom: 5px;
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
        border: 2px solid #eee;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    .memory-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {main_color};
        margin-bottom: 10px;
    }}

    .memory-text {{
        font-size: 1.15rem;
        line-height: 1.6;
        color: #333;
    }}

    .question-card {{
        background: #fff;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        font-size: 1.2rem;
        border: 2px solid #eee;
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
# ERINNERUNG SPEICHERN
# ============================================================

st.markdown("### 🌱 Einen schönen Moment speichern")

title = st.text_input(
    "Was möchtest du speichern?",
    placeholder="Zum Beispiel: Mein Ausflug"
)

memory = st.text_area(
    "Erzähl ein bisschen davon:",
    placeholder="Was war schön? Wer war dabei? Was möchtest du später erinnern?"
)


if st.button(
    "💾 Erinnerung speichern",
    use_container_width=True
):

    if not title.strip():

        st.warning(
            "Gib deiner Erinnerung zuerst einen Titel."
        )

    elif not memory.strip():

        st.warning(
            "Schreib noch kurz auf, was passiert ist."
        )

    else:

        success = save_memory(
            title.strip(),
            memory.strip()
        )

        if success:

            st.success(
                "✨ Deine Erinnerung wurde gespeichert!"
            )

            st.rerun()


# ============================================================
# ERINNERUNG ZUFÄLLIG AUFRUFEN
# ============================================================

st.markdown("---")

st.markdown("### 🔔 Dein Lichtblick")


if st.button(
    "💡 Erinnere mich an etwas Schönes",
    use_container_width=True
):

    memories = load_memories()

    if memories.empty:

        st.info(
            "Du hast noch keine Erinnerung gespeichert."
        )

    else:

        row = memories.sample(1).iloc[0]

        st.markdown(
            f"""
            <div class="memory-card">

                <div class="memory-title">
                    ✨ {row["title"]}
                </div>

                <div class="memory-text">
                    {row["memory"]}
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
# EIGENE ERINNERUNGEN ANZEIGEN
# ============================================================

st.markdown("---")

with st.expander("🌟 Meine gespeicherten Erinnerungen"):

    memories = load_memories()

    if memories.empty:

        st.write(
            "Hier erscheinen deine Erinnerungen."
        )

    else:

        for _, row in memories.iloc[::-1].iterrows():

            st.markdown(
                f"""
                <div class="memory-card">

                    <div class="memory-title">
                        {row["title"]}
                    </div>

                    <div class="memory-text">
                        {row["memory"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
