import streamlit as st
from datetime import datetime
import time
import base64
import os
import random

# --- Password gate ---
if st.query_params.get("key") != "ahoi":
    st.error("Access Denied. You need the secret link to view this app.")
    st.stop()


# --- Helper: encode images for CSS ---
def get_base64_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


sky_encoded = get_base64_image("assets/sky.avif")
man_encoded = get_base64_image("assets/miles_pixelhug_free.png")
woman_encoded = get_base64_image("assets/alica_pixelhug_free.png")

# --- Progress Calculation ---
progress_start = datetime(2026, 9, 19)
progress_end = datetime(2026, 11, 23)
elapsed = (datetime.now() - progress_start).total_seconds()
total_duration = (progress_end - progress_start).total_seconds()
progress_percent = round(max(0.0, min(1.0, elapsed / total_duration)) * 100, 2)

# --- Alles CSS (Zentral und aufgeräumt) ---
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    * {{ font-family: 'Poppins', sans-serif !important; color: darkblue !important; }}

    .stApp {{
        background-image: url("data:image/avif;base64,{sky_encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Quiz Antworten Style (Secondary Buttons) */
    div[data-testid="stButton"] > button[kind="secondary"] {{
        background-color: #d0e8f2 !important; 
        border: 2px solid darkblue !important;
        border-radius: 12px !important;
        color: darkblue !important;
        transition: all 0.3s ease;
    }}
    div[data-testid="stButton"] > button[kind="secondary"]:hover {{
        background-color: #a8d5e5 !important; 
        transform: scale(1.02);
    }}

    /* CSS Trick um Buttons AUF die Umschläge zu ziehen */
    div.element-container:has(#quiz-anchor) + div.element-container,
    div.element-container:has(#text-anchor) + div.element-container {{
        margin-top: -85px;  /* HIER ANPASSEN falls der Button zu hoch/tief ist */
        position: relative;
        z-index: 10;
        width: 80%;
        margin-left: 10%;
        padding-bottom: 30px;
    }}

    /* Animation Track */
    .animation-track {{
        position: relative; width: 100%; height: 210px; margin: 25px 0 10px 0;
        background: rgba(255, 255, 255, 0.4); border-radius: 20px;
        border: 2px dashed rgba(0, 0, 139, 0.35); box-sizing: border-box; overflow: hidden;
    }}
    .track-ground {{ position: absolute; bottom: 12px; left: 2%; width: 96%; height: 6px; background: rgba(0, 0, 139, 0.15); border-radius: 3px; }}
    .track-fill {{ position: absolute; bottom: 12px; left: 2%; width: calc({progress_percent}% * 0.96); height: 6px; background: rgba(0, 0, 139, 0.55); border-radius: 3px; transform-origin: left; }}
    .sprite-destination {{ position: absolute; right: 15px; bottom: 16px; height: 200px; width: auto; z-index: 2; transform: scaleX(-1); }}
    .sprite-walker {{ position: absolute; bottom: 16px; left: calc(10px + ({progress_percent} / 100) * (100% - 110px)); height: 200px; width: auto; z-index: 3; transform: scaleX(-1); }}
    </style>
    """, unsafe_allow_html=True
)

# --- Title ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Hallo Süße <3")
    st.write(
        "Das hier ist jetzt deine Website bis ich wieder in Würzburg bin. "
        "Hier findest du vorallem Countdowns, wann wir uns wieder sehen und ein paar süße Bilder. "
        "In einem Umschlag findest du außerdem ein kleines Quiz!")
with col2:
    st.image("assets/zeiger.png", width="stretch")

st.divider()

# --- Zufälliges Bild ---
if "random_image" not in st.session_state:
    folder_path = "assets/random_pics"
    if os.path.exists(folder_path):
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp'))]
        st.session_state.random_image = os.path.join(folder_path, random.choice(images)) if images else None
    else:
        st.session_state.random_image = None

if st.session_state.random_image:
    img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
    with img_col2:
        st.image(st.session_state.random_image, width="stretch")
else:
    st.info("Bitte erstelle den Ordner 'assets/random_pics' und lege Bilder hinein!")

st.divider()


# --- Countdowns ---
def show_countdown(label: str, target_date: datetime):
    time_until = target_date - datetime.now()
    if time_until.total_seconds() > 0:
        st.header(label)
        c1, c2, c3 = st.columns(3)
        c1.metric("Tage", time_until.days)
        c2.metric("Stunden", time_until.seconds // 3600)
        c3.metric("Minuten", (time_until.seconds % 3600) // 60)


show_countdown("Poprad-Countdown", datetime(2026, 10, 2))
st.divider()
show_countdown("Würzburg-Countdown", datetime(2026, 11, 23))

# --- Walking Animation Progress Bar ---
st.markdown(
    f"""
    <div class="animation-track">
        <div class="track-ground"></div>
        <div class="track-fill"></div>
        <img class="sprite-destination" src="data:image/png;base64,{woman_encoded}">
        <img class="sprite-walker" src="data:image/png;base64,{man_encoded}">
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- Session States für Umschläge und Quiz ---
if "quiz_offen" not in st.session_state: st.session_state.quiz_offen = False
if "brief_offen" not in st.session_state: st.session_state.brief_offen = False
if "aktuelle_frage" not in st.session_state: st.session_state.aktuelle_frage = 0
if "quiz_feedback" not in st.session_state: st.session_state.quiz_feedback = None

fragen = [
    {"frage": "1. Wie viele Nachrichten haben wir insgesamt schon geschrieben? (Stand 16.9.26)",
     "antworten": ["290", "1230", "5190", "18550"], "korrekt": "5190", "statement": ""},
    {"frage": "2. Wer von uns hat davon mehr Nachrichten geschrieben?", "antworten": ["Alica", "Miles"],
     "korrekt": "Alica",
     "statement": "Naja, du hast 300 Nachrichten mehr geschrieben, eigentlich sind wir also ziemlich ausgeglichen!"},
    {"frage": "3. Welches Emoji hast du dabei am häufigen benutzt?", "antworten": ["✨", "❤️", "🥲", "👉👈"],
     "korrekt": "❤️", "statement": "Und zwar mit Abstand!"},
    {"frage": "4. In welchem Monat haben wir am meisten geschrieben?", "antworten": ["August", "Juli", "Juni", "Mai"],
     "korrekt": "Juni", "statement": "", "image": "assets/timeseries.png"},
    {"frage": "5. Wie viele Minuten haben wir schon über WhatsApp telefoniert?",
     "antworten": ["450", "1320", "69", "670"], "korrekt": "450", "statement": ""},
    {"frage": "5. Wie viele Kilometer liegen gerade zwischen uns? (Luftlinie)",
     "antworten": ["410", "190", "240", "360"], "korrekt": "240", "statement": "Also eigentlich gar nicht so viel."}
]

# --- Die beiden Umschläge nebeneinander ---
colA, colB = st.columns(2)

# Umschlag 1: Quiz
with colA:
    st.image("assets/envelope.png", width="stretch")
    st.markdown('<div id="quiz-anchor"></div>', unsafe_allow_html=True)
    quiz_btn_text = "Quiz schließen 💌" if st.session_state.quiz_offen else "Quiz öffnen 💌"
    if st.button(quiz_btn_text, key="btn_quiz", type="primary", width="stretch"):
        st.session_state.quiz_offen = not st.session_state.quiz_offen
        st.session_state.brief_offen = False  # Schließt den Brief, falls offen
        st.rerun()

# Umschlag 2: Brief
with colB:
    st.image("assets/envelope.png", width="stretch")
    st.markdown('<div id="text-anchor"></div>', unsafe_allow_html=True)
    brief_btn_text = "Brief schließen 💌" if st.session_state.brief_offen else "Feeling lonely? :/"
    if st.button(brief_btn_text, key="btn_text", type="primary", width="stretch"):
        st.session_state.brief_offen = not st.session_state.brief_offen
        st.session_state.quiz_offen = False  # Schließt das Quiz, falls offen
        st.rerun()

# --- Inhalt Brief ---
if st.session_state.brief_offen:
    st.markdown("### Movieeeeenight!!!!!!!!")
    st.write("""
    Eigentlich wollte ich hier einen Gutschein-Code hinterlegen, mit dem wir Online einen Film kaufen und mit Discord zusammen schauen können!
    Ich dachte aber es macht mehr Sinn dann einfach spontan zu schauen, auf welchen Plattform wir den Film schauen wollen :)
    Es könnte ganz süß sein, vorallem wenn wir beide abends mal etwas müde vom hustlen sind fände ich es ganz cute, mit dir einen Film zu schauen. 
    Lade dir gerne schonmal Discord herunter: https://discord.com/download!
    
    Bis dann, ich freu mich!!
    """)

# --- Inhalt Quiz ---
if st.session_state.quiz_offen:
    st.markdown("### Zeit für ein kleines Quiz! 🧐")

    if st.session_state.aktuelle_frage < len(fragen):
        frage_daten = fragen[st.session_state.aktuelle_frage]
        st.write(f"**{frage_daten['frage']}**")

        if st.session_state.quiz_feedback is None:
            cA, cB = st.columns(2)
            for i, antwort in enumerate(frage_daten["antworten"]):
                spalte = cA if i % 2 == 0 else cB
                if spalte.button(antwort, width="stretch", key=f"ans_{st.session_state.aktuelle_frage}_{i}"):
                    if antwort == frage_daten["korrekt"]:
                        st.session_state.quiz_feedback = "Richtig! 🥰"
                    else:
                        st.session_state.quiz_feedback = f"Leider falsch! Richtig wäre **{frage_daten['korrekt']}** gewesen. 🤭"
                    st.rerun()
        else:
            if "Richtig" in st.session_state.quiz_feedback:
                st.success(st.session_state.quiz_feedback)
            else:
                st.error(st.session_state.quiz_feedback)

            if frage_daten.get('statement'):
                st.markdown(
                    f"<p style='text-align: center; font-style: italic; color: darkblue;'>{frage_daten['statement']}</p>",
                    unsafe_allow_html=True)

            if frage_daten.get("image") and os.path.exists(frage_daten["image"]):
                img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
                with img_col2: st.image(frage_daten["image"], width="stretch")

            if st.button("Nächste Frage ➔", width="stretch", type="primary"):
                st.session_state.aktuelle_frage += 1
                st.session_state.quiz_feedback = None
                st.rerun()
    else:
        st.success("Du hast alle Fragen geschafft!!")
        st.balloons()
        if st.button("Quiz neu starten 🔄", width="stretch", type="primary"):
            st.session_state.aktuelle_frage = 0
            st.session_state.quiz_feedback = None
            st.rerun()