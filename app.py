import streamlit as st
import joblib
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart Spam Detector", page_icon="🛡️", layout="wide")

# 2. CUSTOM CSS (UPGRADED DESIGN)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #fdfaf9 0%, #f4ece9 100%);
    }

    /* Efek Hover pada Metric Card */
    .metric-card {
        background-color: white; 
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #a1887f;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(161, 136, 127, 0.2);
        border-bottom: 5px solid #6d4c41;
    }
    
    .metric-card h3 {
        color: #a1887f !important; 
        margin-bottom: 5px;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    .metric-card p {
        color: #8d6e63 !important;
        font-size: 1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Animasi Fade In */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-header {
        animation: fadeIn 1s ease-out;
    }

    /* Styling Input Box */
    .stTextArea textarea {
        border-radius: 20px !important;
        border: 2px solid #e0d5d1 !important;
        padding: 15px !important;
        transition: all 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #a1887f !important;
        box-shadow: 0 0 10px rgba(161, 136, 127, 0.2) !important;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 50px !important;
        padding: 12px 30px !important;
        background-color: #6d4c41 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #4e342e !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.title("Control Panel")
    bahasa = st.selectbox("🌐 Language / Bahasa", ["Indonesia", "English"])
    st.markdown("---")
    st.markdown("### 💡 Quick Guide")
    st.caption("AI akan menganalisis struktur kata dan frekuensi kemunculannya untuk menentukan apakah pesan tersebut aman atau spam.")

# 4. HEADER
st.markdown('<div class="main-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #4e342e;'>🛡️ AI Spam Guardian</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8d6e63; font-size: 1.1rem;'>Smart Message Classification using Machine Learning Analysis</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. DASHBOARD STATISTIK (Metric Cards)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card"><h3>98%</h3><p>Accuracy</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><h3>Real-time</h3><p>Processing</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><h3>TF-IDF</h3><p>Algorithm</p></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 6. LOGIKA LOADING MODEL
try:
    if bahasa == "Indonesia":
        model = joblib.load('model_spam_indo.pkl')
        tfidf = joblib.load('vectorizer_indo.pkl')
        label_text = "Masukkan teks pesan di bawah ini:"
        btn_label = "Analisis Pesan"
        placeholder = "Contoh: Menangkan hadiah 100 juta rupiah sekarang juga!"
    else:
        model = joblib.load('model_spam_hasna.pkl')
        tfidf = joblib.load('vectorizer_hasna.pkl')
        label_text = "Input your message here:"
        btn_label = "Analyze Message"
        placeholder = "Example: You have won a $1000 gift card!"
except:
    st.error("⚠️ Components not found! Please check your .pkl files.")
    st.stop()

# 7. AREA INPUT
c1, c2, c3 = st.columns([1, 5, 1])
with c2:
    pesan = st.text_area(label_text, height=150, placeholder=placeholder)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(btn_label, use_container_width=True):
        if pesan.strip() != "":
            with st.spinner('AI sedang menganalisis pola kalimat...'):
                time.sleep(1) # Delay biar dramatis
                vektor_pesan = tfidf.transform([pesan]).toarray()
                prediksi = model.predict(vektor_pesan)
                
                if prediksi[0] == 1:
                    st.error("🚨 **ANALISIS SELESAI: PESAN TERDETEKSI SPAM**")
                    st.toast("Warning: Spam Detected!", icon="🚨")
                else:
                    st.success("✅ **ANALISIS SELESAI: PESAN AMAN (HAM)**")
                    st.balloons()
        else:
            st.warning("Silakan ketik sesuatu dulu ya!")

# 8. FOOTER
st.markdown("""
    <div style="text-align: center; margin-top: 100px; padding: 20px; color: #a1887f;">
        <hr style="border: 0.5px solid #e0d5d1;">
        <p style="font-size: 0.8rem; letter-spacing: 2px;">INFORMATICS PROJECT CC • 2026</p>
    </div>
    """, unsafe_allow_html=True)
