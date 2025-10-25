import streamlit as st
import time
import random

# ------------------ Configuration ------------------
st.set_page_config(page_title="Typing Speed Test", page_icon="⌨️", layout="centered")

# Custom CSS for both dark & light themes
st.markdown("""
    <style>
    :root {
        --bg-color: #0f172a; /* Dark mode */
        --text-color: #f8fafc;
        --card-bg: #1e293b;
    }
    [data-theme="light"] {
        --bg-color: #f8fafc; /* Light mode */
        --text-color: #1e293b;
        --card-bg: #ffffff;
    }
    body {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Poppins', sans-serif;
    }
    .passage-box {
        background: var(--card-bg);
        color: var(--text-color);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .stTextArea textarea {
        font-size: 16px !important;
        line-height: 1.6;
        border-radius: 10px !important;
    }
    .result-box {
        background: rgba(59,130,246,0.1);
        border-left: 5px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Passages ------------------
passages = {
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

# ------------------ Title ------------------
st.title("⌨️ Professional Typing Speed Test")
st.write("Enhance your typing speed and accuracy with real-time evaluation. Select your level and begin!")

# ------------------ Difficulty Selection ------------------
level = st.radio("🎚️ Choose Difficulty Level:", ["Easy", "Medium", "Hard"], horizontal=True)

# ------------------ Start Test ------------------
if st.button("🚀 Start Test"):
    st.session_state['text'] = random.choice(passages[level])
    st.session_state['start_time'] = None
    st.session_state['typed'] = ""
    st.session_state['test_started'] = True

# ------------------ Show Passage ------------------
if st.session_state.get('test_started', False):
    passage = st.session_state.get('text', "")
    if passage:
        st.markdown(f"<div class='passage-box'><b>Type the passage below:</b><br><br>{passage}</div>", unsafe_allow_html=True)

        typed_text = st.text_area("💬 Start Typing Here:", st.session_state.get('typed', ""), height=150)

        if typed_text and st.session_state.get('start_time') is None:
            st.session_state['start_time'] = time.time()

        if st.button("✅ Submit"):
            if not typed_text.strip():
                st.warning("⚠️ Please type the passage before submitting.")
            else:
                end_time = time.time()
                time_taken = round(end_time - st.session_state['start_time'], 2)

                words = passage.split()
                typed_words = typed_text.strip().split()
                correct = sum(1 for i in range(min(len(words), len(typed_words))) if words[i] == typed_words[i])
                accuracy = round((correct / len(words)) * 100, 2)
                wpm = round((len(typed_words) / time_taken) * 60, 2)

                st.markdown("""
                    <div class='result-box'>
                        <h4>📊 Test Results</h4>
                    </div>
                """, unsafe_allow_html=True)

                st.metric(label="⏱ Time Taken", value=f"{time_taken} sec")
                st.metric(label="✅ Correct Words", value=f"{correct}/{len(words)}")
                st.metric(label="🎯 Accuracy", value=f"{accuracy}%")
                st.metric(label="⌨️ Typing Speed", value=f"{wpm} WPM")

                if st.button("🔁 Restart Test"):
                    st.session_state.clear()
                    st.experimental_rerun()

