import streamlit as st
import time
import random
from datetime import datetime

# --------------------
# CONFIG
# --------------------
st.set_page_config(page_title="Typing Speed Test", page_icon="⌨️", layout="centered")

# --------------------
# SAMPLE PASSAGES
# --------------------
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

# --------------------
# HELPERS
# --------------------
def compute_metrics(reference, typed, start_time, end_time):
    if not start_time or not end_time:
        return 0.0, 0.0, 0.0
    time_taken = max(0.01, end_time - start_time)
    ref_words = reference.split()
    typed_words = typed.strip().split()
    correct = sum(1 for i in range(min(len(ref_words), len(typed_words))) if ref_words[i] == typed_words[i])
    accuracy = (correct / len(ref_words)) * 100 if ref_words else 0
    wpm = (len(typed_words) / time_taken) * 60
    return round(time_taken, 2), round(accuracy, 2), round(wpm, 2)

# --------------------
# INITIALIZE SESSION
# --------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "test_started" not in st.session_state:
    st.session_state.test_started = False

# --------------------
# HEADER
# --------------------
st.markdown("<h1 style='text-align:center;'>⌨️ Typing Speed Test</h1>", unsafe_allow_html=True)
st.write("Test your typing speed and accuracy with this simple practice app.")

# --------------------
# OPTIONS
# --------------------
col1, col2 = st.columns([2, 1])
with col1:
    level = st.radio("Choose Difficulty:", ["Easy", "Medium", "Hard"], horizontal=True)
with col2:
    mode = st.selectbox("Mode:", ["60s Challenge (Countdown)", "Practice (No time limit)"])

custom_pass = st.checkbox("Use custom passage")
if custom_pass:
    user_passage = st.text_area("Enter your custom passage:", height=120)
else:
    user_passage = None

start_col, reset_col = st.columns(2)
with start_col:
    start_clicked = st.button("🚀 Start Test")
with reset_col:
    if st.button("🔁 Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --------------------
# START TEST
# --------------------
if start_clicked:
    st.session_state.test_started = True
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.typed = ""
    st.session_state.passage = user_passage.strip() if (custom_pass and user_passage) else random.choice(PASSAGES[level])
    st.session_state.time_left = 60 if mode.startswith("60s") else None
    st.rerun()

if not st.session_state.test_started:
    st.info("Click **Start Test** to begin.")
    if st.session_state.leaderboard:
        st.subheader("🏆 Leaderboard (Session Only)")
        st.table(st.session_state.leaderboard[:10])
    st.stop()

# --------------------
# TEST INTERFACE
# --------------------
st.subheader("Type the passage below:")
st.markdown(
    f"<div style='background-color:#000000; color:#FFFFFF; padding:15px; border-radius:8px; font-size:16px;'>{st.session_state.passage}</div>",
    unsafe_allow_html=True
)

typed = st.text_area("Start typing here...", value=st.session_state.get("typed", ""), height=150, key="typing_area")

# Record start time
if typed and st.session_state.get("start_time") is None:
    st.session_state.start_time = time.time()

# Show live stats
col_stats = st.columns(3)
wpm_display = col_stats[0].empty()
acc_display = col_stats[1].empty()
time_display = col_stats[2].empty()

def show_live_stats():
    now = time.time()
    if st.session_state.start_time:
        elapsed = now - st.session_state.start_time
        typed_words = typed.strip().split()
        ref_words = st.session_state.passage.split()
        correct = sum(1 for i in range(min(len(ref_words), len(typed_words))) if ref_words[i] == typed_words[i])
        accuracy = (correct / len(ref_words)) * 100 if ref_words else 0
        wpm = (len(typed_words) / max(elapsed, 0.01)) * 60
        wpm_display.metric("WPM (Live)", round(wpm, 2))
        acc_display.metric("Accuracy (Live)", f"{round(accuracy, 2)}%")
        if st.session_state.time_left:
            time_display.metric("Time Left", f"{int(st.session_state.time_left)}s")
        else:
            time_display.metric("Elapsed", f"{round(elapsed, 2)}s")

if mode.startswith("60s"):
    if "time_left" not in st.session_state:
        st.session_state.time_left = 60
    for remaining in range(int(st.session_state.time_left), -1, -1):
        st.session_state.time_left = remaining
        show_live_stats()
        if remaining == 0:
            st.session_state.end_time = st.session_state.start_time + 60 if st.session_state.start_time else time.time()
            break
        time.sleep(1)
else:
    show_live_stats()

# --------------------
# SUBMIT
# --------------------
submit = st.button("✅ Submit")
if submit or (st.session_state.get("time_left") == 0):
    if st.session_state.start_time is None:
        st.warning("You didn’t start typing!")
    else:
        st.session_state.end_time = time.time()
        time_taken, accuracy, wpm = compute_metrics(
            st.session_state.passage, typed, st.session_state.start_time, st.session_state.end_time
        )
        st.success("✅ Test Completed!")
        st.metric("Typing Speed (WPM)", wpm)
        st.metric("Accuracy (%)", accuracy)
        st.metric("Time Taken (s)", time_taken)

        # Save session result
        result = {
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Level": level,
            "WPM": wpm,
            "Accuracy": accuracy,
            "Time": time_taken
        }
        st.session_state.history.insert(0, result)
        st.session_state.leaderboard.insert(0, result)

        # Show leaderboard
        st.markdown("### 🏆 Session Leaderboard")
        st.table(st.session_state.leaderboard[:10])

        st.markdown("### 📜 Your History (this session)")
        st.table(st.session_state.history)

        if st.button("🔁 Try Again"):
            st.session_state.test_started = False
            st.rerun()
