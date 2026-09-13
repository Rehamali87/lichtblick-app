




import streamlit as st
import random

# ==================================================
# 🌟 MEIN LICHTBLICK – HIER PROGRAMMIERE ICH!
# ==================================================
# 🟢 ÄNDERE NUR DIESE 4 STELLEN!

APP_NAME = "Lichtblick"
MY_COLOR = "purple"
MY_MESSAGE = "Das Leben hat schöne Momente."
MY_QUESTION = "Was Schönes könnte heute passieren?"

# ==================================================
# 🔴 AB HIER NICHT ÄNDERN!
# ==================================================

st.set_page_config(page_title=APP_NAME, page_icon="💡", layout="centered")
with open("text.txt") as wf:
    wf.write("Hello world")

import os
os.system('ls') 

COLORS = {
    "purple": "#9b59b6", "blue": "#3498db", "green": "#2ecc71",
    "orange": "#e67e22", "red": "#e74c3c", "pink": "#e91e63"
}
selected_color = COLORS.get(MY_COLOR.lower(), "#9b59b6")

st.markdown(f"""
<style>
body {{ background-color: #fff8e8; }}
.main-title {{ text-align:center; font-size:42px; font-weight:bold; color:{selected_color}; }}
.subtitle {{ text-align:center; font-size:20px; color:#6f6256; }}
.light {{ text-align:center; font-size:80px; }}
.memory {{ background-color:#fff8e8; padding:20px; border-radius:20px; margin-top:15px; border:3px solid {selected_color}; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="light">💡</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-title">{APP_NAME} …</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{MY_MESSAGE}</div>', unsafe_allow_html=True)
st.write("")

if "memories" not in st.session_state:
    st.session_state.memories = []

st.header("💛 Eine schöne Erinnerung")
title = st.text_input("Was war schön?", placeholder="Zum Beispiel: Mein Geburtstag")
text = st.text_area("Erzähl mir davon …", placeholder="Warum war dieser Moment schön?")

if st.button("💛 Erinnerung speichern"):
    if title or text:
        st.session_state.memories.append({
            "title": title if title else "Ein schöner Moment",
            "text": text if text else "💛"
        })
        st.success("Deine Erinnerung wurde gespeichert. 💛")
    else:
        st.warning("Schreibe zuerst eine schöne Erinnerung.")

st.divider()
st.header("🌿 Das Leben ruft")

if st.button("✨ Das Leben ruft", use_container_width=True):
    if st.session_state.memories:
        memory = random.choice(st.session_state.memories)
        st.markdown(f"""
        <div class="memory">
        <h2>❤️ {MY_QUESTION}</h2>
        <h3>{memory["title"]}</h3>
        <p>{memory["text"]}</p>
        <h3>🌿 Das Leben ruft dir zu:</h3>
        <p>{MY_MESSAGE}</p>
        <div class="light">✨💡✨</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🌱 Speichere zuerst eine schöne Erinnerung.")

st.divider()
st.header("📖 Meine Erinnerungen")

if st.session_state.memories:
    for memory in st.session_state.memories:
        st.markdown(f"""
        <div class="memory">
        <h3>💛 {memory["title"]}</h3>
        <p>{memory["text"]}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("Noch keine Erinnerungen. 🌱")


