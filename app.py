import streamlit as st
import joblib
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart Spam Detector", page_icon="🛡️", layout="wide")

# 2. CUSTOM CSS (Agar tampilan estetik dan terbaca di Mode Terang/Gelap)
st.markdown("""
    <style>
    /* Latar belakang aplikasi */
    .stApp {
        background-color: #fdfaf9;
    }
    
    /* Style Kotak Statistik (Metrics) */
    .metric-card {
        background-color: rgba(255, 255, 255, 0.1); 
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #a1887f;
        margin-bottom: 20px;
    }
    
    /* Paksa warna teks angka dan judul di kotak agar selalu kelihatan */
    .metric-card h3 {
        color: #a1887f !important; 
        margin-bottom: 5px;
        font-size: 2rem;
    }
    
    .metric-card p {
        color: #6d4c41 !important;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* Input Box (Text Area) */
    textarea {
        border-radius: 15px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #a1887f;
        padding-top: 50px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.title("Settings")
    bahasa = st.selectbox("🌐 Pilih Bahasa", ["Indonesia", "English"])
    st.markdown("---")
    st.info("**Tips:** Masukkan kalimat yang cukup panjang agar AI bisa mengenali pola pesan dengan lebih akurat.")

# 4. HEADER
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🛡️ Smart Spam Detector")
    st.markdown("<p style='text-align: center; color: #6d4c41;'>Sistem Klasifikasi Pesan Otomatis berbasis Machine Learning</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. DASHBOARD STATISTIK (Metric Cards)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card"><h3>98%</h3><p>Model Accuracy</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><h3>< 1s</h3><p>Response Time</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><h3>TF-IDF</h3><p>NLP Method</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. LOGIKA LOADING MODEL & VECTORIZER
try:
    if bahasa == "Indonesia":
        model = joblib.load('model_spam_indo.pkl')
        tfidf = joblib.load('vectorizer_indo.pkl')
        label_text = "Masukkan pesan (Indonesia):"
        btn_label = "Periksa Sekarang"
        placeholder = "Contoh: Selamat! Anda mendapatkan hadiah 10jt..."
    else:
        model = joblib.load('model_spam_hasna.pkl')
        tfidf = joblib.load('vectorizer_hasna.pkl')
        label_text = "Enter message (English):"
        btn_label = "Check Now"
        placeholder = "Example: Get a free voucher by clicking this link..."
except Exception as e:
    st.error(f"⚠️ Error: File model (.pkl) tidak ditemukan atau rusak. Pastikan file sudah ada di GitHub.")
    st.stop()

# 7. AREA INPUT DAN PREDIKSI
left, mid, right = st.columns([1, 6, 1])
with mid:
    pesan = st.text_area(label_text, height=180, placeholder=placeholder)
    
    if st.button(btn_label, use_container_width=True):
        if pesan.strip() != "":
            with st.spinner('Sedang menganalisis teks...'):
                time.sleep(0.8) # Efek loading
                
                # Transformasi teks ke angka
                vektor_pesan = tfidf.transform([pesan]).toarray()
                prediksi = model.predict(vektor_pesan)
                
                st.markdown("---")
                if prediksi[0] == 1:
                    st.error("🚨 **HASIL ANALISIS: PESAN SPAM**")
                    st.warning("Hati-hati! Pesan ini terdeteksi sebagai spam, promosi paksaan, atau indikasi penipuan.")
                else:
                    st.success("✅ **HASIL ANALISIS: PESAN AMAN (HAM)**")
                    st.info("Pesan ini terlihat normal dan aman untuk dibaca.")
                    st.balloons()
        else:
            st.warning("Mohon masukkan teks terlebih dahulu untuk dianalisis.")

# 8. FOOTER
st.markdown("""
    <div class="footer">
        <hr>
        Informatics Project cc • 2026
    </div>
    """, unsafe_allow_html=True)
