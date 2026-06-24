import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Pupuk Presisi", page_icon="🌶️", layout="centered")

st.title("🌶️ Kalkulator Pemupukan Presisi Cabe")
st.write("Didesain untuk tanah vulkanik (Tomohon) dengan pendekatan *Precision Farming* untuk Pembelajaran Sekolah Lapang Agrobisnis Komoditas Unggulan Cabe bagi Petani Tahun 2026.")

# --- INPUT PARAMETER ---
st.header("1. Input Data Lahan & Pupuk")

populasi = st.number_input("Jumlah Populasi Pohon (Batang):", min_value=1, value=2500, step=100)
pukand = st.number_input("Total Pupuk Kandang Dasar (kg):", min_value=0, value=2000, step=100)

st.subheader("Kandungan NPK Merek Pupuk yang Tersedia (%)")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Pupuk Veg (cth: Mutiara)**")
    n_veg = st.number_input("N (%)", value=16.0, key="nv")
    p_veg = st.number_input("P (%)", value=16.0, key="pv")
    k_veg = st.number_input("K (%)", value=16.0, key="kv")
with col2:
    st.write("**Pupuk Bunga (cth: Professional)**")
    n_flo = st.number_input("N (%)", value=9.0, key="nf")
    p_flo = st.number_input("P (%)", value=25.0, key="pf")
    k_flo = st.number_input("K (%)", value=25.0, key="kf")
with col3:
    st.write("**Pupuk Buah (cth: Grower)**")
    n_fru = st.number_input("N (%)", value=15.0, key="nfr")
    p_fru = st.number_input("P (%)", value=9.0, key="pfr")
    k_fru = st.number_input("K (%)", value=20.0, key="kfr")

# --- PROSES PERHITUNGAN ---
# 1. Kebutuhan Total Teoretis (gram per pohon) -> N=4g, P=3.6g (vulkanik), K=5g
n_target = (4.0 * populasi) / 1000
p_target = (3.6 * populasi) / 1000 
k_target = (5.0 * populasi) / 1000

# 2. Kontribusi Pupuk Kandang (Asumsi efisiensi 50% di tanah vulkanik)
n_dari_pukand = pukand * 0.005 * 0.5
p_dari_pukand = pukand * 0.0025 * 0.5
k_dari_pukand = pukand * 0.005 * 0.5

# 3. Kekurangan hara yang harus ditutup pupuk kimia
n_butuh = max(0.0, n_target - n_dari_pukand)
p_butuh = max(0.0, p_target - p_dari_pukand)
k_butuh = max(0.0, k_target - k_dari_pukand)

# 4. Alokasi Penggunaan Pupuk Komersial berdasarkan Rasio Fase
# Fase Vegetatif dominan menggunakan Pupuk Veg
kg_pupuk_veg = (n_butuh * 0.6) / (n_veg / 100)
# Fase Generatif Awal dominan menggunakan Pupuk Bunga (Fokus P)
kg_pupuk_flo = (p_butuh * 0.6) / (p_flo / 100)
# Fase Generatif Akhir dominan menggunakan Pupuk Buah (Fokus K)
kg_pupuk_fru = (k_butuh * 0.7) / (k_fru / 100)

# --- OUTPUT HASIL ---
st.markdown("---")
st.header("📊 Rekomendasi Kebutuhan Pupuk")

st.subheader("Total Stok Pupuk Kimia yang Diperlukan:")
st.success(f"🔹 **Pupuk Vegetatif (Rasio {int(n_veg)}-{int(p_veg)}-{int(k_veg)}):** {kg_pupuk_veg:.1f} kg")
st.success(f"🔹 **Pupuk Pembungaan (Rasio {int(n_flo)}-{int(p_flo)}-{int(k_flo)}):** {kg_pupuk_flo:.1f} kg")
st.success(f"🔹 **Pupuk Pembuahan (Rasio {int(n_fru)}-{int(p_fru)}-{int(k_fru)}):** {kg_pupuk_fru:.1f} kg")

st.markdown("---")
st.subheader("📅 Jadwal Aplikasi Berkala (Sistem Kocor):")
st.info(f"📅 **Fase Vegetatif (7-28 HST):** Kocor **{kg_pupuk_veg/4:.1f} kg** per minggu (Dibagi menjadi 4 kali aplikasi).")
st.info(f"📅 **Fase Pembungaan (35-45 HST):** Kocor **{kg_pupuk_flo/2:.1f} kg** per 10 hari (Dibagi menjadi 2 kali aplikasi).")
st.info(f"📅 **Fase Pembuahan (55-85+ HST):** Kocor **{kg_pupuk_fru/4:.1f} kg** per petikan/10 hari (Dibagi menjadi 4 kali aplikasi dasar).")

# --- COPYRIGHT ---
st.markdown("---")
st.write("dibuat oleh @stenlymandagi")
