import streamlit as st
import joblib

# Konfigurasi Halaman
st.set_page_config(page_title="Smart Spam Detector", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS (SOFT BROWN PROFESSIONAL) ---
st.markdown("""
    <style>
    /* 1. Background Animasi Soft Brown */
    .stApp {
        background: linear-gradient(-45deg, #efebe9, #d7ccc8, #f5f5f5, #bcaaa4);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Container Utama Glassmorphism */
    .main .block-container {
        background: rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(141, 110, 99, 0.1);
        margin-top: 40px;
    }

    /* 3. Judul Profesional */
    h1 {
        color: #4e342e !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
    }

    /* 4. Input Area dengan Teks Putih Terang */
    div[data-baseweb="textarea"] {
        background-color: #2d2d2d !important;
        border: 2px solid #d7ccc8 !important;
        border-radius: 15px !important;
    }
    
    textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    textarea::placeholder {
        color: #bcaaa4 !important;
    }

    /* 5. Tombol Profesional */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(45deg, #a1887f, #795548);
        color: white !important;
        border: none;
        padding: 15px;
        font-weight: bold;
        transition: 0.4s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(121, 85, 72, 0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(245, 245, 245, 0.6) !important;
        backdrop-filter: blur(10px);
    }
    
    label, p, span {
        color: #5d4037 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.title("Control Panel")
    bahasa = st.selectbox("🌐 Pilih Bahasa", ["Indonesia", "English"])
    st.write("---")
    st.caption("AI Smart Detector v3.5")

# --- LOGIKA LOADING MODEL ---
try:
    if bahasa == "Indonesia":
        model = joblib.load('model_spam_indo.pkl')
        tfidf = joblib.load('vectorizer_indo.pkl')
        label_text = "Masukkan pesan (Indonesia):"
        btn_label = "Periksa Sekarang"
        placeholder = "Contoh: 'Selamat! Anda memenangkan hadiah...'"
    else:
        model = joblib.load('model_spam_hasna.pkl')
        tfidf = joblib.load('vectorizer_hasna.pkl')
        label_text = "Input message (English):"
        btn_label = "Check Now"
        placeholder = "Example: 'Winner! You won a lottery...'"
except:
    st.error("⚠️ File Model (.pkl) tidak ditemukan!")
    st.stop()

# --- MAIN INTERFACE ---
st.title("🛡️ Smart Spam Detector")
st.markdown("<p style='text-align: center;'>Implementasi Machine Learning untuk Deteksi Dini Pesan Spam</p>", unsafe_allow_html=True)

pesan = st.text_area(label_text, height=150, placeholder=placeholder)

if st.button(btn_label):
    if pesan:
        with st.spinner('Menganalisis pesan...'):
            data_input = tfidf.transform([pesan]).toarray()
            prediksi = model.predict(data_input)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if prediksi[0] == 1:
                st.error("🚨 **HASIL ANALISIS: TERDETEKSI SEBAGAI SPAM!**")
            else:
                st.success("✅ **HASIL ANALISIS: PESAN DINYATAKAN AMAN (HAM)**")
                st.balloons()
    else:
        st.warning("Silakan isi teks pesan terlebih dahulu.")

# Footer Baru
st.markdown("<br><hr><center style='color: #a1887f; font-size: 0.8rem;'>Informatics Project cc</center>", unsafe_allow_html=True)