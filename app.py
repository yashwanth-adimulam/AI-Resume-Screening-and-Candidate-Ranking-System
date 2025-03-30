import streamlit as st
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() if page.extract_text() else ""
    return text


def compute_similarity(job_desc, resumes):
    texts = [job_desc] + resumes
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    return similarity_scores


st.title("📄 AI Resume Screening & Ranking System")
job_description = st.text_area("Enter the Job Description:", height=150)
uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type=["pdf"], accept_multiple_files=True)

if st.button("Process Resumes"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        resume_texts = []
        resume_names = []

        for pdf_file in uploaded_files:
            text = extract_text_from_pdf(pdf_file)
            if text.strip():
                resume_texts.append(text)
                resume_names.append(pdf_file.name)

        if resume_texts:
            scores = compute_similarity(job_description, resume_texts)
            results_df = pd.DataFrame({
                "Resume Name": resume_names,
                "Similarity Score": scores
            })
            results_df = results_df.sort_values(by="Similarity Score", ascending=False)
            st.subheader("🏆 Ranked Resumes")
            st.dataframe(results_df)
        else:
            st.error("No readable text found in the uploaded resumes.")
