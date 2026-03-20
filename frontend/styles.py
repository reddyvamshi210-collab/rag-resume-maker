"""CSS styles for the Streamlit frontend."""

MAIN_CSS = """
<style>
    /* Main container */
    .block-container { padding-top: 2rem; max-width: 1200px; }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #e0e0e0 !important;
    }

    /* Score gauge */
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

    /* Metric cards */
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

    /* Keyword tags */
    .keyword-tag {
        display: inline-block;
        background: #e8f4f8;
        color: #0c5460;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        border: 1px solid #bee5eb;
    }
    .keyword-tag.missing {
        background: #fff3cd;
        color: #856404;
        border-color: #ffc107;
    }
    .keyword-tag.matched {
        background: #d4edda;
        color: #155724;
        border-color: #28a745;
    }

    /* Section cards */
    .section-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 24px;
        font-weight: 600;
    }

    /* Download buttons */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
"""
