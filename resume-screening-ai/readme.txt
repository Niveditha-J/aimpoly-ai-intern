
📄 Resume Screening AI
Semantic Resume Matcher powered by Hugging Face Transformers


The Resume Screening AI is a high-performance recruitment tool designed to automate the initial candidate screening process.

Unlike traditional keyword-based filters, this system uses Natural Language Processing (NLP) to understand the semantic meaning of resumes and job descriptions, ensuring that qualified candidates are not overlooked due to terminology differences.


==================================================
🛠 Tools & Technologies Used
==================================================

Category           : Technology                  : Description
--------------------------------------------------------------
Language           : Python 3.x                  : Core programming language for logic and AI
Web Framework      : Streamlit                   : Interactive web interface
AI Model           : Hugging Face                : all-MiniLM-L6-v2 (Sentence-BERT) for embeddings
PDF Parsing        : PyPDF2                      : Extracts text from PDF resumes
Mathematics        : Scikit-Learn                : Cosine similarity calculation
Data Handling      : NumPy                       : Numerical operations and arrays


==================================================
🚀 Setup & Installation
==================================================

1. Clone the Repository

git clone https://github.com/your-username/resume-screening-ai.git
cd resume-screening-ai


2. Create a Virtual Environment (Recommended)

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Command:
python -m venv venv


3. Install Dependencies

pip install streamlit pypdf2 sentence-transformers scikit-learn numpy


4. Run the Application

streamlit run app.py


==================================================
🧠 How the System Works
==================================================

1. Text Extraction
The system extracts text from uploaded PDF resumes using PyPDF2 and prepares it for processing.

2. Semantic Embedding (AI Model)
The Hugging Face all-MiniLM-L6-v2 model converts both the resume and job description into 384-dimensional vectors.

Why?
In this vector space, similar meanings (e.g., "Developer" and "Engineer") are placed closer together mathematically.

3. Cosine Similarity Calculation
The similarity between resume and job description vectors is computed using cosine similarity.

This produces a score between 0% and 100%, indicating how well the resume matches the job description.

4. Dynamic Ranking
Resumes are ranked automatically and categorized as:

Strong Match      : 80% and above
Potential Match   : 50% to 79%
Low Match         : Below 50%


==================================================
🌟 Key Features
==================================================

• Batch Processing:
  Upload multiple resumes and get ranked results instantly.

• Context Awareness:
  Understands semantic differences like "Java" vs "JavaScript".

• Interactive UI:
  Real-time progress bars and expandable result sections.

• Lightweight:
  Optimized transformer model that runs efficiently on CPU.


==================================================
📂 Project Structure
==================================================

resume-screening-ai/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies
├── README.txt          # Project documentation
└── resumes/            # Optional sample resumes


==================================================
🤝 Contributing
==================================================

Contributions are welcome.

Feel free to:
• Improve the matching algorithm
• Add features like skill extraction
• Optimize performance

Submit a pull request or open an issue.


==================================================
Developed with ❤️ using Python and Hugging Face
==================================================
