import os
import sys
import tempfile
import streamlit as st
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Add src to sys.path for importing crew
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

try:
    from fact_checker.crew import FactChecker
except ImportError as e:
    st.error(f"Could not import FactChecker: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="VERIFACT - Professional AI Fact Verification",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Hide sidebar completely */
    .css-1d391kg {display: none;}
    
    /* Universal dark mode override - Force light theme */
    .stApp, 
    .stApp > div, 
    .main, 
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main .block-container {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Force light theme on ALL elements */
    * {
        color: inherit !important;
    }
    
    /* Override any theme variations */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* ENHANCED Logo container styling - REMOVE BOX */
    .logo-container {
        text-align: center;
        margin-bottom: 3rem;
        padding: 0;
        background: transparent;
        border: none;
        box-shadow: none;
    }
    
    .logo-container img {
        max-width: 600px !important;
        width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
        filter: none;
        transition: transform 0.3s ease;
        border: none;
        box-shadow: none;
    }
    
    .logo-container img:hover {
        transform: scale(1.02);
    }
    
    /* Enhanced header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 6s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .main-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .main-subtitle {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 0;
        font-weight: 300;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    /* Input section styling */
    .input-section {
        background: #f8f9fa !important;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
        color: #000000 !important;
    }
    
    /* Results section styling */
    .results-section {
        background: white !important;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        color: #000000 !important;
    }
    
    /* Verdict styling */
    .verdict-container {
        text-align: center;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .verdict-true {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }
    
    .verdict-false {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }
    
    .verdict-partial {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        color: #856404;
    }
    
    .verdict-inconclusive {
        background-color: #d1ecf1;
        border: 2px solid #17a2b8;
        color: #0c5460;
    }
    
    /* Enhanced feature cards with hover effects */
    .feature-card {
        background: white !important;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        color: #000000 !important;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        border-left-color: #764ba2;
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50 !important;
        margin-bottom: 0.8rem;
        position: relative;
        z-index: 1;
    }
    
    .feature-description {
        color: #555 !important;
        font-size: 1rem;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Professional section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50 !important;
        text-align: center;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Enhanced professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        height: 60px !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        color: white !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
        outline: none !important;
    }
    
    /* ENHANCED Radio button styling with GLOWING EFFECT for selected buttons */
    .stRadio > div {
        flex-direction: row !important;
        gap: 1rem !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        background-color: transparent !important;
    }
    
    .stRadio > div > label {
        background: white !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        border: 3px solid #667eea !important;
        transition: all 0.4s ease !important;
        cursor: pointer !important;
        font-weight: 700 !important;
        color: #000000 !important;
        min-width: 150px !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0.25rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
        position: relative !important;
        z-index: 100 !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #764ba2 !important;
        background: #f8f9ff !important;
        color: #000000 !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* FORCE radio button visibility in ALL themes */
    [data-theme="dark"] .stRadio > div > label,
    html[data-theme="dark"] .stRadio > div > label,
    .stRadio > div > label[data-baseweb="radio"],
    div[data-testid="stRadio"] > div > label {
        background: white !important;
        color: #000000 !important;
        border: 3px solid #667eea !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        z-index: 999 !important;
    }
    
    /* Radio button text styling */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p,
    .stRadio > div > label > div > p,
    .stRadio label p {
        color: #000000 !important;
        margin: 0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        visibility: visible !important;
    }
    
    /* ENHANCED Selected radio button state with GLOWING EFFECT */
    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        transform: scale(1.08) !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.8), 
                    0 0 60px rgba(102, 126, 234, 0.4), 
                    0 8px 25px rgba(102, 126, 234, 0.6) !important;
        animation: glow-pulse 2s ease-in-out infinite alternate !important;
    }
    
    /* Glowing animation for selected radio button */
    @keyframes glow-pulse {
        0% {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.6), 
                        0 0 40px rgba(102, 126, 234, 0.3), 
                        0 8px 25px rgba(102, 126, 234, 0.5);
        }
        100% {
            box-shadow: 0 0 35px rgba(102, 126, 234, 0.9), 
                        0 0 70px rgba(102, 126, 234, 0.5), 
                        0 12px 35px rgba(102, 126, 234, 0.7);
        }
    }
    
    .stRadio > div > label[data-checked="true"] > div[data-testid="stMarkdownContainer"] > p,
    .stRadio > div > label[data-checked="true"] > div > p,
    .stRadio > div > label:has(input:checked) p {
        color: white !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Text inputs styling */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #000000 !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: #000000 !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        resize: vertical !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background-color: white !important;
        border: 2px dashed #e9ecef !important;
        border-radius: 8px !important;
        padding: 2rem !important;
        text-align: center !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #667eea !important;
        background-color: #f8f9ff !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #20c997 0%, #28a745 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .main-subtitle {
            font-size: 1.2rem;
        }
        
        .stRadio > div {
            flex-direction: column !important;
        }
        
        .stRadio > div > label {
            min-width: 200px !important;
        }
        
        .logo-container img {
            max-width: 400px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Company logo at the top center - NO BOX
try:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("src/fact_checker/assets/ramanasoftware_logo.png", width=600)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    # Fallback if image is not found
    st.markdown("""
    <div class="logo-container">
        <h1 style="color: #667eea; font-size: 4rem; margin: 0;">RAMANA SOFTWARE</h1>
        <p style="color: #666; font-size: 1.5rem; margin: 0;">Consulting Services</p>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">VERIFACT</h1>
    <p class="main-subtitle">Professional AI-Powered Fact Verification System</p>
</div>
""", unsafe_allow_html=True)

# Environment check
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ **Configuration Error:** Please set your OPENAI_API_KEY in the .env file")
    st.stop()

# Features overview
st.markdown('<h2 class="section-header">🚀 Platform Capabilities</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🗣️ Text Claims</div>
        <div class="feature-description">Advanced AI verification of factual statements, assertions, and textual content with comprehensive source validation</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🌐 Web Content</div>
        <div class="feature-description">Real-time analysis of articles, news content, and online publications with cross-referencing capabilities</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📺 Video Content</div>
        <div class="feature-description">Intelligent fact-checking of YouTube videos, transcripts, and multimedia content claims</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📄 Documents</div>
        <div class="feature-description">Comprehensive processing and verification of PDF documents, Word files, and text-based materials</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input section
st.markdown("""
<div class="input-section">
""", unsafe_allow_html=True)

st.markdown('<h3 class="section-header">🎯 Select Verification Method</h3>', unsafe_allow_html=True)

# Input mode selection
mode = st.radio(
    "",
    ["📝 Text Claim", "🌐 Website URL", "📺 YouTube Video", "📄 Document Upload"],
    horizontal=True,
    key="input_mode"
)

st.markdown("<br>", unsafe_allow_html=True)

user_input = ""
claim, url, youtube_url, uploaded_file = "", "", "", None

# Input forms based on selected mode
if mode == "📝 Text Claim":
    st.markdown("**Enter the factual claim you want to verify:**")
    claim = st.text_area(
        "",
        height=120,
        placeholder="Enter the statement or claim you want to fact-check...",
        key="claim_input"
    )
    user_input = claim

elif mode == "🌐 Website URL":
    st.markdown("**Enter the website URL to analyze:**")
    url = st.text_input(
        "",
        placeholder="https://example.com/article",
        key="url_input"
    )
    user_input = url

elif mode == "📺 YouTube Video":
    st.markdown("**Enter the YouTube video URL:**")
    youtube_url = st.text_input(
        "",
        placeholder="https://www.youtube.com/watch?v=...",
        key="youtube_input"
    )
    if youtube_url:
        if re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)', youtube_url):
            st.success("✅ Valid YouTube URL detected")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL")
    user_input = youtube_url

elif mode == "📄 Document Upload":
    st.markdown("**Upload a document for analysis:**")
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, Word Document (.docx), Text File (.txt)"
    )
    if uploaded_file:
        st.success(f"✅ File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size/1024, 1)} KB)")

st.markdown("</div>", unsafe_allow_html=True)

# Analysis button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 Launch Professional Analysis",
        use_container_width=True,
        key="analyze_btn"
    )

# Analysis execution
if analyze_button:
    # Input validation
    has_input = bool(claim or url or youtube_url or uploaded_file)
    
    if not has_input:
        st.error("⚠️ **Input Required:** Please provide content to analyze before starting the verification process.")
        st.stop()
    
    # Processing indicator
    with st.spinner("🔍 **VERIFACT Analysis in Progress** - Our AI agents are researching, analyzing, and verifying your content..."):
        input_content = ""

        # File processing
        if uploaded_file:
            from pathlib import Path
            suffix = Path(uploaded_file.name).suffix.lower()
            try:
                if suffix == ".pdf":
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    input_content = "".join([page.extract_text() for page in reader.pages])
                elif suffix == ".docx":
                    from docx import Document
                    doc = Document(uploaded_file)
                    input_content = "\n".join([p.text for p in doc.paragraphs])
                elif suffix == ".txt":
                    raw = uploaded_file.read()
                    for enc in ["utf-8", "utf-16", "latin-1", "cp1252"]:
                        try:
                            input_content = raw.decode(enc)
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        st.error("❌ **File Processing Error:** Unable to decode text file. Please ensure UTF-8 encoding.")
                        st.stop()
                else:
                    st.error("❌ **Unsupported Format:** Please upload a PDF, Word document, or text file.")
                    st.stop()
            except Exception as e:
                st.error(f"❌ **File Processing Error:** {e}")
                st.stop()
        else:
            input_content = claim or url or youtube_url

        # Run analysis
        try:
            progress = st.progress(0, text="Initializing VERIFACT system...")
            progress.progress(20, text="Loading AI agents...")
            checker = FactChecker()
            progress.progress(60, text="Executing multi-agent analysis...")
            result = checker.crew().kickoff(inputs={"input_content": input_content})
            progress.progress(100, text="Analysis complete!")
        except Exception as e:
            st.error(f"❌ **Analysis Error:** {e}")
            st.stop()

    # Success notification
    st.balloons()
    st.success("🎉 **Analysis Complete** - Professional verification report generated successfully")

    # Results section
    st.markdown("""
    <div class="results-section">
    """, unsafe_allow_html=True)

    # Verdict analysis and display
    result_text = str(result)
    result_lower = result_text.lower()

    st.markdown("### 📊 Verification Result")
    
    # Determine verdict
    if "true" in result_lower and "false" not in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-true">
            ✅ VERDICT: THE PROVIDED INFORMATION IS TRUE
        </div>
        """, unsafe_allow_html=True)
    elif "false" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-false">
            ❌ VERDICT: THE PROVIDED INFORMATION IS FALSE
        </div>
        """, unsafe_allow_html=True)
    elif "misleading" in result_lower or "partially" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-partial">
            ⚠️ VERDICT: THE PROVIDED INFORMATION IS PARTIALLY ACCURATE
        </div>
        """, unsafe_allow_html=True)
    elif "INCONCLUSIVE" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-inconclusive">
            🔍 VERDICT: REQUIRES FURTHER INVESTIGATION
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="verdict-container verdict-inconclusive">
            📋 DETAILED ANALYSIS AVAILABLE
        </div>
        """, unsafe_allow_html=True)

    # Detailed report
    st.markdown("### 📄 Comprehensive Analysis Report")
    with st.expander("**Click to view detailed verification report**", expanded=True):
        st.markdown(result_text)

    st.markdown("</div>", unsafe_allow_html=True)

    # Download options
    st.markdown("### 📥 Export Options")
    col1, col2 = st.columns(2)

    with col1:
        # Text report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            report_header = f"VERIFACT PROFESSIONAL VERIFICATION REPORT\n{'='*50}\n\n"
            report_header += f"Input Content: {input_content[:200]}{'...' if len(input_content) > 200 else ''}\n\n"
            report_header += f"Analysis Results:\n{'-'*20}\n\n{result_text}"
            f.write(report_header)
            temp_path = f.name
        
        with open(temp_path, "rb") as f:
            st.download_button(
                "📄 Download as Text Report",
                f.read(),
                "verifact_professional_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    with col2:
        # Markdown report
        md_report = f"""# VERIFACT Professional Verification Report

## Input Analysis
**Content:** {input_content[:200]}{'...' if len(input_content) > 200 else ''}

## Verification Results

{result_text}

---
*Generated by VERIFACT AI Fact-Checking System*
*Powered by Multi-Agent Intelligence Architecture*
"""
        st.download_button(
            "📋 Download as Markdown",
            md_report,
            "verifact_professional_report.md",
            mime="text/markdown",
            use_container_width=True
        )

# Simple Professional Footer - Fixed Copyright Display
# Simple Professional Footer - Fixed Copyright Display
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    padding: 2rem;
    border-radius: 15px;
    margin-top: 3rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
">
    <a href="mailto:rs_bunnybobbali@outlook.com" style="
        color: white !important;
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 600;
        display: block;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    ">📧 rs_bunnybobbali@outlook.com</a>
    
    © 2025 RAMANA SOFT - All Rights Reserved
</div>
""", unsafe_allow_html=True)