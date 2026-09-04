import datetime
import json
import os
import streamlit as st
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Anı Günlüğü", page_icon="📸", layout="centered"
)

# Özel Şık CSS Tasarımı
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }
    
    h1 {
        color: #f43f5e !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(244, 63, 94, 0.3);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #e2e8f0;
        padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e11d48, #be123c) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_FILE = "ani_verileri.json"
IMAGE_DIR = "yuklenen_fotograflar"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)


def veri_yukle():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


st.title("✨ 📸 Günün Anısı ✨")

# Sekmeler sadeleştirildi
tab1, tab2 = st.tabs(["➕  Yeni Anı Ekle", "📅  Anılar"])

with tab1:
    st.subheader("Bugünün Anısını Kaydet")
    tarih = st.date_input("Tarih Seç", datetime.date.today())
    tarih_str = str(tarih)

    foto = st.file_uploader(
        "Bir Fotoğraf Seç / Çek", type=["jpg", "jpeg", "png"]
    )
    not_metni = st.text_area("Bugün neler oldu? (Kısa bir not bırak)")

    if st.button("🚀 Anıyı Kaydet"):
        if foto is not None and not_metni:
            dosya_uzantisi = foto.name.split(".")[-1]
            foto_adi = f"{tarih_str}.{dosya_uzantisi}"
            foto_yolu = os.path.join(IMAGE_DIR, foto_adi)

            image = Image.open(foto)
            image.save(foto_yolu)

            veriler = veri_yukle()
            veriler[tarih_str] = {"foto_yolu": foto_yolu, "not": not_metni}
            veri_kaydet(veriler)

            st.balloons()
            st.success("Anın başarıyla kaydedildi! 🎉")
            st.image(image)
        else:
            st.warning("Lütfen hem fotoğraf yükle hem de bir not yaz.")

with tab2:
    st.subheader("Geçmiş Anıların")
    veriler = veri_yukle()

    if veriler:
        secilen_tarih = st.selectbox(
            "Tarih Seç:", sorted(list(veriler.keys()), reverse=True)
        )

        if secilen_tarih:
            ani = veriler[secilen_tarih]
            st.write(f"🗓️ **Tarih:** {secilen_tarih}")
            if os.path.exists(ani["foto_yolu"]):
                st.image(ani["foto_yolu"])
            st.info(f"📝 **Notun:** {ani['not']}")

            # Silme butonu sadece anı seçilip içine girildiğinde en altta çıkıyor
            st.markdown("---")
            if st.button("🗑️ Bu Anıyı Sil"):
                if os.path.exists(ani["foto_yolu"]):
                    os.remove(ani["foto_yolu"])

                del veriler[secilen_tarih]
                veri_kaydet(veriler)

                st.success("Anı başarıyla silindi!")
                st.rerun()
    else:
        st.info("Henüz kaydedilmiş bir anı yok. İlk anını eklemekle başla!")