import os
import json
import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    return result["text"]

RESPONSES_DIR = "responses"
QUESTIONS_FILE = "generated_questions.txt"
OUTPUT_JSON = "qa_data.json"

with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]

wav_files = [f for f in os.listdir(RESPONSES_DIR) if f.endswith(".wav")]

def sort_key(filename):
    try:
        base = filename.replace(".wav", "")
        num = int(base.split("_")[-1])
        return num
    except Exception:
        return filename

wav_files = sorted(wav_files, key=sort_key)

qa_data = []

for wav_file in wav_files:
    wav_path = os.path.join(RESPONSES_DIR, wav_file)
    transcript = transcribe_audio(wav_path)
    
    txt_file = wav_file.replace(".wav", ".txt")
    txt_path = os.path.join(RESPONSES_DIR, txt_file)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    
    try:
        num = int(wav_file.replace(".wav", "").split("_")[-1])
        question = questions[num - 1] if num - 1 < len(questions) else ""
    except Exception:
        question = ""
    
    qa_data.append({
        "question": question,
        "answer": transcript,
        "metrics": {}
    })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(qa_data, f, indent=4)

print("Transcription complete. JSON file saved as", OUTPUT_JSON)
