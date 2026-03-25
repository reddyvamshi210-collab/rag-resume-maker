"""CSS styles for the Streamlit frontend."""

MAIN_CSS = """
<style>
    /* Main container */
    .block-container { padding-top: 2rem; max-width: 1200px; }

    /* ── Sidebar styling ─────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* All sidebar text: headings, paragraphs, labels, spans */
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stTextArea label,
    section[data-testid="stSidebar"] .stFileUploader label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
    }

    /* Sidebar radio options text */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Sidebar selectbox / dropdown display text */
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Sidebar text inputs */
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stTextArea textarea {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input::placeholder,
    section[data-testid="stSidebar"] .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    /* Sidebar file uploader */
    section[data-testid="stSidebar"] .stFileUploader section {
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    section[data-testid="stSidebar"] .stFileUploader section span,
    section[data-testid="stSidebar"] .stFileUploader section small,
    section[data-testid="stSidebar"] .stFileUploader section p {
        color: #c0c0c0 !important;
    }

    /* Sidebar primary button (Analyze & Generate) */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }

    /* Sidebar horizontal rule */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15) !important;
    }

    /* ── Score gauge ─────────────────────────────────────────────────── */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    .score-card .score-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .score-card .score-label {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }

    /* ── Metric cards ────────────────────────────────────────────────── */
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Keyword tags ────────────────────────────────────────────────── */
    .keyword-tag {
        display: inline-block;
        background: #e8f4f8;
        color: #0c5460;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        border: 1px solid #bee5eb;
        font-weight: 600;
    }
    .keyword-tag.missing {
        background: #fff3cd;
        color: #856404;
        border-color: #ffc107;
        font-weight: 700;
    }
    .keyword-tag.matched {
        background: #d4edda;
        color: #155724;
        border-color: #28a745;
        font-weight: 700;
    }

    /* ── Section cards ───────────────────────────────────────────────── */
    .section-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* ── Tab styling ─────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 24px;
        font-weight: 700;
        font-size: 0.95rem;
    }

    /* ── Download buttons ────────────────────────────────────────────── */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 700;
    }

    /* ── Welcome feature cards ───────────────────────────────────────── */
    .section-card h4 {
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    .section-card p {
        font-weight: 500 !important;
    }

    /* ── Results headings ────────────────────────────────────────────── */
    .stTabs h3, .stTabs h4 {
        font-weight: 700 !important;
    }
</style>
"""
