import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(page_title="Resume Screening AI", layout="wide", page_icon="📄")

# --- LOAD HUGGING FACE MODEL ---
@st.cache_resource
def load_model():
    # Using a lightweight, high-performance semantic similarity model
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# --- UTILS ---
def extract_text_from_pdf(file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def calculate_match_score(resume_text, jd_text):
    """Calculates semantic similarity between resume and job description."""
    # Encode texts into embeddings
    embeddings = model.encode([resume_text, jd_text])
    # Compute Cosine Similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    # Explicitly cast to standard Python float to avoid Streamlit type errors
    return float(round(similarity * 100, 2))

# --- UI LAYOUT ---
st.title("📄 Resume Screening AI")
st.markdown("#### Semantic Matcher powered by Hugging Face Transformers")
st.info("Upload resumes and a job description to find the best candidates based on semantic meaning, not just keywords.")

# Input Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes (PDF)", 
        type="pdf", 
        accept_multiple_files=True,
        help="You can select multiple files at once."
    )

with col2:
    st.subheader("2. Job Description")
    jd_text = st.text_area(
        "Paste the Job Requirements", 
        height=300, 
        placeholder="e.g. We are looking for a Senior React Developer with 5 years of experience..."
    )

# Action Button
if st.button("🚀 Run AI Screening", use_container_width=True):
    if not uploaded_files:
        st.error("Please upload at least one resume.")
    elif not jd_text.strip():
        st.error("Please provide a job description.")
    else:
        st.divider()
        st.subheader("📊 Ranking Results")
        
        results = []
        
        # Progress bar for processing
        progress_bar = st.progress(0.0)
        for i, file in enumerate(uploaded_files):
            # Extract and Score
            resume_text = extract_text_from_pdf(file)
            if resume_text.startswith("Error"):
                st.warning(f"Skipping {file.name}: {resume_text}")
                continue
                
            score = calculate_match_score(resume_text, jd_text)
            results.append({"name": file.name, "score": score})
            
            # Update progress (cast to float)
            progress_bar.progress(float((i + 1) / len(uploaded_files)))
            
        # Sort results by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Display Results
        for idx, res in enumerate(results):
            score = res['score']
            
            # Determine color based on score
            if score >= 80:
                color = "green"
                label = "Strong Match"
            elif score >= 50:
                color = "orange"
                label = "Potential Match"
            else:
                color = "red"
                label = "Low Match"
                
            with st.expander(f"#{idx+1} | {res['name']} — {score}% Match", expanded=(idx == 0)):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Status:** :{color}[{label}]")
                    # FIX: Explicitly cast to float and ensure it's between 0.0 and 1.0
                    progress_val = float(score / 100)
                    st.progress(min(max(progress_val, 0.0), 1.0))
                with c2:
                    st.metric("Score", f"{score}%")
                
                st.caption("Semantic analysis complete. This candidate shows high relevance to the core concepts in your job description.")

# Sidebar Info
st.sidebar.title("About")
st.sidebar.write("""
This tool uses the **all-MiniLM-L6-v2** model from Hugging Face. 
Unlike keyword search, it understands the **context** of skills and experience.
""")
st.sidebar.markdown("---")
st.sidebar.write("Built with Streamlit & Hugging Face")