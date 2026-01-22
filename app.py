"""
Skill Gap AI - Integrated Version
Combines the best features from both implementations
"""

import streamlit as st
from auth.login import show_login
from auth.register import show_register
from database.db import init_db
from utils.file_parser import parse_file, clean_text
from utils.skill_extractor import extract_skills_with_confidence, highlight_text
from utils.comparator import compare_skills_advanced
from utils.visualizer import create_integrated_visualizations
from utils.recommender import get_smart_recommendations
from utils.report_generator import generate_advanced_pdf_report, generate_csv_report
import os

# Page configuration
st.set_page_config(
    page_title="Skill Gap AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS combining both styles
st.markdown("""
    <style>
    /* Base dark theme */
    .main {
        background-color: #020617;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    /* Main header with gradient */
    .center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    }

    .hero-card {
    min-width: 900px;
    background: linear-gradient(90deg, #6a1b9a 0%, #8e24aa 50%, #667eea 100%);
    padding: 15px 70px;
    border-radius: 14px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 30px rgba(106, 27, 154, 0.3);
    }
    
    .hero-card h1 {
        margin: 0;
        font-size: 3.5rem;
        font-weight: 800;
    }
    
    .hero-card p {
        margin: 8px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }

    
    /* Dashboard card */
    .dashboard-card {
        background: #020617;
        border-radius: 22px;
        padding: 24px;
        margin-top: 24px;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.45);
    }
    
    /* Skill chips with confidence */
    .skill-chip {
        display: inline-block;
        padding: 6px 14px;
        margin: 0 6px 8px 0;
        border-radius: 999px;
        background: linear-gradient(135deg, #E8F6F3, #D5F4E6);
        color: #117A65;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(17, 122, 101, 0.2);
        box-shadow: 0 2px 8px rgba(17, 122, 101, 0.15);
    }
    
    .skill-chip-soft {
        background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
        color: #4338CA;
        border: 1px solid rgba(67, 56, 202, 0.2);
        box-shadow: 0 2px 8px rgba(67, 56, 202, 0.15);
    }
    
    .skill-chip-partial {
        background: linear-gradient(135deg, #FFF7ED, #FFEDD5);
        color: #C2410C;
        border: 1px solid rgba(194, 65, 12, 0.2);
    }
    
    .skill-chip-missing {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        color: #991B1B;
        border: 1px solid rgba(153, 27, 27, 0.2);
    }
    
    /* Metric boxes */
    .metric-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #F9FAFB;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Highlighted text box */
    .highlight-box {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #1e293b;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #e5e7eb;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .highlight {
        background: linear-gradient(135deg, #65a30d, #84cc16);
        padding: 2px 6px;
        border-radius: 4px;
        color: white;
        font-weight: 600;
    }
    
    /* Progress bars */
    .skill-bar {
        width: 100%;
        height: 12px;
        background: rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        margin-top: 8px;
        overflow: hidden;
        border: 1px solid rgba(31, 41, 55, 0.6);
    }
    
    .skill-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981);
        transition: width 0.6s ease;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1e3a8a, #1e40af);
        padding: 14px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        color: #dbeafe;
        margin: 12px 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #065f46, #047857);
        border-left: 4px solid #10b981;
        color: #d1fae5;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #92400e, #b45309);
        border-left: 4px solid #f59e0b;
        color: #fef3c7;
    }
    
    .error-box {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border-left: 4px solid #ef4444;
        color: #fee2e2;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f9fafb;
        margin: 2rem 0 1rem 0;
        padding-left: 12px;
        border-left: 4px solid;
        border-image: linear-gradient(180deg, #667eea, #764ba2) 1;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0f172a;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'logged_in': False,
        'user_email': None,
        'user_name': None,
        'resume_text': None,
        'jd_text': None,
        'resume_skills': None,
        'jd_skills': None,
        'analysis_complete': False,
        'comparison_results': None,
        'recommendations': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def show_home_page():
    """Display the main application page"""
    
    # Header
    st.markdown("""
        <div class="center-wrapper">
        <div class="hero-card">
        <h1>Skill Gap AI</h1>
        <p>Analyzing Resume and Job Description for Skill Gap!</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown(f"**📧** {st.session_state.user_email}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Workflow Steps")
        st.markdown("""
        1. 📄 Upload Documents
        2. 👀 Preview Parsed Text
        3. 🔬 Extract Skills
        4. 📊 Analyze Gaps
        5. 📥 Download Reports
        """)
        
        if st.session_state.analysis_complete:
            st.markdown("---")
            st.success("✅ Analysis Complete!")
            comparison = st.session_state.comparison_results
            st.metric("Match Score", f"{comparison['overall_match']:.1f}%")
    
    # Step 1: Document Upload
    st.markdown('<div class="section-header">📄 Upload Documents</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Resume")
        resume_method = st.radio(
            "Input Method",
            ["Upload File", "Paste Text"],
            key="resume_method",
            horizontal=True
        )
        
        if resume_method == "Upload File":
            resume_file = st.file_uploader(
                "Upload Resume (PDF/DOCX/TXT)",
                type=['pdf', 'docx', 'txt'],
                key="resume_file"
            )
            if resume_file:
                with st.spinner("🔄 Extracting text..."):
                    text = parse_file(resume_file)
                    if text:
                        st.session_state.resume_text = text
                        st.success("✅ Resume processed!")
                        st.caption(f"📊 {len(text)} chars | {len(text.split())} words")
        else:
            resume_input = st.text_area(
                "Paste Resume Text",
                height=200,
                key="resume_input"
            )
            if resume_input:
                st.session_state.resume_text = clean_text(resume_input)
    
    with col2:
        st.markdown("#### 💼 Job Description")
        jd_method = st.radio(
            "Input Method",
            ["Upload File", "Paste Text"],
            key="jd_method",
            horizontal=True
        )
        
        if jd_method == "Upload File":
            jd_file = st.file_uploader(
                "Upload Job Description (PDF/DOCX/TXT)",
                type=['pdf', 'docx', 'txt'],
                key="jd_file"
            )
            if jd_file:
                with st.spinner("🔄 Extracting text..."):
                    text = parse_file(jd_file)
                    if text:
                        st.session_state.jd_text = text
                        st.success("✅ Job description processed!")
                        st.caption(f"📊 {len(text)} chars | {len(text.split())} words")
        else:
            jd_input = st.text_area(
                "Paste Job Description Text",
                height=200,
                key="jd_input"
            )
            if jd_input:
                st.session_state.jd_text = clean_text(jd_input)
    
    # Step 2: Preview with Highlighting
    if st.session_state.resume_text and st.session_state.jd_text:
        st.markdown('<div class="section-header">👀 Preview with Skill Highlighting</div>', unsafe_allow_html=True)
        
        preview_tab1, preview_tab2 = st.tabs(["📝 Resume Preview", "💼 JD Preview"])
        
        with preview_tab1:
            if st.button("🔍 Highlight Skills in Resume", key="highlight_resume"):
                with st.spinner("Highlighting skills..."):
                    temp_skills = extract_skills_with_confidence(st.session_state.resume_text)
                    all_skills = []
                    for cat_data in temp_skills.values():
                        all_skills.extend(cat_data.keys())
                    
                    highlighted = highlight_text(st.session_state.resume_text, all_skills)
                    st.markdown(f'<div class="highlight-box">{highlighted}</div>', unsafe_allow_html=True)
        
        with preview_tab2:
            if st.button("🔍 Highlight Skills in JD", key="highlight_jd"):
                with st.spinner("Highlighting skills..."):
                    temp_skills = extract_skills_with_confidence(st.session_state.jd_text)
                    all_skills = []
                    for cat_data in temp_skills.values():
                        all_skills.extend(cat_data.keys())
                    
                    highlighted = highlight_text(st.session_state.jd_text, all_skills)
                    st.markdown(f'<div class="highlight-box">{highlighted}</div>', unsafe_allow_html=True)
        
        # Step 3: Skill Extraction and Analysis
        st.markdown('<div class="section-header">🔬 Advanced Skill Analysis</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Start ML-Powered Analysis", use_container_width=True, type="primary"):
            with st.spinner("🤖 Running advanced ML analysis... This may take a moment."):
                # Extract skills with confidence scores
                resume_skills = extract_skills_with_confidence(st.session_state.resume_text)
                jd_skills = extract_skills_with_confidence(st.session_state.jd_text)
                
                # Advanced comparison with TF-IDF
                comparison = compare_skills_advanced(resume_skills, jd_skills)
                
                # Get smart recommendations
                recommendations = get_smart_recommendations(comparison)
                
                # Store in session state
                st.session_state.resume_skills = resume_skills
                st.session_state.jd_skills = jd_skills
                st.session_state.comparison_results = comparison
                st.session_state.recommendations = recommendations
                st.session_state.analysis_complete = True
            
            st.success("✅ Analysis complete! Scroll down to view results.")
            st.rerun()
    
    # Step 4: Display Results
    if st.session_state.analysis_complete:
        st.markdown('<div class="section-header">📊 Comprehensive Results Dashboard</div>', unsafe_allow_html=True)
        
        comparison = st.session_state.comparison_results
        
        # Metrics Overview
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Overall Match</div>
                    <div class="metric-value">{comparison['overall_match']:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Matched Skills</div>
                    <div class="metric-value">{len(comparison['matched_skills'])}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Partial Matches</div>
                    <div class="metric-value">{len(comparison.get('partial_skills', []))}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Missing Skills</div>
                    <div class="metric-value">{len(comparison['missing_skills'])}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("### 📈 Advanced Visualizations")
        create_integrated_visualizations(comparison, st.session_state.resume_skills, st.session_state.jd_skills)
        
        # Detailed Skills Breakdown
        st.markdown("### 📋 Detailed Skill Analysis")
        
        skill_tabs = st.tabs([
            "✅ Matched Skills",
            "⚡ Partial Matches",
            "❌ Missing Skills",
            "➕ Extra Skills",
            "🎓 Smart Recommendations"
        ])
        
        with skill_tabs[0]:
            if comparison['matched_skills']:
                for skill in comparison['matched_skills']:
                    confidence = comparison.get('skill_confidences', {}).get(skill, 90)
                    st.markdown(f"""
                        <span class="skill-chip">{skill} ({confidence}%)</span>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="skill-bar">
                            <div class="skill-bar-fill" style="width: {confidence}%"></div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No perfect matches found.")
        
        with skill_tabs[1]:
            partial_skills = comparison.get('partial_skills', [])
            if partial_skills:
                for skill_data in partial_skills:
                    skill = skill_data['skill']
                    similarity = skill_data['similarity']
                    st.markdown(f"""
                        <span class="skill-chip skill-chip-partial">{skill} ({similarity:.0%} match)</span>
                    """, unsafe_allow_html=True)
            else:
                st.info("No partial matches found.")
        
        with skill_tabs[2]:
            if comparison['missing_skills']:
                st.markdown('<div class="warning-box">🎯 Focus on acquiring these critical skills to improve your match!</div>', unsafe_allow_html=True)
                for skill in comparison['missing_skills']:
                    st.markdown(f'<span class="skill-chip skill-chip-missing">❌ {skill}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">🎉 Excellent! You have all required skills!</div>', unsafe_allow_html=True)
        
        with skill_tabs[3]:
            extra = comparison.get('extra_skills', [])
            if extra:
                st.markdown('<div class="info-box">💎 These bonus skills make you stand out!</div>', unsafe_allow_html=True)
                for skill in extra:
                    st.markdown(f'<span class="skill-chip">{skill}</span>', unsafe_allow_html=True)
            else:
                st.info("No additional skills identified.")
        
        with skill_tabs[4]:
            if st.session_state.recommendations:
                st.markdown("### 🎓 Personalized Learning Recommendations")
                
                for skill, rec_data in st.session_state.recommendations.items():
                    st.markdown(f"#### 📘 {skill}")
                    
                    # Priority badge
                    priority = rec_data.get('priority', 'Medium')
                    if priority == 'Critical':
                        st.markdown('<div class="error-box">🔥 Critical Gap - Start immediately!</div>', unsafe_allow_html=True)
                    elif priority == 'High':
                        st.markdown('<div class="warning-box">⚡ High Priority - Focus area</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="info-box">📚 Recommended for improvement</div>', unsafe_allow_html=True)
                    
                    # Course recommendations
                    for course in rec_data.get('courses', []):
                        st.markdown(f"- **[{course['title']}]({course['url']})** - {course['platform']}")
            else:
                st.info("No recommendations needed - great job!")
        
        # Step 5: Reports
        st.markdown('<div class="section-header">📥 Download Reports</div>', unsafe_allow_html=True)
        
        report_col1, report_col2 = st.columns(2)
        
        with report_col1:
            if st.button("📄 Generate Advanced PDF Report", use_container_width=True):
                with st.spinner("Creating comprehensive PDF..."):
                    pdf_path = generate_advanced_pdf_report(
                        st.session_state.user_name,
                        st.session_state.user_email,
                        st.session_state.comparison_results,
                        st.session_state.recommendations
                    )
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                "💾 Download PDF Report",
                                f,
                                file_name="skillgap_ai_integrated_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        st.success("✅ PDF report ready!")
        
        with report_col2:
            if st.button("📊 Generate CSV Data Export", use_container_width=True):
                with st.spinner("Preparing CSV export..."):
                    csv_path = generate_csv_report(st.session_state.comparison_results)
                    if csv_path and os.path.exists(csv_path):
                        with open(csv_path, "rb") as f:
                            st.download_button(
                                "💾 Download CSV Report",
                                f,
                                file_name="skillgap_analysis.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        st.success("✅ CSV export ready!")

def main():
    """Main application entry point"""
    init_db()
    initialize_session_state()
    
    if not st.session_state.logged_in:
        # Hide header and clean up for auth pages
        st.markdown("""
            <style>
            /* Hide Streamlit header for auth pages */
            header[data-testid="stHeader"] {
                display: none;
            }
            
            /* Full height background */
            .main > div {
                padding-top: 0rem;
            }
            
            /* Auth page title */
            .auth-title {
                text-align: center;
                font-size: 5rem;
                font-weight: 1000;
                background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
                -webkit-background-clip: text;
                -webkit-text-fill-color: white;
                background-clip: text;
                margin: 60px 0 40px 0;
                letter-spacing: -1px;
                text-shadow: 0 0 8px rgba(186, 104, 200, 0.6),
                0 0 16px rgba(156, 39, 176, 0.6),
                0 0 32px rgba(124, 58, 237, 0.5),
                0 0 48px rgba(124, 58, 237, 0.4);
            }
            
            /* Move tabs to right corner */
            .stTabs [data-baseweb="tab-list"] {
                position: absolute;
                top: 20px;
                right: 10px;
                gap: 8px;
                background: #0f172a;
                padding: 8px;
                border-radius: 12px;
    
            }
            
            .stTabs [data-baseweb="tab"] {
                font-size: 0.85rem;
                padding: 8px 20px;
                border-radius: 12px;
                background: transparent;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            
            /* Compact form inputs */
            .stTextInput > div > div > input {
                padding: 10px 14px;
                font-size: 0.9rem;
            }
            
            /* Compact buttons */
            .stButton > button {
                padding: 10px 20px;
                font-size: 0.95rem;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Centered title
        st.markdown('<h1 class="auth-title">Skill Gap AI</h1>', unsafe_allow_html=True)
        
        # Authentication page with tabs in right corner
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_register()
    else:
        # Main application
        show_home_page()

if __name__ == "__main__":
    main()