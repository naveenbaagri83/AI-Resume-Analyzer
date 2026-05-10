import streamlit as st
import pandas as pd
import PyPDF2
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- SETTINGS ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Function: PDF se text nikalne ke liye
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

# Function: Match Score Calculate karne ke liye
def get_match_score(text_list):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# --- UI DESIGN ---
st.title("🎯 Smart-Path AI: Skill Gap Analyzer")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Input Section")
    jd_text = st.text_area("Paste Job Description (JD) here:", height=200)
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

if st.button("🚀 Analyze Now"):
    if uploaded_file and jd_text:
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Calculating Score
        score = get_match_score([resume_text, jd_text])
        
        with col2:
            st.subheader("📊 Analysis Result")
            
            # --- GAUGE CHART (Visuals) ---
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Resume Match %"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2ecc71"},
                    'steps': [
                        {'range': [0, 40], 'color': "#ff4b4b"},
                        {'range': [40, 70], 'color': "#ffa500"},
                        {'range': [70, 100], 'color': "#2ecc71"}],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

            if score > 70:
                st.success("Great! Your profile is a strong match.")
            else:
                st.warning("You might need to add more keywords to your resume.")
    else:
        st.error("Please provide both Resume and Job Description.")