import streamlit as st
import joblib
import time
import requests

st.set_page_config(page_title="AI Message Validator Pro", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'IBM+Plex+Sans', sans-serif;
        color: #263238;
    }

    .stApp {
        background-color: #fafafa;
    }

    /* Profesional Metric Card (Realistis) */
    .metric-container {
        display: flex;
        justify-content: space-around;
        gap: 25px;
        margin-bottom: 40px;
    }

    .metric-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        text-align: left;
        flex: 1;
        transition: 0.3s ease;
        border: 1px solid #eceff1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }
    
    .metric-card h3 {
        color: #6d4c41 !important; 
        font-size: 2.8rem;
        font-weight: 600;
        margin: 0;
        line-height: 1;
    }
    
    .metric-card p {
        color: #78909c !important;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
        margin-bottom: 0;
    }

    /* Input Styling (Clean) */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #cfd8dc !important;
        background-color: #ffffff !important;
        color: #263238 !important;
        padding: 20px !important;
        font-size: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #a1887f !important;
        box-shadow: 0 0 12px rgba(161, 136, 127, 0.1) !important;
    }

    /* Profesional Button (No Gradient) */
    div.stButton > button {
        border-radius: 12px !important;
        background-color: #6d4c41 !important;
        color: white !important;
        height: 3.8rem;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
        transition: 0.3s !important;
        box-shadow: 0 4px 6px rgba(109, 76, 65, 0.1) !important;
    }
    
    div.stButton > button:hover {
        background-color: #5d4037 !important;
        box-shadow: 0 6px 15px rgba(109, 76, 65, 0.3) !important;
    }
    
    /* Output Result Styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3643/3643948.png", width=60) # Ikon shield minimal
    st.markdown("<h2 style='color: #4e342e;'>Security Center</h2>", unsafe_allow_html=True)
    bahasa = st.selectbox("🌐 Analysis Language", ["Indonesia", "English"])
    st.divider()
    st.markdown("#### About the Engine")
    st.caption("This system employs a trained Naive Bayes classifier to identify linguistic patterns associated with bulk messaging and deceptive content.")
    st.caption("Engine Version: 1.2.0")

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #263238; font-size: 3rem; font-weight: 600;'>Message Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #78909c; margin-top: -10px; font-size: 1.1rem;'>Verify the integrity of your inbound communications.</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card"><h3>98.3%</h3><p>Engine Accuracy</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><h3>Instant</h3><p>Analysis Speed</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><h3>2026</h3><p>Dataset Base</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

try:
    if bahasa == "Indonesia":
        model = joblib.load('model_spam_indo.pkl')
        tfidf = joblib.load('vectorizer_indo.pkl')
        label = "Input pesan untuk validasi:"
        btn = "Validasi Sekarang"
        ph = "Tempel pesan di sini (misal: Anda mendapatkan promo khusus...)"
    else:
        model = joblib.load('model_spam_hasna.pkl')
        tfidf = joblib.load('vectorizer_hasna.pkl')
        label = "Enter message for validation:"
        btn = "Validate Message"
        ph = "Paste message here (e.g., You've been selected for a limited offer...)"
except:
    st.error("⚠️ System components missing. Please check model files.")
    st.stop()

c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    pesan = st.text_area(label, height=180, placeholder=ph, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(btn):
        if pesan.strip():
            with st.spinner('Analysing message patterns...'):
                time.sleep(0.8) 
                
                vektor = tfidf.transform([pesan]).toarray()
                pred = model.predict(vektor)
                
                st.markdown("---")
                if pred[0] == 1:
                    st.error("🔴 **RESULT: Message Flagged as Spam/Deceptive**")
                    st.toast("Security Alert!", icon="🚨")
                else:
                    st.success("🟢 **RESULT: Message Verified as Secure (Ham)**")
                    st.balloons()
        else:
            st.warning("Please provide a message.")

st.markdown("<br><br><br><p style='text-align: center; color: #b0bec5; font-size: 0.8rem; letter-spacing: 3px;'>INFORMATICS PROJECT CC • PROFESSIONAL GRADE SECURITY</p>", unsafe_allow_html=True)
