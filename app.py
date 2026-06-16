import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION & ENTERPRISE UI THEME
# ==========================================
st.set_page_config(
    page_title="Enterprise Customer Insights Matrix",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp { background-color: #FDFEFE; color: #1E293B; }
        [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #0F172A !important; }
        [data-testid="stMetricLabel"] { font-size: 0.95rem !important; font-weight: 600 !important; color: #475569 !important; }
        .stTabs [data-baseweb="tab"] { font-weight: 700; font-size: 1.05rem; color: #64748B; }
        .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #2563EB !important; border-bottom-color: #2563EB !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ADVANCED DETERMINISTIC COMPLIANCE NLP ENGINE
# ==========================================
LEXICON = {
    "excellent": 0.9, "perfect": 1.0, "great": 0.7, "good": 0.5, "love": 0.8, 
    "amazing": 0.9, "helpful": 0.6, "friendly": 0.6, "fast": 0.7, "clean": 0.5, 
    "smooth": 0.6, "resolved": 0.7, "easy": 0.6, "satisfied": 0.7, "best": 0.8,
    "slow": -0.6, "wait": -0.5, "delay": -0.6, "hours": -0.4, "rude": -0.8, 
    "terrible": -0.9, "worst": -1.0, "broken": -0.8, "crash": -0.9, "bug": -0.7, 
    "error": -0.7, "fail": -0.8, "freeze": -0.8, "horrible": -0.9, "useless": -0.8, 
    "hate": -0.8, "frustrated": -0.7, "confusing": -0.5, "messy": -0.5, "expensive": -0.4
}

SERVQUAL_MAP = {
    "Reliability": ["crash", "bug", "error", "fail", "freeze", "broken", "glitch", "downtime", "loss"],
    "Responsiveness": ["slow", "wait", "delay", "time", "hour", "respond", "speed", "latency", "queue"],
    "Empathy": ["rude", "attitude", "helpful", "friendly", "support", "care", "ignored", "listen", "understand"],
    "Tangibles": ["ui", "layout", "font", "clean", "look", "screen", "interface", "design", "visual", "aesthetic"],
    "Assurance": ["security", "safe", "trust", "privacy", "leak", "hack", "confident", "compliance", "legal"]
}

def analyze_feedback(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0.0, "General", 3.0, "none"
    
    tokens = text.lower().split()
    score_sum = 0.0
    match_count = 0
    
    for token in tokens:
        clean_token = token.strip(".,!?\"'()[]{}")
        if clean_token in LEXICON:
            score_sum += LEXICON[clean_token]
            match_count += 1
            
    sentiment_score = score_sum / match_count if match_count > 0 else 0.0
    
    # Track which exact keywords triggered the classification
    triggered_keywords = []
    dimension_scores = {dim: 0 for dim in SERVQUAL_MAP}
    
    for dim, keywords in SERVQUAL_MAP.items():
        for kw in keywords:
            if kw in text.lower():
                dimension_scores[dim] += 1
                if kw not in triggered_keywords:
                    triggered_keywords.append(kw)
                
    max_matches = max(dimension_scores.values())
    chosen_dimension = [k for k, v in dimension_scores.items() if v == max_matches][0] if max_matches > 0 else "General"
    root_cause = ", ".join(triggered_keywords) if triggered_keywords else "unspecified terms"
    csat_proxy = round(((sentiment_score + 1.0) * 2.0) + 1.0, 2)
    
    return round(sentiment_score, 2), chosen_dimension, csat_proxy, root_cause

def process_dataframe(df, text_col):
    df = df.copy()
    results = df[text_col].astype(str).apply(analyze_feedback)
    df['Sentiment_Score'] = [r[0] for r in results]
    df['SERVQUAL_Dimension'] = [r[1] for r in results]
    df['CSAT_Proxy'] = [r[2] for r in results]
    df['Root_Cause_Keywords'] = [r[3] for r in results]
    return df

# ==========================================
# 3. HIGH-FIDELITY SAMPLE DATA GENERATOR
# ==========================================
def generate_mock_data():
    samples = [
        ("The platform UI layout looks super clean and modern, but checkout keeps throwing a database execution error.", "2026-06-14 09:12"),
        ("Customer support staff were incredibly friendly and helped me resolve my pipeline access token error within minutes.", "2026-06-14 11:45"),
        ("Extremely slow load performance today. I've been stuck waiting for over an hour for data exports to complete.", "2026-06-15 08:22"),
        ("I feel totally safe using this system. Their data compliance framework and security architecture are outstanding.", "2026-06-15 14:30"),
        ("The interface font options are hard to read and the screen alignment looks broken on small displays.", "2026-06-16 10:02"),
        ("Absolute downtime crash failure during our presentation. Complete application freeze.", "2026-06-16 10:15"),
        ("The technical team was completely rude and ignored my open ticket loops for two full days.", "2026-06-16 10:30")
    ]
    texts, times = zip(*samples)
    return pd.DataFrame({"Review_Text": list(texts), "Timestamp": list(times)})

# ==========================================
# 4. RUNTIME ENVIRONMENT CONTROL PANEL
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "analyzed_data" not in st.session_state:
    st.session_state.analyzed_data = None

with st.sidebar:
    st.title("🔐 Intelligence Control Panel")
    st.markdown("---")
    bypass_auth = st.checkbox("Demo Override (Bypass Security Token)", value=True)
    
    if not bypass_auth:
        token_input = st.text_input("Workspace Security Token", type="password")
        if token_input == "admin123":
            st.session_state.authenticated = True
            st.success("Authorization Confirmed")
        else:
            st.session_state.authenticated = False
            st.warning("Locked Status Protocol Active")
    else:
        st.session_state.authenticated = True

    st.markdown("---")
    st.subheader("Data Engine Utilities")
    if st.button("Inject High-Fidelity Mock Dataset", use_container_width=True, type="secondary"):
        st.session_state.staged_df = generate_mock_data()
        st.toast("Corporate sample data loaded successfully!", icon="📥")
        
    if st.button("Reset Global App Memory State", use_container_width=True, type="primary", icon="🗑️"):
        st.session_state.analyzed_data = None
        if "staged_df" in st.session_state:
            del st.session_state.staged_df
        st.rerun()

# ==========================================
# 5. CORE WORKFLOW APPLICATION LOGIC
# ==========================================
if st.session_state.authenticated:
    st.title("📊 Customer Feedback Analytics Engine")
    st.caption("Enterprise Feedback Vectoring | Dynamic Incident Extraction & Adaptive Prescriptive Remediation")
    st.divider()

    tab_ingest, tab_dashboard, tab_actions, tab_docs = st.tabs([
        "📥 Data Hub & Extraction Setup", 
        "📈 Strategic Dashboard", 
        "🎯 Automated Remediation Blueprint",
        "📄 Mathematical Engineering Brief"
    ])

    # --- TAB 1: DATA PIPELINES ---
    with tab_ingest:
        st.subheader("Ingestion Matrix Pipelines")
        input_strategy = st.radio("Select Processing Vector:", ["Direct Raw Text Analysis Block", "Enterprise Data File Upload (Bulk Engine)"], horizontal=True)
        active_df = st.session_state.get("staged_df", None)
        
        if input_strategy == "Direct Raw Text Analysis Block":
            user_text = st.text_area("Input Raw Text Feedback String", value="The app speed is slow and I had to wait for hours to get a response from customer care.")
            if st.button("Execute Single Sequence Parsing"):
                active_df = pd.DataFrame({"Review_Text": [user_text], "Timestamp": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")]})
                st.session_state.staged_df = active_df
                st.success("Single record captured in short-term buffer memory.")
        else:
            uploaded_file = st.file_uploader("Upload CSV or Excel Master sheets", type=["csv", "xlsx"])
            if uploaded_file:
                active_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.session_state.staged_df = active_df
                st.success(f"Staged {len(active_df)} target source rows for ingestion execution.")

        if active_df is not None:
            st.markdown("---")
            st.subheader("Data Schema Validation Mapping")
            columns = list(active_df.columns)
            c1, c2 = st.columns(2)
            with c1:
                target_text_col = st.selectbox("Target Content Column (Feedback text)", options=columns, index=columns.index("Review_Text") if "Review_Text" in columns else 0)
            with c2:
                target_time_col = st.selectbox("Target Temporal Column (Operational Timestamp)", options=["None - Bypass Temporal Alignment"] + columns, index=columns.index("Timestamp") if "Timestamp" in columns else 0)
                
            if st.button("🚀 Fire Core Analytical Analytics Engine", type="primary", use_container_width=True):
                out_df = process_dataframe(active_df, target_text_col)
                st.session_state.analyzed_data = out_df
                st.session_state.text_column_ref = target_text_col
                st.balloons()
                st.success("Execution complete. Move to the 'Strategic Dashboard' tab.")

    # --- TAB 2: STRATEGIC DASHBOARD ---
    with tab_dashboard:
        if st.session_state.analyzed_data is None:
            st.warning("⚠️ Processing Engine Idle. Please stage and analyze data inside the Ingestion Matrix tab first.")
        else:
            res_df = st.session_state.analyzed_data
            total_vol = len(res_df)
            avg_csat = res_df['CSAT_Proxy'].mean()
            avg_polarity = res_df['Sentiment_Score'].mean()
            positive_share = (len(res_df[res_df['Sentiment_Score'] > 0]) / total_vol) * 100
            
            st.subheader("💡 Strategic Operations Performance Summary")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Feedback Volume", f"{total_vol} Units")
            m2.metric("Aggregated CSAT Proxy Score", f"{avg_csat:.2f} / 5.0")
            m3.metric("Net Sentiment Polarity Index", f"{avg_polarity:+.2f}")
            m4.metric("Positive Sentiment Ratio", f"{positive_share:.1f}%")
            
            st.markdown("---")
            chart1, chart2 = st.columns(2)
            with chart1:
                st.subheader("SERVQUAL Dimensions Performance Density")
                counts = res_df['SERVQUAL_Dimension'].value_counts().reset_index()
                counts.columns = ['Dimension', 'Volume Tracker']
                st.plotly_chart(px.bar(counts, x='Dimension', y='Volume Tracker', color='Dimension', color_discrete_sequence=px.colors.qualitative.G10).update_layout(showlegend=False, height=350), use_container_width=True)
            with chart2:
                st.subheader("CSAT Distribution Spread Profile")
                st.plotly_chart(px.box(res_df, x='SERVQUAL_Dimension', y='CSAT_Proxy', color='SERVQUAL_Dimension', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, height=350), use_container_width=True)
                
            st.markdown("---")
            st.subheader("Granular Core Audit Ledger Data")
            st.dataframe(res_df, use_container_width=True, hide_index=True)

    # --- TAB 3: AUTOMATED REMEDIATION ENGINE (DYNAMICALLY POWERED BY DATA) ---
    with tab_actions:
        if st.session_state.analyzed_data is None:
            st.warning("⚠️ Action generation vector unavailable. No processed pipeline metrics located.")
        else:
            df_act = st.session_state.analyzed_data
            negative_elements = df_act[df_act['Sentiment_Score'] < 0.0]
            
            st.subheader("🎯 Real-Time Dynamically Extracted Mitigation Strategies")
            st.caption("This interface extracts root-cause metadata dynamically directly from your target file upload trends.")
            
            if negative_elements.empty:
                st.success("✅ Operational thresholds within nominal parameters. No systemic risk flags detected in this dataset.")
            else:
                # Group data to identify the true volume-based pain point
                vulnerability_summary = negative_elements.groupby('SERVQUAL_Dimension').agg(
                    Complaint_Count=('CSAT_Proxy', 'count'),
                    Average_CSAT=('CSAT_Proxy', 'mean')
                )
                
                worst_dim = vulnerability_summary['Complaint_Count'].idxmax()
                complaint_vol = vulnerability_summary.loc[worst_dim, 'Complaint_Count']
                worst_score = vulnerability_summary.loc[worst_dim, 'Average_CSAT']
                
                # Dynamic Token Extraction Layer: Find out what words are causing the pain
                worst_records = negative_elements[negative_elements['SERVQUAL_Dimension'] == worst_dim]
                all_keywords = []
                for keywords_str in worst_records['Root_Cause_Keywords'].dropna():
                    if keywords_str != "none":
                        all_keywords.extend([k.strip() for k in keywords_str.split(",")])
                
                unique_keywords = list(set(all_keywords))
                keyword_focus_string = ", ".join([f"'{k}'" for k in unique_keywords]) if unique_keywords else "unstructured text variables"

                # -------------------------------------------------------------
                # DYNAMIC PLAYBOOK COMPILER MATRIX
                # -------------------------------------------------------------
                st.markdown(f"### Primary Threat Analysis Vector: **{worst_dim} Framework**")
                st.markdown(f"**Data Footprint:** Found **{complaint_vol} explicit system vulnerabilities** averaging a critical `{worst_score:.2f} / 5.0` CSAT rating.")
                
                # Dynamic programmatic actions generation
                if worst_dim == "Reliability":
                    vulnerability_statement = f"System architecture stability failure driven primarily by user encounters with explicit platform triggers matching {keyword_focus_string}."
                    remediation_steps = [
                        f"Isolate production logs pinpointing processing faults specifically referencing key triggers: {keyword_focus_string}.",
                        "Spin up automated rollback regression matrices across code environments showing recent dependency updates.",
                        "Initialize localized circuit breakers on data pipelines to prevent full app crashes during peak transaction states."
                    ]
                elif worst_dim == "Responsiveness":
                    vulnerability_statement = f"Severe platform infrastructure bottlenecks and operational processing latencies detected, specifically driven by terms matching {keyword_focus_string}."
                    remediation_steps = [
                        f"Audit execution trace times on components matching user complaints around: {keyword_focus_string}.",
                        "Scale background compute node clusters horizontally to manage database request bottlenecks.",
                        "Configure strict system dead-letter-queues to automatically alert senior engineering staff if wait states exceed 15 minutes."
                    ]
                elif worst_dim == "Empathy":
                    vulnerability_statement = f"Severe communication and relational friction flags raised within support desk channels, specifically referencing operational triggers matching {keyword_focus_string}."
                    remediation_steps = [
                        f"Flag and inspect support tickets where customer communications contain phrases matching {keyword_focus_string}.",
                        "Initiate targeted support team recalibrations to standardize customer escalation management steps.",
                        "Deploy automated real-time alerts within internal messaging systems if tracking models flag toxic conversation lines."
                    ]
                elif worst_dim == "Tangibles":
                    vulnerability_statement = f"Visual layout presentation exceptions and interface navigation blocks identified by users via layout terms matching {keyword_focus_string}."
                    remediation_steps = [
                        f"Execute cross-device visual layout checks focusing specifically on features involving: {keyword_focus_string}.",
                        "Validate user-interface rendering CSS scripts to patch display alignment bugs causing scaling collapses.",
                        "Implement responsive viewport testing constraints inside deployment pipelines to block layout breaking changes."
                    ]
                elif worst_dim == "Assurance":
                    vulnerability_statement = f"Security compliance uncertainty or access credential authentication anxiety flagged by user strings matching {keyword_focus_string}."
                    remediation_steps = [
                        f"Deploy systematic penetration testing vectors across authentication endpoints mapping to: {keyword_focus_string}.",
                        "Publish clear encryption update logs to reassure users regarding network privacy standards.",
                        "Enforce strict token key renewal structures to limit workspace data exposure risks."
                    ]
                else:
                    vulnerability_statement = "Mixed generalized negative user signals requiring non-specific system-wide overview monitoring."
                    remediation_steps = [
                        "Deploy follow-up qualitative surveys to extract cleaner categorical data.",
                        "Run log trace audits on high-level application paths to locate edge-case exceptions."
                    ]

                # Render the compiled blueprint inside a premium UI component
                with st.container(border=True):
                    c_left, c_right = st.columns(2)
                    with c_left:
                        st.error("🚨 **Data-Driven Root Cause Identification**")
                        st.write(f"**System Summary:** {vulnerability_statement}")
                        st.write(f"**Isolated Target Keywords:** `{keyword_focus_string}`")
                        
                    with c_right:
                        st.success("⚙️ **Prescriptive Mitigation Action Script**")
                        for idx, step in enumerate(remediation_steps, 1):
                            st.write(f"{idx}. {step}")
                            
                # Contextual Data Display
                with st.expander(f"🔍 Audit the {complaint_vol} Raw Negative Quotes Powering This Specific Strategy", expanded=True):
                    for idx, row in worst_records.iterrows():
                        st.info(f"\"*{row[st.session_state.text_column_ref]}*\" (Calculated CSAT: **{row['CSAT_Proxy']}**) | Key triggers: `{row['Root_Cause_Keywords']}`")

    # --- TAB 4: MATHEMATICAL BLUEPRINT ---
    with tab_docs:
        st.subheader("Academic Formulation & Lexical Mapping Blueprint")
        with st.container(border=True):
            st.markdown(
                """
                ### Core Mathematical Projections
                Sentiment tracking maps raw token patterns into a bounded space of $[-1.0, +1.0]$.
                To standardize metrics for traditional management dashboards, this value is linearly projected onto standard corporate tracking scales via an explicit conversion equation:
                
                $$\\text{CSAT Proxy Score} = \\left( \\frac{\\text{Sentiment Polarity Index} + 1.0}{2.0} \\right) \\times 4.0 + 1.0$$
                
                ### Dynamic Remediation Mechanics
                Unlike static alert architectures, this platform parses sub-token lists dynamically during runtime:
                1. **Volume Extraction:** Aggregates negative vectors to calculate the highest incident frequency density per dimension.
                2. **Token Inversion Mapping:** Re-scans the source string to isolate the actual keywords (`Root_Cause_Keywords`) triggering system rules.
                3. **Script Compilation:** Generates programmatically accurate business solutions using contextual string interpolation based on user inputs.
                """
            )

else:
    st.error("🔒 Workspace Authentication Barrier Active")
