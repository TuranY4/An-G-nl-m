import datetime
import json
import os
import random
import streamlit as st
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Anı Günlüğü", page_icon="📸", layout="centered"
)

# 👑 YÖNETİCİ E-POSTA ADRESİN (Telefondan girerken yazdığın e-posta ile BİREBİR AYNI olmalı!)
ADMIN_EMAIL = "turanyonetıcı4@gmail.com" 

# Günün Motivasyon Sözleri
MOTIVASYON_SOZLERI = [
    "✨ Her gün yeni bir başlangıçtır, anılarını ölümsüzleştir!",
    "🚀 Bugün yaşadığın bir anı, yarının en güzel tebessümü olacak.",
    "📸 Küçük anlar, en büyük hatıralara dönüşür.",
    "⭐ Hayat, biriktirdiğin güzel anılardan ibarettir.",
    "💡 Bugün kendine iyi bak ve güzel bir hatıra bırak!"
]

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
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px; color: #e2e8f0; padding: 8px 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e11d48, #be123c) !important;
        color: white !important; border: none !important;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
    }
    div.stButton > button {
        width: 100%; background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white; font-weight: bold; border: none; padding: 10px;
        border-radius: 12px; transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
    }
    .quote-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #a855f7;
        padding: 12px 16px;
        border-radius: 8px;
        font-style: italic;
        margin-bottom: 20px;
        text-align: center;
    }
    .announcement-box {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid #f43f5e;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .admin-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_FILE = "ani_verileri.json"
SYSTEM_FILE = "sistem_verileri.json"
IMAGE_DIR = "yuklenen_fotograflar"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

if not os.path.exists(SYSTEM_FILE):
    with open(SYSTEM_FILE, "w", encoding="utf-8") as f:
        json.dump({"duyuru": ""}, f)


def veri_yukle():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def sistem_yukle():
    if not os.path.exists(SYSTEM_FILE):
        return {"duyuru": ""}
    with open(SYSTEM_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"duyuru": ""}


def sistem_kaydet(data):
    with open(SYSTEM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Oturum Koruma
query_params = st.query_params
url_email = query_params.get("user", None)

if "kullanici_email" not in st.session_state:
    st.session_state.kullanici_email = url_email

st.title("✨ 📸 Anı Günlüğü ✨")

# Giriş Ekranı
if not st.session_state.kullanici_email:
    st.markdown(f'<div class="quote-box">{random.choice(MOTIVASYON_SOZLERI)}</div>', unsafe_allow_html=True)
    st.subheader("🔑 Giriş Yap / Kaydol")
    email = st.text_input("E-posta Adresinizi Girin:", placeholder="ornek@gmail.com")

    if st.button("Giriş Yap"):
        if email and "@" in email and "." in email and len(email) > 5:
            email_clean = email.strip().lower()
            st.session_state.kullanici_email = email_clean
            st.query_params["user"] = email_clean

            veriler = veri_yukle()
            if email_clean not in veriler:
                veriler[email_clean] = {}
                veri_kaydet(veriler)

            st.success(f"Hoş geldin, {email_clean}!")
            st.rerun()
        else:
            st.error("Lütfen geçerli bir e-posta adresi girin.")
else:
    kullanici_id = st.session_state.kullanici_email.strip().lower()
    admin_clean = ADMIN_EMAIL.strip().lower()
    is_admin = kullanici_id == admin_clean

    # Sistem Duyurusu
    sistem_data = sistem_yukle()
    if sistem_data.get("duyuru"):
        st.markdown(f'<div class="announcement-box">📢 <b>Sistem Duyurusu:</b> {sistem_data["duyuru"]}</div>', unsafe_allow_html=True)

    # Yan Menü
    st.sidebar.write(f"👤 **Giriş Yapan:** {kullanici_id}")
    if is_admin:
        st.sidebar.markdown("👑 **Özel Yönetici Paneli Aktif**")

    if st.sidebar.button("Çıkış Yap"):
        st.session_state.kullanici_email = None
        if "user" in st.query_params:
            del st.query_params["user"]
        st.rerun()

    # Sekmeler
    tab_list = ["➕ Yeni Anı", "📅 Anılarım", "⭐ Favoriler", "📊 İstatistikler"]
    if is_admin:
        tab_list.append("👑 Admin Paneli")

    tabs = st.tabs(tab_list)

    # 1. SEKME: Yeni Anı Ekle
    with tabs[0]:
        st.subheader("Bugünün Anısını Kaydet")
        tarih = st.date_input("Tarih Seç", datetime.date.today())
        tarih_str = str(tarih)

        ruh_hali = st.selectbox("Bugünkü Ruh Halin:", [
            "😊 Mutlu", "🚀 Heyecanlı", "☕ Sakin", 
            "😴 Yorgun", "🔥 Motivasyonlu", "🥳 Eğlenceli", "❤️ Sevgi Dolu"
        ])

        foto = st.file_uploader("Bir Fotoğraf Seç / Çek", type=["jpg", "jpeg", "png"])
        not_metni = st.text_area("Bugün neler oldu? (Kısa bir not bırak)")

        if st.button("🚀 Anıyı Kaydet"):
            if foto is not None and not_metni:
                dosya_uzantisi = foto.name.split(".")[-1]
                foto_adi = f"{kullanici_id}_{tarih_str}.{dosya_uzantisi}"
                foto_yolu = os.path.join(IMAGE_DIR, foto_adi)

                image = Image.open(foto)
                image.save(foto_yolu)

                veriler = veri_yukle()
                if kullanici_id not in veriler:
                    veriler[kullanici_id] = {}

                veriler[kullanici_id][tarih_str] = {
                    "foto_yolu": foto_yolu,
                    "not": not_metni,
                    "ruh_hali": ruh_hali,
                    "favori": False
                }
                veri_kaydet(veriler)

                st.balloons()
                st.success("Anın başarıyla kaydedildi! 🎉")
                st.image(image)
            else:
                st.warning("Lütfen hem fotoğraf yükle hem de bir not yaz.")

    # 2. SEKME: Anılarım
    with tabs[1]:
        st.subheader("Geçmiş Anıların")
        veriler = veri_yukle()
        kullanici_anilari = veriler.get(kullanici_id, {})

        if kullanici_anilari:
            arama_kelimesi = st.text_input("🔍 Notlarda Arama Yap:", placeholder="Kelime girin...")
            
            filtrelenmis = {}
            for t, a in kullanici_anilari.items():
                if arama_kelimesi.lower() in a.get("not", "").lower():
                    filtrelenmis[t] = a

            if filtrelenmis:
                secilen_tarih = st.selectbox(
                    "Tarih Seç:", sorted(list(filtrelenmis.keys()), reverse=True)
                )

                if secilen_tarih:
                    ani = filtrelenmis[secilen_tarih]
                    st.write(f"🗓️ **Tarih:** {secilen_tarih} | **Ruh Hali:** {ani.get('ruh_hali', '😊 Belirtilmemiş')}")
                    
                    if os.path.exists(ani["foto_yolu"]):
                        st.image(ani["foto_yolu"])
                    st.info(f"📝 **Notun:** {ani['not']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        is_fav = ani.get("favori", False)
                        fav_btn_label = "⭐ Favorilerden Çıkar" if is_fav else "☆ Favorilere Ekle"
                        if st.button(fav_btn_label):
                            veriler[kullanici_id][secilen_tarih]["favori"] = not is_fav
                            veri_kaydet(veriler)
                            st.rerun()

                    with col2:
                        if st.button("🗑️ Bu Anıyı Sil"):
                            if os.path.exists(ani["foto_yolu"]):
                                os.remove(ani["foto_yolu"])
                            del veriler[kullanici_id][secilen_tarih]
                            veri_kaydet(veriler)
                            st.success("Anı silindi!")
                            st.rerun()
            else:
                st.warning("Aramanıza uygun anı bulunamadı.")
        else:
            st.info("Henüz kaydedilmiş bir anın yok. İlk anını eklemekle başla!")

    # 3. SEKME: Favoriler
    with tabs[2]:
        st.subheader("⭐ Favori Anıların")
        veriler = veri_yukle()
        kullanici_anilari = veriler.get(kullanici_id, {})
        favoriler = {t: a for t, a in kullanici_anilari.items() if a.get("favori", False)}

        if favoriler:
            fav_tarih = st.selectbox("Favori Anı Seç:", sorted(list(favoriler.keys()), reverse=True))
            if fav_tarih:
                ani = favoriler[fav_tarih]
                st.write(f"🗓️ **Tarih:** {fav_tarih} | **Ruh Hali:** {ani.get('ruh_hali', '😊')}")
                if os.path.exists(ani["foto_yolu"]):
                    st.image(ani["foto_yolu"])
                st.info(f"📝 **Not:** {ani['not']}")
        else:
            st.info("Henüz favorilere eklenmiş anın yok. Anılarım sekmesinden favorilere ekleyebilirsin!")

    # 4. SEKME: İstatistikler
    with tabs[3]:
        st.subheader("📊 Kişisel İstatistiklerin")
        veriler = veri_yukle()
        kullanici_anilari = veriler.get(kullanici_id, {})
        
        toplam_ani = len(kullanici_anilari)
        toplam_fav = sum(1 for a in kullanici_anilari.values() if a.get("favori", False))

        c1, c2 = st.columns(2)
        c1.metric("📸 Toplam Anı", toplam_ani)
        c2.metric("⭐ Favori Anı", toplam_fav)

        if kullanici_anilari:
            st.markdown("---")
            st.write("🎭 **Ruh Hali Dağılımın:**")
            ruh_halleri = [a.get("ruh_hali", "Belirtilmemiş") for a in kullanici_anilari.values()]
            from collections import Counter
            sayac = Counter(ruh_halleri)
            for mood, count in sayac.items():
                st.write(f"* **{mood}:** {count} defa")

    # 5. SEKME: Özel Tam Yetkili Admin Paneli
    if is_admin:
        with tabs[4]:
            st.subheader("👑 Özel Yönetici Kontrol Merkezi")
            veriler = veri_yukle()
            
            toplam_kullanici = len(veriler)
            toplam_platform_ani = sum(len(v) for v in veriler.values())

            # Genel Metrikler
            ac1, ac2 = st.columns(2)
            ac1.metric("👥 Kayıtlı E-Posta Sayısı", toplam_kullanici)
            ac2.metric("🖼️ Yüklenen Toplam Anı", toplam_platform_ani)

            st.markdown("---")
            
            # 1. Duyuru Yönetimi
            st.subheader("📢 Sistem Duyurusu Yayınla")
            mevcut_duyuru = sistem_yukle().get("duyuru", "")
            yeni_duyuru = st.text_input("Tüm kullanıcılara gösterilecek duyuru metni:", value=mevcut_duyuru)
            
            if st.button("Duyuruyu Kaydet & Yayınla"):
                sistem_data = sistem_yukle()
                sistem_data["duyuru"] = yeni_duyuru
                sistem_kaydet(sistem_data)
                st.success("Duyuru başarıyla yayınlandı!")
                st.rerun()

            st.markdown("---")
            
            # 2. Tüm Kullanıcıları ve Fotoğrafları İnceleme Alanı
            st.subheader("🔍 Tüm Kullanıcılar ve Fotoğraflar")
            
            if veriler:
                secilen_user = st.selectbox("İncelemek istediğin e-posta adresini seç:", list(veriler.keys()))
                
                if secilen_user:
                    user_anilari = veriler[secilen_user]
                    st.write(f"👤 **Seçilen Kullanıcı:** `{secilen_user}`")
                    st.write(f"📸 **Yüklediği Anı Sayısı:** {len(user_anilari)}")
                    
                    if user_anilari:
                        st.markdown("##### 📁 Kullanıcının Yüklediği Anı ve Fotoğraflar:")
                        for t, a in user_anilari.items():
                            with st.expander(f"🗓️ {t} - {a.get('ruh_hali', '😊')}"):
                                if os.path.exists(a["foto_yolu"]):
                                    st.image(a["foto_yolu"], width=300)
                                else:
                                    st.caption("⚠️ Fotoğraf görseli bulunamadı veya silinmiş.")
                                st.write(f"📝 **Not:** {a.get('not', '')}")
                    else:
                        st.info("Bu kullanıcı henüz hiç anı yüklememiş.")
            else:
                st.info("Sistemde henüz kayıtlı veri yok.")