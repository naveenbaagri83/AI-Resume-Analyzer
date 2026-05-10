import streamlit as st
import pandas as pd
import PyPDF2
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. SETTINGS & RESOURCES ---
st.set_page_config(page_title="AI Career Path Analyzer", layout="wide")

# Yeh list aap apne hisaab se badha sakte hain
RESOURCES = {
    "python": "Course: [Python for Everybody (Coursera)](https://www.coursera.org/specializations/python)",
    "sql": "Resource: [SQLZoo - Practice SQL](https://sqlzoo.net/)",
    "machine learning": "Course: [Andrew Ng's ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction)",
    "tableau": "Resource: [Tableau Free Training](https://www.tableau.com/learn/training/20211)",
    "power bi": "Resource: [Microsoft Power BI Learning Path](https://learn.microsoft.com/en-us/training/powerplatform/power-bi)",
    "nlp": "Resource: [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course/)",
    "aws": "Resource: [AWS Cloud Practitioner Essentials](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/)",
    "excel": "Resource: [Excel for Data Analysis (Microsoft)](https://learn.microsoft.com/en-us/training/paths/modern-analytics/)"
}

# --- 2. HELPER FUNCTIONS ---
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

def get_match_score(text_list):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# --- 3. UI DESIGN ---
st.title("🎯 Smart-Path AI: Resume Analyzer & Career Coach")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Input Section")
    jd_text = st.text_area("Paste the Job Description (JD) here:", height=250, placeholder="E.g. We are looking for a Data Analyst with SQL and Python skills...")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

if st.button("🚀 Analyze & Generate Roadmap"):
    if uploaded_file and jd_text:
        resume_text = extract_text_from_pdf(uploaded_file)
        score = get_match_score([resume_text, jd_text])
        
        with col2:
            st.subheader("📊 Matching Analysis")
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2ecc71"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ff4b4b"},
                        {'range': [50, 80], 'color': "#ffa500"},
                        {'range': [70, 100], 'color': "#2ecc71"}],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        # --- NEW: ROADMAP SECTION ---
        st.markdown("---")
        st.subheader("💡 Personalized Growth Roadmap")
        
        # Skill Gap Logic
        missing_skills = []
        for skill in RESOURCES.keys():
            # Agar skill JD mein hai par Resume mein nahi, toh wo missing hai
            if skill in jd_text.lower() and skill not in resume_text.lower():
                missing_skills.append(skill)
        
        if missing_skills:
            st.warning(f"Humne {len(missing_skills)} missing skills pehchani hain jo is job ke liye zaroori hain:")
            
            # Skills ko sundar cards mein dikhana
            res_col1, res_col2 = st.columns(2)
            for i, skill in enumerate(missing_skills):
                with (res_col1 if i % 2 == 0 else res_col2):
                    with st.expander(f"📚 Learn {skill.upper()}"):
                        st.write(f"Aapko is skill par kaam karne ki zaroorat hai.")
                        st.markdown(f"**Recommended Resource:** {RESOURCES[skill]}")
        else:
            st.success("🎉 Excellent! Your resume is well-aligned with the core skills mentioned in this Job Description.")
            
    else:
        st.error("Please provide both the Job Description and your Resume to start the analysis.")