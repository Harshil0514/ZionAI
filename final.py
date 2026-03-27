import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
from datetime import datetime
import re
import streamlit as st

# 1. SECURITY: Simple Session Gate
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_user(username, password):
    # In production, check this against a Database (Supabase/Firebase)
    if username == "admin" and password == "imperium77":
        st.session_state.authenticated = True
    else:
        st.error("Invalid Credentials")

# 2. UI: The Login/Signup Page
if not st.session_state.authenticated:
    st.title("🛡️ IMPERIUM TERMINAL ACCESS")
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access Terminal"):
            login_user(u, p)
            st.rerun()
    
    with tab2:
        st.info("Subscription Fee: $99/Month. Redirecting to Stripe...")
        st.button("Pay & Register")
    st.stop() # Prevents the rest of the script from loading

# --- REST OF YOUR IMPERIUM CODE GOES BELOW THIS LINE ---

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="Imperium | Absolute Zero", layout="wide", page_icon="Logo.png")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 2px solid #C5A059; min-width: 420px; }
    h1, h2, h3 { color: #C5A059 !important; font-family: 'serif'; letter-spacing: 1px; }
    div[data-testid="stMetricValue"] { font-size: 38px !important; font-weight: 800; color: #FFFFFF !important; }
    input { background-color: #1c1c1c !important; color: #C5A059 !important; border: 1px solid #C5A059 !important; }
    
    .status-pulse {
        height: 14px; width: 14px; background-color: #28a745; 
        border-radius: 50%; display: inline-block; margin-right: 12px; 
        animation: pulse 1.8s infinite; vertical-align: middle;
    }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.8); } 70% { box-shadow: 0 0 0 14px rgba(40, 167, 69, 0); } 100% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); } }

    .stButton>button { 
        background: linear-gradient(135deg, #C5A059 0%, #8E6D29 100%); 
        color: black; font-weight: bold; width: 100%; border-radius: 10px; height: 3.8em; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATES ---
if "analysis_active" not in st.session_state:
    st.session_state.analysis_active = False
if "ai_brief" not in st.session_state:
    st.session_state.ai_brief = None

# --- 3. AI CORE ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. SIDEBAR (CONTROLS) ---
with st.sidebar:
    if os.path.exists("Logo.png"):
        st.image("Logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center; color:#C5A059;'>⚜️ IMPERIUM</h1>", unsafe_allow_html=True)
    
    st.markdown("<div><span class='status-pulse'></span><span style='color:#28a745; font-weight:bold;'>SYSTEM READY: STANDBY</span></div>", unsafe_allow_html=True)
    
    st.header("Corporate Identity")
    company_name = st.text_input("Corporate Entity Name", value="Global Enterprise Corp")
    industry = st.selectbox("Industry Sector", ["Manufacturing", "Banking", "Tech/SaaS", "Energy", "Logistics"])
    
    st.header("Enterprise Fundamentals")
    current_cash = st.number_input("Liquid Reserves ($)", value=5000000.0)
    monthly_rev = st.number_input("Base Monthly Revenue ($)", value=1200000.0)
    monthly_costs = st.number_input("Base Operating Costs ($)", value=850000.0)
    
    st.header("Financial Health Ratios")
    curr_ratio = st.number_input("Current Ratio", value=1.50)
    quick_ratio = st.number_input("Quick Ratio", value=1.10)
    debt_equity = st.number_input("Debt-to-Equity", value=0.50)
    op_margin = st.number_input("Operating Margin (%)", value=25.0)
    
    st.header("Black Swan Suite")
    recession = st.number_input("Market Demand Collapse (%)", value=35.0)
    tax_hike = st.number_input("Emergency Fiscal Tax Hike (%)", value=15.0)
    lehman_event = st.checkbox("Banking Collapse (Lehman Style)")
    covid_mode = st.checkbox("Pandemic Lockdown (Total)")
    suez_closure = st.checkbox("Trade Route Closure (Suez)")
    
    st.header("Recovery Measures")
    bailout = st.number_input("Federal Bailout Injection ($)", value=0.0)

    st.markdown("---")
    if st.button("⚡ EXECUTE SYSTEM ANALYSIS", use_container_width=True):
        st.session_state.analysis_active = True
        st.session_state.ai_brief = None

# --- 5. EXECUTION ENGINE ---
if st.session_state.analysis_active:
    liquidity_multiplier = 0.60 if lehman_event else 1.0
    effective_cash = (current_cash * liquidity_multiplier) + bailout
    rev_shock = 0.85 if covid_mode else (recession / 100)
    adj_rev = monthly_rev * (1 - rev_shock)
    cost_multiplier = 1.50 if suez_closure else 1.10
    adj_costs = monthly_costs * cost_multiplier
    interest_drag = (debt_equity * 0.05) * monthly_costs
    pre_tax_flow = (adj_rev - adj_costs) - interest_drag
    tax_cost = max(0, pre_tax_flow * (tax_hike / 100))
    final_net_flow = pre_tax_flow - tax_cost

    if final_net_flow < 0:
        runway = effective_cash / abs(final_net_flow)
        r_status, r_color = "BURN", "inverse"
        run_status, run_color = "DRAINING", "inverse"
    else:
        runway = 100.0
        r_status, r_color = "PROFIT", "normal"
        run_status, run_color = "STABLE", "normal"

    resilience = max(0, min(100, ((curr_ratio*10) + (op_margin*0.5)) - (debt_equity*15) - (rev_shock*20)))
    res_label = "NICE" if resilience >= 70 else "CAUTION" if resilience >= 40 else "RISK"
    res_color = "normal" if resilience >= 40 else "inverse"

    sensitivity_results = []
    for drop in [10, 30, 50, 70, 90]:
        s_rev = monthly_rev * (1 - (drop/100))
        s_flow = (s_rev - adj_costs) - interest_drag
        s_tax = max(0, s_flow * (tax_hike/100))
        s_final_flow = s_flow - s_tax
        s_runway = effective_cash / abs(s_final_flow) if s_final_flow < 0 else "Infinite"
        sensitivity_results.append([f"{drop}%", f"${s_final_flow:,.2f}", f"{s_runway if s_runway == 'Infinite' else f'{s_runway:.1f} Mo'}"])

    # --- PDF ENGINE ---
    class ImperiumPDF(FPDF):
        def header(self):
            self.set_line_width(0.5); self.set_draw_color(197, 160, 89)
            self.rect(5, 5, 200, 287) 
            self.set_line_width(0.1); self.rect(7, 7, 196, 283) 
            self.set_y(12); self.set_font('Helvetica', 'B', 15); self.set_text_color(197, 160, 89)
            self.cell(0, 8, f'IMPERIUM SOLVENCY REPORT: {company_name.upper()}', 0, 1, 'C')
            self.set_font('Helvetica', 'I', 8); self.set_text_color(128, 128, 128)
            now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
            self.cell(0, 6, f"Generation Timestamp: {now}", 0, 1, 'C')
            self.set_draw_color(197, 160, 89); self.line(20, 28, 190, 28); self.ln(12)

        def footer(self):
            self.set_y(-15); self.set_font('Helvetica', 'I', 8); self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def generate_pdf():
        projection = [max(0, effective_cash + (final_net_flow * i)) for i in range(13)]
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.fill_between(range(13), projection, color='#C5A059', alpha=0.2)
        ax.plot(range(13), projection, color='#C5A059', linewidth=3)
        ax.set_title(f"Strategic Capital Erosion: {company_name}", color='#C5A059', pad=20)
        ax.set_xlabel("Months"); ax.set_ylabel("Liquidity ($)")
        plt.savefig("line_chart.png", bbox_inches='tight', dpi=200, facecolor='#161B22'); plt.close()
        
        fig_ind, ax_ind = plt.subplots(figsize=(5, 4))
        score_color = '#28a745' if resilience >= 70 else '#C5A059' if resilience >= 40 else '#dc3545'
        ax_ind.text(0.5, 0.6, f"{resilience:.1f}", fontsize=65, ha='center', va='center', fontweight='bold', color=score_color)
        ax_ind.text(0.5, 0.3, f"RESILIENCE: {res_label}", fontsize=12, ha='center', va='center', color='white', fontweight='bold')
        ax_ind.axis('off')
        plt.savefig("gauge_chart.png", bbox_inches='tight', dpi=200, facecolor='#161B22'); plt.close()

        pdf = ImperiumPDF(); pdf.set_margins(20, 20, 20); pdf.add_page()
        pdf.set_font("Helvetica", 'B', 12); pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, " I. EXECUTIVE SUMMARY", 0, 1, 'L', 1); pdf.ln(3)
        pdf.set_font("Helvetica", '', 11); pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, f" - Net Flow: ${final_net_flow:,.2f}", 0, 1)
        pdf.cell(0, 7, f" - Resilience: {resilience:.1f}/100", 0, 1)
        pdf.cell(0, 7, f" - Survival: {runway:.1f} Months", 0, 1)

        pdf.ln(8); pdf.set_font("Helvetica", 'B', 12); pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, " II. VISUAL RISK DIAGNOSTICS", 0, 1, 'L', 1); pdf.ln(5)
        pdf.image("gauge_chart.png", x=22, y=pdf.get_y(), w=60); pdf.image("line_chart.png", x=88, y=pdf.get_y(), w=100); pdf.ln(65)

        pdf.set_font("Helvetica", 'B', 12); pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, " III. INSTITUTIONAL HEALTH MATRIX", 0, 1, 'L', 1); pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 10); pdf.set_fill_color(220, 220, 220); pdf.set_text_color(0, 0, 0)
        pdf.cell(45, 10, "Metric", 1, 0, 'C', 1); pdf.cell(40, 10, "Value", 1, 0, 'C', 1); pdf.cell(40, 10, "Benchmark", 1, 0, 'C', 1); pdf.cell(45, 10, "Status", 1, 1, 'C', 1)
        pdf.set_font("Helvetica", '', 10)
        for r in [["Current Ratio", f"{curr_ratio:.2f}", "> 1.20", "OK"], ["Quick Ratio", f"{quick_ratio:.2f}", "> 1.00", "OK"], 
                  ["Debt-Equity", f"{debt_equity:.2f}", "< 1.00", "OK"], ["Op Margin", f"{op_margin}%", "> 15%", "OK"]]:
            pdf.cell(45, 10, r[0], 1); pdf.cell(40, 10, r[1], 1, 0, 'C'); pdf.cell(40, 10, r[2], 1, 0, 'C'); pdf.cell(45, 10, r[3], 1, 1, 'C')

        # SECTION IV: MOVED TO NEW PAGE TO PREVENT DIVISION
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 12); pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, " IV. ADAPTIVE STRESS TEST RESULTS", 0, 1, 'L', 1); pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 10); pdf.set_fill_color(220, 220, 220); pdf.set_text_color(0, 0, 0)
        pdf.cell(55, 10, "Revenue Reduction", 1, 0, 'C', 1); pdf.cell(55, 10, "Adjusted Net Flow", 1, 0, 'C', 1); pdf.cell(60, 10, "Survival Period", 1, 1, 'C', 1)
        pdf.set_font("Helvetica", '', 10)
        for res in sensitivity_results:
            pdf.cell(55, 10, res[0], 1, 0, 'C'); pdf.cell(55, 10, res[1], 1, 0, 'C'); pdf.cell(60, 10, res[2], 1, 1, 'C')

        if st.session_state.ai_brief:
            pdf.add_page(); pdf.set_font("Helvetica", 'B', 12); pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, " V. AI STRATEGIC WAR ROOM ADVISORY", 0, 1, 'L', 1); pdf.ln(8)
            pdf.set_font("Helvetica", '', 11); pdf.set_text_color(0, 0, 0)
            clean_text = st.session_state.ai_brief.replace('**', '').replace('&*', '•').replace('*', '•')
            pdf.multi_cell(0, 7, clean_text.encode('latin-1', 'replace').decode('latin-1'))
        return pdf.output(dest='S').encode('latin-1', 'ignore')

    # --- 6. DASHBOARD UI ---
    st.title(f"🛡️ IMPERIUM : {company_name.upper()}")
    st.subheader(f"Institutional Solvency Terminal | {industry}")
    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Net Flow (Post-Shock)", f"${final_net_flow:,.2f}", delta=f"↑ {r_status}", delta_color=r_color)
    m2.metric("Survival Runway", f"{runway:.1f} Mo" if final_net_flow < 0 else "Infinite", delta=f"↑ {run_status}", delta_color=run_color)
    m3.metric("Resilience Index", f"{resilience:.1f}/100", delta=f"↑ {res_label}", delta_color=res_color)

    c_graph, c_sens = st.columns([2, 1])
    with c_graph:
        st.markdown(f"### 📉 Strategic Capital Erosion: {company_name}") 
        proj_y = [max(0, effective_cash + (final_net_flow * i)) for i in range(13)]
        fig = go.Figure(data=[go.Scatter(x=[f"Mo {i}" for i in range(13)], y=proj_y, fill='tozeroy', line=dict(color='#C5A059', width=5))])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Months", yaxis_title="Liquidity ($)")
        st.plotly_chart(fig, use_container_width=True)
    with c_sens:
        st.markdown("### 🧪 Stress Test: Revenue Flow") 
        st.table(pd.DataFrame(sensitivity_results, columns=["Rev Drop", "Net Flow", "Runway"]))

    act1, act2 = st.columns(2)
    with act1:
        if st.button("⚜️ ACTIVATE AI WAR ROOM STRATEGY"):
            with st.spinner("Analyzing Risks..."):
                prompt = f"CRO for {industry} firm. Resilience: {resilience}/100. Provide 3 tactical moves. No '?' or '*'."
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state.ai_brief = res.choices[0].message.content
                st.rerun()
    with act2:
        try:
            pdf_bytes = generate_pdf()
            st.download_button("📥 DOWNLOAD BOARD-READY PDF", data=pdf_bytes, file_name=f"Report_{company_name}.pdf", mime="application/pdf")
        except: st.warning("Activate AI Strategy first.")

    if st.session_state.ai_brief:
        st.markdown(f"""<div style="background:#161B22; padding:25px; border-left:10px solid #C5A059; border-radius:10px; color: #E0E0E0;">{st.session_state.ai_brief}</div>""", unsafe_allow_html=True)
else:
    st.info("👋 Welcome to Imperium. Adjust variables and click 'EXECUTE SYSTEM ANALYSIS' to begin.")
    st.image("https://via.placeholder.com/1200x400/0E1117/C5A059?text=SYSTEM+AWAITING+COMMAND+READY", use_container_width=True)
