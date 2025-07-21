import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import pyttsx3
import os
import time

# 1. Start
SAMPLE_RATE = 44100
CHANNELS = 1
QUESTIONS_FILE = "generated_questions.txt"
RESPONSES_DIR = "responses"
os.makedirs(RESPONSES_DIR, exist_ok=True)

with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]


# 2. Set up session state for question counter and recording status
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "recording" not in st.session_state:
    st.session_state.recording = False
if "question_played" not in st.session_state:
    st.session_state.question_played = False
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "recording_start_time" not in st.session_state:
    st.session_state.recording_start_time = 0


def play_question_audio(question_text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")
    for voice in voices:
        if "english" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.say(question_text)
    engine.runAndWait()

# 4. Function to start recording when button is pressed
def start_recording():
    st.session_state.audio_data = sd.rec(int(3600 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    st.session_state.recording_start_time = time.time()
    st.session_state.recording = True

# 7. Function to stop recording, save file, and move to next question
def stop_recording():
    sd.stop()
    st.session_state.recording = False
    duration = time.time() - st.session_state.recording_start_time
    frames = int(duration * SAMPLE_RATE)
    
    if st.session_state.audio_data is not None and frames > 0:
        audio_clip = st.session_state.audio_data[:frames]
        response_filename = os.path.join(RESPONSES_DIR, f"response_{st.session_state.current_question + 1}.wav")
        with wave.open(response_filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_clip.tobytes())
        # st.success(f"Recording saved as")
    else:
        st.warning("No audio recorded. Please try again.")
    
    st.session_state.current_question += 1
    st.session_state.question_played = False
    st.rerun()

# 3. Display current question and play audio automatically
st.title("Automated AI Interview System")

if st.session_state.current_question < len(questions):
    question_text = questions[st.session_state.current_question]
    st.write(f"### Question {st.session_state.current_question + 1}: {question_text}")

    if not st.session_state.question_played:
        play_question_audio(question_text)
        st.session_state.question_played = True

    # 4 & 5. Recording controls: Show Start Recording button when not recording, and Stop Recording button when recording
    if not st.session_state.recording:
        if st.button("🎙️ Start Recording"):
            start_recording()
    else:
        if st.button("⏹️ Stop Recording"):
            stop_recording()
else:
    # 8. When all questions are done, display Thank You message
    st.success("Interview Completed! 🎉")
    st.write("Thank you for participating!")

    st.stop()
    os._exit(0)
