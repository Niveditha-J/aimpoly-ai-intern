# AI CODE REVIEWER PRO -
=============================

AI Code Reviewer Pro is a professional-grade, local-first code analysis dashboard. 
It combines static heuristics, vector embeddings, and Large Language Models (LLMs) 
to provide deep insights into code quality, security, and performance without 
sending your data to the cloud.

--------------------------------------------------------------------------------
## 1. SETUP STEPS
--------------------------------------------------------------------------------

Prerequisites:
- Python 3.9 or higher installed on your system.

Installation:
1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
   pip install streamlit transformers sentence-transformers torch

Running the Application:
1. In your terminal, run the following command:
   streamlit run app.py
2. The application will open in your default web browser at http://localhost:8501.

--------------------------------------------------------------------------------
## 2. TOOLS & TECHNOLOGIES USED
--------------------------------------------------------------------------------

- Frontend: Streamlit (High-performance web framework for Python)
- Generative AI: HuggingFace Transformers (google/flan-t5-base)
- Vector Engine: Sentence-Transformers (all-MiniLM-L6-v2)
- Deep Learning: PyTorch (Backend engine for model inference)
- Styling: Custom CSS (Tailwind-inspired dark mode dashboard)
- Analysis: Regex & Static Heuristics (For complexity and safety checks)

--------------------------------------------------------------------------------
## 3. HOW THE SYSTEM WORKS
--------------------------------------------------------------------------------

The AI Code Reviewer Pro uses a Hybrid Analysis Pipeline to evaluate code across 
three distinct layers:

Layer 1: Static Heuristics (The "Speed" Layer)
- Instantly scans the source code using Regular Expressions.
- Calculates Complexity Index (branching logic like if, for, while).
- Identifies Safety Guards (risky patterns like unprotected division).
- Generates a base Quality Score.

Layer 2: Vector Similarity (The "Pattern" Layer)
- Uses Sentence-Transformers to convert code into a high-dimensional vector.
- Compares your code against a "Golden Set" of high-quality code templates.
- Calculates Cosine Similarity to determine alignment with industry standards.

Layer 3: LLM Reasoning (The "Intelligence" Layer)
- Uses the flan-t5-base model for deep semantic review.
- Identifies logical bugs, style violations, and performance bottlenecks.
- Generates suggested refactored code blocks.

--------------------------------------------------------------------------------
## 4. KEY FEATURES
--------------------------------------------------------------------------------

- Real-time Dashboard: Visual metrics for Quality and ML Pattern Matching.
- ML Pattern Insight: Dynamic explanations of vector analysis results.
- Actionable AI Suggestions: Categorized into Critical, Improvement, and Best Practice.
- Color-Coded Cards: Visually distinct feedback blocks with descriptive icons.
- Visual Bug Highlighting: Red-line highlighting for problematic code segments.
- One-Click Copy: Integrated button to copy refactored code to your clipboard.
- Privacy First: All models run locally; no code is sent to external APIs.
- Multi-Language Support: Optimized for Python, JavaScript, Java, C++, and TypeScript.
