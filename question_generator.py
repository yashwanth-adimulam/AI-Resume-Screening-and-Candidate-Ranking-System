import subprocess


def generate_questions_with_mistral(resume_text):
    prompt = (
        "Generate **exactly 5** technical interview questions based on the following resume.\n"
        "Only output the questions, with each question on a **new line**.\n"
        "Strictly follow this format:\n\n"
        "<Question 1>\n"
        "<Question 2>\n"
        "<Question 3>\n"
        "...\n\n"
        "Do **not** include:\n"
        "- Any introductory text\n"
        "- Any numbering or bullet points\n"
        "- Phrases like 'Here are your questions:' or 'Based on the resume:'\n"
        "- Any explanations or summaries\n\n"
        "Focus on:\n"
        "- Projects (fundamental technical questions on implementation and challenges faced).\n"
        "- Tech stack (fundamental concepts to test understanding).\n"
        "- Don't include questions related to school and college.\n\n"
        "Resume:\n"
        f"{resume_text}\n"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "resume"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        questions = result.stdout.strip()
        return questions

    except Exception as e:
        return f"Error occurred while generating questions: {str(e)}"


with open("parsed_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read().strip()

questions = generate_questions_with_mistral(resume_text)

if "Error" not in questions:
    with open("generated_questions.txt", "w", encoding="utf-8") as f:
        f.write(questions)
    print("Interview questions generated and saved successfully.")
else:
    print(questions)
