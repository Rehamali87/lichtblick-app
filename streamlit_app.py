import streamlit as st
import random

# --------------------------------
# APP EINSTELLUNGEN
# --------------------------------

st.set_page_config(
    page_title="Das Leben ruft dir",
    page_icon="💡",
    layout="centered"
)

# --------------------------------
# DESIGN
# --------------------------------

st.markdown("""
<style>

body {
    background-color: #fff8e8;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #6f6256;
}

.light {
    text-align: center;
    font-size: 80px;
}

.memory {
    background-color: #fff8e8;
    padding: 20px;
    border-radius: 20px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# TITEL
# --------------------------------

st.markdown(
    '<div class="light">💡</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Das Leben ruft dir …</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Manchmal erinnert dich das Leben an etwas Schönes.'
    '</div>',
    unsafe_allow_html=True
)


st.write("")


# --------------------------------
# ERINNERUNGEN SPEICHERN
# --------------------------------

if "memories" not in st.session_state:
    st.session_state.memories = []


st.header("💛 Eine schöne Erinnerung")


title = st.text_input(
    "Was war schön?",
    placeholder="Zum Beispiel: Mein Geburtstag"
)


text = st.text_area(
    "Erzähl mir davon …",
    placeholder="Warum war dieser Moment schön?"
)


if st.button("💛 Erinnerung speichern"):

    if title or text:

        st.session_state.memories.append({
            "title": title if title else "Ein schöner Moment",
            "text": text if text else "💛"
        })

        st.success(
            "Deine Erinnerung wurde gespeichert. 💛"
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

    if st.session_state.memories:

        memory = random.choice(
            st.session_state.memories
        )

        st.markdown(
            f"""
            <div class="memory">

            <h2>❤️ Erinnerst du dich?</h2>

            <h3>{memory["title"]}</h3>

            <p>{memory["text"]}</p>

            <h3>
            🌿 Das Leben ruft dir zu:
            </h3>

            <p>
            Schau, was Schönes schon da ist.
            </p>

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


if st.session_state.memories:

    for i, memory in enumerate(
        st.session_state.memories
    ):

        st.markdown(
            f"""
            <div class="memory">

            <h3>
            💛 {memory["title"]}
            </h3>

            <p>
            {memory["text"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.write(
        "Noch keine Erinnerungen. 🌱"
    )
