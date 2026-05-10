import streamlit as st
import pandas as pd
import PyPDF2
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. SETTINGS & RESOURCES ---
st.set_page_config(page_title="AI Career Mentor", layout="wide")

RESOURCES = {
    "python": "Course: [Python for Everybody (Coursera)](https://www.coursera.org/specializations/python)",
    "sql": "Resource: [SQLZoo - Practice SQL](https://sqlzoo.net/)",
    "machine learning": "Course: [Andrew Ng's ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction)",
    "tableau": "Resource: [Tableau Free Training](https://www.tableau.com/learn/training/20211)",
    "power bi": "Resource: [Microsoft Power BI Learning Path](https://learn.microsoft.com/en-us/training/powerplatform/power-bi)",
    "nlp": "Resource: [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course/)",
    "aws": "Resource: [AWS Cloud Practitioner Essentials](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/)"
}

# --- 2. FUNCTIONS ---
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

# --- 3. UI - ANALYZER SECTION ---
st.title("🎯 Smart-Path AI: Resume Analyzer & Chatbot")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Analysis Input")
    jd_text = st.text_area("Paste Job Description:", height=200)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if st.button("🚀 Analyze Profile"):
    if uploaded_file and jd_text:
        resume_text = extract_text_from_pdf(uploaded_file)
        score = get_match_score([resume_text, jd_text])
        
        with col2:
            st.subheader("📊 Match Score")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#2ecc71"}}
            ))
            st.plotly_chart(fig, use_container_width=True)

        # Roadmap Section
        st.subheader("💡 Missing Skills & Roadmap")
        missing = [s for s in RESOURCES.keys() if s in jd_text.lower() and s not in resume_text.lower()]
        if missing:
            for s in missing:
                st.write(f"✅ **{s.upper()}**: {RESOURCES[s]}")
        else:
            st.success("No major skill gaps found!")
    else:
        st.error("Please upload both files.")

# --- 4. UI - CHATBOT SECTION ---
st.markdown("---")
st.subheader("🤖 AI Career Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about skills or roadmap..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Simple Bot Logic
    p = prompt.lower()
    if "skill" in p:
        res = "Focus on Python, SQL, and Machine Learning for Data Science roles."
    elif "roadmap" in p:
        res = "Start with Python, move to SQL, then learn Statistics and EDA."
    else:
        res = "I can help you with career guidance. Ask me about skills or roadmaps!"

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})