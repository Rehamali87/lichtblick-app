import random
from uuid import uuid4

import streamlit as st
from streamlit_cookies_controller import CookieController

from db import add_memory, get_memories


# ==================================================
# 🌟 MEIN LICHTBLICK – HIER PROGRAMMIERE ICH!
# ==================================================

APP_NAME = "Lichtblick"
MY_COLOR = "purple"
MY_MESSAGE = "Das Leben hat schöne Momente."
MY_QUESTION = "Was Schönes könnte heute passieren?"


# ==================================================
# 🔴 AB HIER NICHT ÄNDERN!
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💡",
    layout="centered"
)


# ==================================================
# COOKIE CONTROLLER (FEHLERFREI)
# ==================================================

if "cookie_controller" not in st.session_state:
    st.session_state.cookie_controller = CookieController(key="lichtblick_cookie")

cookie_controller = st.session_state.cookie_controller

user_key = cookie_controller.get("user_key", key="get_user_key")

if not user_key:
    user_key = str(uuid4())
    cookie_controller.set(
        "user_key",
        user_key,
        max_age=60 * 60 * 24 * 365,
        key="set_user_key"
    )


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

selected_color = COLORS.get(
    MY_COLOR.lower(),
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

    .main-title {{
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: {selected_color};
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


# ==================================================
# TITEL
# ==================================================

st.markdown('<div class="light">💡</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-title">{APP_NAME} …</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{MY_MESSAGE}</div>', unsafe_allow_html=True)
st.write("")


# ==================================================
# ERINNERUNGEN LADEN
# ==================================================

memories = get_memories(user_key)


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


if st.button("💛 Erinnerung speichern", use_container_width=True):

    if title.strip() or text.strip():

        add_memory(
            user_key=user_key
