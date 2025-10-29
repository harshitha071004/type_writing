import streamlit as st
import time
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Typing Speed Test", page_icon="⌨️", layout="centered")

PASSAGES = {
    "Easy": [
        "Python is a versatile programming language.",
        "Typing speed test helps improve accuracy.",
        "Practice makes perfect."
    ],
    "Medium": [
        "Data science combines statistics, programming, and domain knowledge.",
        "Learning Python can open doors to many tech careers.",
        "Consistent practice improves typing speed and precision."
    ],
    "Hard": [
        "Artificial Intelligence leverages machine learning and deep learning to solve complex problems.",
        "Optimization of algorithms requires both theoretical knowledge and practical experience.",
        "Software engineering principles help build scalable and maintainable systems."
    ]
}

# ---------------- HELPERS ----------------
def highlight_text(passage, typed):
    """Highlight correctly typed characters in green and incorrect in red."""
    result = ""
    for i, char in enumerate(passage):
        if i < len(typed):
            if typed[i] == char:
                result += f"<span style='color:#00FF00;'>{char}</span>"
            else:
                result += f"<span style='color:#FF4B4B;'>{char}</span>"
        else:
            result += f"<span style='color:#999999;'>{char}</span>"
    return result

def compute_metrics(reference, typed, start_time, end_time):
    if not start_time or not end_time:
        return 0.0, 0.0, 0.0
    time_taken = max(0.01, end_time - start_time)
    correct_chars = sum(1 for i in range(min(len(reference), len(typed))) if reference[i] == typed[i])
    accuracy = (correct_chars / len(reference)) * 100 if reference else 0
    wpm = (len(typed.split()) / time_taken) * 60
    return round(time_taken, 2), round(accuracy, 2), round(wpm, 2)

# ---------------- SESSION STATE ----------------
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "time_left" not in st.session_state:
    st.session_state.time_left = 60
if "passage" not in st.session_state:
    st.session_state.passage = ""
if "typed" not in st.session_state:
    st.session_state.typed = ""

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>⌨️ Typing Speed Test</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    level = st.radio("Choose Difficulty:", ["Easy", "Medium", "Hard"], horizontal=True)
with col2:
    duration = st.selectbox("Duration (seconds):", [30, 45, 60], index=2)

start_col, reset_col = st.columns(2)
with start_col:
    start_clicked = st.button("🚀 Start Test")
with reset_col:
    if st.button("🔁 Reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ---------------- START TEST ----------------
if start_clicked:
    st.session_state.test_started = True
    st.session_state.start_time = time.time()
    st.session_state.end_time = None
    st.session_state.typed = ""
    st.session_state.passage = random.choice(PASSAGES[level])
    st.session_state.time_left = duration
    st.rerun()

if not st.session_state.test_started:
    st.info("Click **Start Test** to begin.")
    st.stop()

# ---------------- DISPLAY PASSAGE ----------------
st.subheader("Type the passage below 👇")

# Typing area
typed = st.text_area("Start typing here...", value=st.session_state.get("typed", ""), height=150, key="typing_area")

# Highlight passage
highlighted_passage = highlight_text(st.session_state.passage, typed)
st.markdown(
    f"<div style='background-color:black; color:white; padding:15px; border-radius:10px; font-size:18px; line-height:1.6;'>{highlighted_passage}</div>",
    unsafe_allow_html=True
)

# ---------------- LIVE TIMER ----------------
timer_placeholder = st.empty()
if st.session_state.start_time and not st.session_state.end_time:
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, duration - int(elapsed))
    timer_placeholder.metric("⏱️ Time Left", f"{st.session_state.time_left}s")

    if st.session_state.time_left > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.end_time = time.time()

# ---------------- RESULTS ----------------
if st.session_state.end_time:
    time_taken, accuracy, wpm = compute_metrics(
        st.session_state.passage, typed, st.session_state.start_time, st.session_state.end_time
    )
    st.success("✅ Time’s up! Test Completed.")
    st.metric("Typing Speed (WPM)", wpm)
    st.metric("Accuracy (%)", accuracy)
    st.metric("Time Taken (s)", time_taken)

    if st.button("🔁 Try Again"):
        st.session_state.test_started = False
        st.rerun()
