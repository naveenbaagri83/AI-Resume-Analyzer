🎯 Smart-Path AI: Career Skill-Gap Analyzer
🚀 Overview
This is an End-to-End Data Science project designed to bridge the gap between job seekers and their dream roles. The tool utilizes Natural Language Processing (NLP) to analyze and compare a user's Resume (PDF) against a specific Job Description (JD). It provides an interactive matching score and identifies missing skills to help candidates optimize their profiles.

✨ Key Features
Automated PDF Parsing: Extracts unstructured text from resumes using PyPDF2.

NLP-Driven Matching: Leverages Cosine Similarity and CountVectorization from Scikit-learn to calculate accurate compatibility scores.

Interactive Dashboard: A sleek and user-friendly web interface built with Streamlit.

Visual Analytics: Real-time data visualization using Plotly Gauge Charts for immediate feedback.

Skill Gap Identification: Highlights missing keywords and technical skills required for the target role.

🛠️ Tech Stack
Language: Python 3.10+

Libraries: Streamlit, Scikit-learn, Plotly, Pandas, PyPDF2

Domain: Natural Language Processing (NLP), Machine Learning

📖 How to Run
Clone the repository.

Install dependencies: pip install -r requirements.txt

Run the app: streamlit run first.py
