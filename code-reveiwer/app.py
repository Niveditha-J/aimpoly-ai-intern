import re
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import time

# ----------------- CONFIGURATION -----------------
st.set_page_config(
    page_title="AI Code Reviewer Pro", 
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Dashboard Look
st.markdown("""
    <style>
    /* Main Background and Text */
    .main {
        background-color: #0A0A0B;
        color: #E4E4E7;
    }
    
    /* Custom Cards */
    .metric-card {
        background-color: #18181B;
        border: 1px solid #27272A;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #3F3F46;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #A1A1AA;
        font-weight: 600;
    }
    
    /* Color coding for scores */
    .score-high { color: #10B981; }
    .score-med { color: #F59E0B; }
    .score-low { color: #EF4444; }
    
    /* Suggestion Cards */
    .suggestion-content {
        padding: 15px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* ML Insight Box */
    .insight-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #18181B 100%);
        border: 1px solid #312E81;
        padding: 20px;
        border-radius: 12px;
        margin-top: 10px;
    }
    
    /* Code Editor Styling */
    .stTextArea textarea {
        background-color: #18181B !important;
        color: #D4D4D8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #27272A !important;
    }
    
    /* Highlighted Error Lines */
    .line-error {
        color: #EF4444;
        background: rgba(239, 68, 68, 0.15);
        padding: 0 4px;
        border-radius: 2px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- MODEL LOADING -----------------
@st.cache_resource
def load_models():
    try:
        # 1. Load Embedding Model (ML Similarity)
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # 2. Load GenAI Model (Reviewer)
        model_name = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        
        return embed_model, tokenizer, model, device
    except Exception as e:
        st.error(f"Failed to initialize AI models: {str(e)}")
        st.info("Ensure you have 'transformers', 'sentence-transformers', and 'torch' installed.")
        return None, None, None, None

# Initialize models
embed_model, tokenizer, model, device = load_models()

if not embed_model:
    st.stop()

# ----------------- LOGIC FUNCTIONS -----------------
def compute_static_metrics(code: str):
    lines = code.splitlines()
    total = len(lines) if len(lines) > 0 else 1
    
    # Check for risky division (division without a safety check)
    has_div = "/" in code
    risky_div = has_div and not ("if" in code or "try" in code)
    
    complexity = len(re.findall(r"\b(if|for|while|try|with|lambda|elif|else)\b", code))
    
    # Heuristic score based on complexity vs length
    base_score = 100
    if total > 0:
        complexity_ratio = complexity / total
        if complexity_ratio > 0.3: base_score -= 20
        if complexity_ratio > 0.5: base_score -= 20
        
    # Penalty for very long functions without comments
    comments = sum(1 for l in lines if l.strip().startswith(("#", "//")))
    if total > 20 and comments == 0: base_score -= 10
    if risky_div: base_score -= 30
    
    static_score = max(10, min(100, base_score))
    
    return {
        "total_lines": total,
        "complexity": complexity,
        "static_score": round(static_score, 2),
        "comment_ratio": round(comments/total, 2) if total > 0 else 0,
        "risky_div": risky_div
    }

def compute_embedding_score(code: str, language: str):
    try:
        # Reference high-quality snippets
        references = {
            "Python": ["def process(data):\n    return [x for x in data if x]", "class Handler:\n    def __init__(self): pass"],
            "JavaScript": ["const fn = (arr) => arr.filter(x => !!x);", "class Service { constructor() {} }"]
        }.get(language, ["// clean code"])
        
        code_emb = embed_model.encode(code, convert_to_tensor=True)
        ref_embs = embed_model.encode(references, convert_to_tensor=True)
        similarities = util.cos_sim(code_emb, ref_embs)[0]
        best_sim = float(similarities.max().item())
        
        # Scale 0.3-0.8 similarity to 0-100 score
        score = int(max(0, min(100, (best_sim - 0.3) * 200)))
        return score, best_sim
    except Exception as e:
        raise RuntimeError(f"ML Embedding Analysis failed: {str(e)}")

def generate_review(code: str, language: str):
    # Number the lines for the AI to identify them
    lines = code.splitlines()
    numbered_code = "\n".join([f"L{i+1}: {line}" for i, line in enumerate(lines)])

    prompt = f"""Task: Review this {language} code. 
    1. Summarize issues (bugs, style, performance).
    2. List specific line numbers with bugs (e.g., L3, L5).
    3. Provide refactored code.
    
    Format:
    SUMMARY: [Your review]
    BUGS: [Line numbers like L3, L10 or 'None']
    REFACTORED: [Code]
    
    Code:
    {numbered_code}"""
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_length=512, 
                do_sample=True, 
                temperature=0.3, 
                repetition_penalty=2.5,
                top_p=0.9,
                no_repeat_ngram_size=3
            )
        
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parsing
        summary = "Analysis complete."
        refactored = ""
        error_lines = []
        
        if "SUMMARY:" in full_text:
            parts = full_text.split("BUGS:")
            summary = parts[0].replace("SUMMARY:", "").strip()
            if len(parts) > 1:
                sub_parts = parts[1].split("REFACTORED:")
                bug_str = sub_parts[0].strip()
                # Extract numbers from bug_str (e.g. L3 -> 3)
                error_lines = [int(n) for n in re.findall(r'L(\d+)', bug_str)]
                if len(sub_parts) > 1:
                    refactored = sub_parts[1].strip()

        # Fallback for risky division if AI misses it
        if "/" in code and "if" not in code and "try" not in code:
            if not error_lines:
                error_lines = [i+1 for i, l in enumerate(lines) if "/" in l]
                summary = "Potential ZeroDivisionError detected. Ensure you check if the denominator is zero before dividing."

        if len(summary) < 10:
            summary = "The code structure is standard. Ensure you handle edge cases and add documentation."

        # Categorization
        lower_summary = summary.lower()
        is_critical = error_lines or any(w in lower_summary for w in ["error", "bug", "fail", "wrong", "issue", "crash"])
        
        s_type = "critical" if is_critical else "improvement" if any(w in lower_summary for w in ["should", "better", "improve", "optimize", "slow"]) else "best-practice"
        icon = "🚨" if s_type == "critical" else "⚡" if s_type == "improvement" else "💡"
        title = "Critical Issue" if s_type == "critical" else "Optimization" if s_type == "improvement" else "Best Practice"

        return {
            "score": 45 if is_critical else 85,
            "summary": summary,
            "error_lines": error_lines,
            "suggestions": [{
                "type": s_type,
                "icon": icon,
                "title": title,
                "description": summary,
                "code": refactored if refactored else None
            }]
        }
    except Exception as e:
        raise RuntimeError(f"AI Generation Error: {str(e)}")

# ----------------- UI LAYOUT -----------------
st.title("🧾 AI Code Reviewer Pro")
st.caption(f"Hybrid ML Engine | Running on {device.upper()} | Model: flan-t5-base")

# Sidebar
st.sidebar.header("⚙️ Configuration")
language = st.sidebar.selectbox("Target Language", ["Python", "JavaScript", "Java", "C++", "TypeScript"])
st.sidebar.divider()
st.sidebar.info("This tool uses a local LLM and Vector Embeddings to analyze your code without sending it to the cloud.")

# Main Input
code_input = st.text_area("Source Code", height=350, placeholder="Paste your code here for a deep review...")

# State for retries
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = None

def run_analysis():
    if not code_input.strip():
        st.warning("Please provide some code to analyze.")
        return

    st.session_state.error_msg = None # Clear previous error
    
    try:
        with st.spinner("Analyzing patterns and generating insights..."):
            # 1. Run Analysis
            static = compute_static_metrics(code_input)
            ml_score, raw_sim = compute_embedding_score(code_input, language)
            ai_review = generate_review(code_input, language)
            
            # 2. Display Top Metrics
            col1, col2 = st.columns(2)
            
            # Quality Score Card
            q_score = int(static['static_score'])
            if ai_review['error_lines']: q_score = min(q_score, 45)
            
            q_class = "score-high" if q_score > 80 else "score-med" if q_score > 50 else "score-low"
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Quality Score</div>
                        <div class="metric-value {q_class}">{q_score}%</div>
                        <div style="color: #71717A; font-size: 0.8rem;">Heuristics + AI Validation</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # ML Insight Card
            m_class = "score-high" if ml_score > 70 else "score-med" if ml_score > 40 else "score-low"
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">ML Pattern Match</div>
                        <div class="metric-value {m_class}">{ml_score}%</div>
                        <div style="color: #71717A; font-size: 0.8rem;">Vector Similarity Analysis</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # 3. ML Insights Section
            st.markdown(f"""
                <div class="insight-box">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 1.2rem;">🧠</span>
                        <h4 style="margin: 0; color: #818CF8;">ML Pattern Insight</h4>
                    </div>
                    <p style="color: #94A3B8; font-size: 0.9rem; margin: 0;">
                        The vector analysis shows a <b>{int(raw_sim*100)}%</b> raw similarity to high-quality code templates. 
                        {'Your code structure aligns well with industry standards.' if raw_sim > 0.6 else 'The code has a unique structure that might benefit from more standard design patterns.'}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # 4. AI Suggestions & Error Lines
            st.subheader("📝 AI Suggestions")
            
            if ai_review['error_lines']:
                st.error(f"🚨 **Bugs Detected on Lines:** {', '.join(['L'+str(n) for n in ai_review['error_lines']])}")
                # Show code with highlighted lines
                lines = code_input.splitlines()
                highlighted_code = ""
                for i, line in enumerate(lines):
                    line_num = i + 1
                    if line_num in ai_review['error_lines']:
                        highlighted_code += f"<span class='line-error'>{line_num}: {line}</span>"
                    else:
                        highlighted_code += f"<span style='color: #71717A;'>{line_num}:</span> {line}\n"
                
                st.markdown(f"<pre style='background-color: #18181B; padding: 15px; border-radius: 10px; border: 1px solid #27272A; font-family: monospace; white-space: pre-wrap;'>{highlighted_code}</pre>", unsafe_allow_html=True)

            for i, s in enumerate(ai_review["suggestions"]):
                with st.expander(f"{s['icon']} {s['title']} ({s['type'].title()})", expanded=True):
                    st.markdown(f"""
                        <div class="suggestion-content">
                            <p style="color: #D1D5DB; margin-bottom: 15px;">{s["description"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if s["code"]:
                        st.markdown("**Suggested Refactoring:**")
                        st.code(s["code"], language=language.lower())
            
            # 5. Technical Breakdown
            with st.expander("📊 Technical Breakdown"):
                tc1, tc2, tc3 = st.columns(3)
                tc1.metric("Lines of Code", static['total_lines'])
                tc2.metric("Complexity Index", static['complexity'])
                tc3.metric("Comment Density", f"{int(static['comment_ratio']*100)}%")
                
                st.caption(f"Analysis performed on {device.upper()} using Sentence-Transformers and FLAN-T5.")

    except Exception as e:
        st.session_state.error_msg = str(e)
        st.error("🚨 **Analysis Failed**")
        st.markdown(f"""
            **Error Details:** {st.session_state.error_msg}
            
            Possible causes:
            - **Local Resource Limit:** Local model inference might have timed out or run out of memory.
            - **Unexpected Response:** The AI engine returned an unparseable result.
        """)
        if st.button("🔄 Try Again"):
            st.rerun()

# Button to trigger analysis
if st.button("🚀 Run Deep Analysis", use_container_width=True):
    run_analysis()
elif st.session_state.error_msg:
    if st.button("🔄 Retry Analysis", use_container_width=True):
        run_analysis()
else:
    # Empty State
    st.info("Paste your code above and click 'Run Deep Analysis' to get started.")