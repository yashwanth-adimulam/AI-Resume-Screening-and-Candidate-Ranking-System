import pdfplumber


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


pdf_path = "1.pdf"
resume_text = extract_text_from_pdf(pdf_path)

with open("parsed_resume.txt", "w", encoding="utf-8") as f:
    f.write(resume_text)

print("Resume text extracted and saved successfully.")
