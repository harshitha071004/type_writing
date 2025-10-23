import streamlit as st
import time
import random

# ---------------- Passages ----------------
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

# ---------------- App Layout ----------------
st.set_page_config(page_title="Typing Speed Test", page_icon="⌨️", layout="centered")
st.title("⌨️ Typing Speed Test")
st.write("Test your typing speed and accuracy at different difficulty levels!")

# ---------------- Difficulty Selection ----------------
level = st.radio("Select Difficulty:", ["Easy", "Medium", "Hard"])

# Start button
if st.button("Start Test"):
    st.session_state['text'] = random.choice(passages[level])
    st.session_state['start_time'] = None
    st.session_state['typed'] = ""

# Show passage if started
if 'text' in st.session_state:
    st.subheader("Type the following passage:")
    st.write(st.session_state['text'])
    
    # User input
    typed_text = st.text_area("Start typing here...", st.session_state.get('typed', ""), height=150)
    
    # Start timer when typing begins
    if typed_text and st.session_state.get('start_time') is None:
        st.session_state['start_time'] = time.time()
    
    # Submit button
    if st.button("Submit"):
        end_time = time.time()
        if not typed_text.strip():
            st.warning("Please type the passage before submitting.")
        else:
            time_taken = round(end_time - st.session_state['start_time'], 2)
            words = st.session_state['text'].split()
            typed_words = typed_text.strip().split()
            
            correct = sum(1 for i in range(min(len(words), len(typed_words))) if words[i] == typed_words[i])
            accuracy = round((correct / len(words)) * 100, 2)
            wpm = round((len(typed_words) / time_taken) * 60, 2)
            
            st.success(f"⏱ **Time Taken:** {time_taken} seconds")
            st.info(f"✅ **Correct Words:** {correct}/{len(words)}")
            st.warning(f"🎯 **Accuracy:** {accuracy}%")
            st.success(f"⌨️ **Typing Speed:** {wpm} WPM")
