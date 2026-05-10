import streamlit as st
import pandas as pd
import PyPDF2
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import keys
    GEMINI_API_KEY = keys.GEMINI_KEY
    YOUTUBE_API_KEY = keys.YOUTUBE_KEY
except ImportError:
    # Agar keys.py nahi milti (jaise Streamlit Cloud par), toh Secrets se uthayein
    GEMINI_API_KEY = st.secrets["GEMINI_KEY"]
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_KEY"]


# --- 1. UNIVERSAL KNOWLEDGE BASE ---
st.set_page_config(page_title="Universal AI Career Mentor", layout="wide")

# Expanded Resources for ALL Fields
RESOURCES = {
    # Data Science & AI
    "python": "Course: [Python for All](https://www.coursera.org/specializations/python)",
    "machine learning": "Resource: [Andrew Ng's ML](https://www.coursera.org/specializations/machine-learning-introduction)",
    # Development
    "web development": "Resource: [FreeCodeCamp Full Stack](https://www.freecodecamp.org/)",
    "app development": "Resource: [Google Android Basics](https://developer.android.com/courses)",
    # Medical (MBBS)
    "anatomy": "Resource: [TeachMeAnatomy](https://teachmeanatomy.info/)",
    "mbbs": "Resource: [Marrow or Prepladder for NEET PG Prep](https://www.marrow.com/)",
    # Law
    "indian constitution": "Resource: [Constitution of India (Official)](https://www.india.gov.in/my-government/constitution-india)",
    "clat": "Resource: [LegalEdge Prep](https://www.toprankers.com/clat-online-coaching)",
    # Government Exams (UPSC, NDA, CDS, Railway)
    "upsc": "Roadmap: [NCERT Basics + Laxmikanth (Polity)](https://www.upsc.gov.in/)",
    "nda": "Resource: [Pathfinder for NDA/NA](https://www.upsc.gov.in/)",
    "railway": "Resource: [RRB Official Exam Portal](https://www.rrbcdg.gov.in/)",
    "general studies": "Resource: [Lucent's General Knowledge Guide]",
    # Technical & Non-Tech
    "soft skills": "Resource: [LinkedIn Learning - Communication](https://www.linkedin.com/learning/)"
}

# --- 2. CORE ENGINE ---
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

# --- 3. UI LAYOUT ---
st.title("🌐 Universal AI Career Mentor")
st.subheader("For Students of Medical, Law, Engineering, & Govt Exams")
st.markdown("---")

# User Input Section
col1, col2 = st.columns([1, 1])
with col1:
    st.info("Aap apna Resume ya Exam Syllabus yahan upload kar sakte hain.")
    jd_text = st.text_area("Paste Job Description or Exam Syllabus:", height=200, placeholder="E.g. UPSC Syllabus or Software Job Description")
    uploaded_file = st.file_uploader("Upload PDF (Resume/Syllabus)", type="pdf")

if st.button("🔍 Analyze My Profile"):
    if uploaded_file and jd_text:
        text = extract_text_from_pdf(uploaded_file)
        score = get_match_score([text, jd_text])
        
        with col2:
            st.metric("Compatibility Score", f"{score}%")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#3498db"}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
        # Skill-Gap Analysis
        st.subheader("📑 Analysis Report")
        missing = [s for s in RESOURCES.keys() if s in jd_text.lower() and s not in text.lower()]
        if missing:
            st.warning("Aapke profile mein ye cheezein missing hain:")
            for s in missing:
                st.write(f"🔹 **{s.upper()}**: {RESOURCES[s]}")
        else:
            st.success("Aapki taiyari sahi disha mein hai!")

# --- 4. UNIVERSAL CHATBOT ---
st.markdown("---")
st.subheader("💬 Ask Your Mentor (Any Field)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'UPSC ki taiyari kaise shuru karein?' or 'MBBS ke baad kya karein?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- ADVANCED LOGIC FOR MULTI-DOMAIN ---
    p = prompt.lower()
    response = ""
    
    if "upsc" in p or "ias" in p:
        response = "UPSC ke liye: 1. NCERT (6th-12th) se base banayein. 2. Current Affairs (The Hindu) padhein. 3. Optional subject choose karein."
    elif "mbbs" in p or "medical" in p:
        response = "MBBS ke baad aap NEET PG ki taiyari kar sakte hain ya USMLE/PLAB ke liye ja sakte hain. Clinical practice par dhyan dein."
    elif "law" in p or "clat" in p:
        response = "Law mein career ke liye CLAT exam top priority hai. Constitutional Law aur Logical Reasoning strong rakhein."
    elif "railway" in p or "rrb" in p:
        response = "Railway (RRB) exams ke liye General Math, Reasoning aur General Awareness (Lucent) kaafi important hai."
    elif "data science" in p or "ai" in p:
        response = "AI/DS ke liye Python, Statistics aur Machine Learning seekhein. Kaggle par projects banayein."
    else:
        response = "Main har field (Medical, Law, Govt Exams, Tech) mein help kar sakta hoon. Aap apna specific target bataiye!"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})