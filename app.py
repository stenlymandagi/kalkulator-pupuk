import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Pupuk Presisi V2", page_icon="🌶️", layout="centered")

st.title("🌶️ Kalkulator Pemupukan Presisi Cabe (V2)")
st.write("Aplikasi untuk Pembelajaran di Pelatihan Sekolah Lapang Agrobisnis Komoditas Unggulan Cabe bagi Petani Tahun 2026 - BPTP Prov. SULUT")

# --- INPUT PARAMETER ---
st.header("1. Data Lahan & Target Populasi")
populasi = st.number_input("Jumlah Populasi Pohon (Batang):", min_value=1, value=2500, step=100)

st.header("2. Komposisi Pupuk Dasar (Sebelum Tanam)")
pukand = st.number_input("Total Pupuk Kandang (kg):", min_value=0, value=2000, step=100)
fertiphos = st.number_input("Total Pupuk Fertiphos (kg):", min_value=0, value=25, step=5)

st.subheader("⚠️ Tambahan NPK Komersial untuk Pupuk Dasar")
st.write("Isi jika Anda mencampur pupuk NPK ke dalam bedengan di awal. Jika tidak ada, isi berat dengan angka 0.")
kg_npk_dasar = st.number_input("Berat Pupuk NPK Dasar yang digunakan (kg):", min_value=0.0, value=10.0, step=1.0)
n_dasar_input = st.number_input("Kandungan N pada NPK Dasar (%)", value=9.0)
p_dasar_input = st.number_input("Kandungan P pada NPK Dasar (%)", value=25.0)
k_dasar_input = st.number_input("Kandungan K pada NPK Dasar (%)", value=25.0)

st.header("3. Stok Pupuk untuk Fase Susulan (Kocor)")
st.write("Masukkan persentase kandungan N-P-K dari merek pupuk kocor yang Anda miliki saat ini:")

col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Fase Veg (cth: Mutiara)**")
    n_veg = st.number_input("N (%)", value=16.0, key="nv")
    p_veg = st.number_input("P (%)", value=16.0, key="pv")
    k_veg = st.number_input("K (%)", value=16.0, key="kv")
with col2:
    st.write("**Fase Bunga (cth: Prof)**")
    n_flo = st.number_input("N (%)", value=9.0, key="nf")
    p_flo = st.number_input("P (%)", value=25.0, key="pf")
    k_flo = st.number_input("K (%)", value=25.0, key="kf")
with col3:
    st.write("**Fase Buah (cth: Grower)**")
    n_fru = st.number_input("N (%)", value=15.0, key="nfr")
    p_fru = st.number_input("P (%)", value=9.0, key="pfr")
    k_fru = st.number_input("K (%)", value=20.0, key="kfr")

# --- PROSES PERHITUNGAN PRESISI ---
# 1. Kebutuhan Total Teoretis (Target awal per pohon: N=4g, P=3.6g, K=5g)
n_target = (4.0 * populasi) / 1000
p_target = (3.6 * populasi) / 1000 
k_target = (5.0 * populasi) / 1000

# 2. Menghitung Total Suplai Hara dari Pupuk Dasar yang diaplikasikan
# a) Dari Pupuk Kandang (Asumsi efisiensi 50%)
n_dari_pukand = pukand * 0.005 * 0.5
p_dari_pukand = pukand * 0.0025 * 0.5
k_dari_pukand = pukand * 0.005 * 0.5

# b) Dari Fertiphos (P2O5 = 20%)
p_dari_fertiphos = fertiphos * 0.20

# c) Dari NPK Dasar Kustom Pilihan Petani
n_dari_npk_dasar = kg_npk_dasar * (n_dasar_input / 100)
p_dari_npk_dasar = kg_npk_dasar * (p_dasar_input / 100)
k_dari_npk_dasar = kg_npk_dasar * (k_dasar_input / 100)

# Total Hara yang sudah masuk di Pupuk Dasar
total_n_dasar = n_dari_pukand + n_dari_npk_dasar
total_p_dasar = p_dari_pukand + p_dari_fertiphos + p_dari_npk_dasar
total_k_dasar = k_dari_pukand + k_dari_npk_dasar

# 3. Sisa Kekurangan hara yang wajib dipenuhi dari Kocor Susulan
n_butuh = max(0.0, n_target - total_n_dasar)
p_butuh = max(0.0, p_target - total_p_dasar)
k_butuh = max(0.0, k_target - total_k_dasar)

# 4. Pembagian ke Pupuk Susulan Komersial (Sistem Kocor Berdasarkan Alokasi Fase)
kg_pupuk_veg = (n_butuh * 0.6) / (n_veg / 100) if n_veg > 0 else 0
kg_pupuk_flo = (p_butuh * 0.5) / (p_flo / 100) if p_flo > 0 else 0
kg_pupuk_fru = (k_butuh * 0.7) / (k_fru / 100) if k_fru > 0 else 0

# --- OUTPUT HASIL ---
st.markdown("---")
st.header("📊 Hasil Analisis Nutrisi Presisi")

# Status Evaluasi Pupuk Dasar
st.subheader("Evaluasi Hara dari Pupuk Dasar Anda:")
st.text(f"✔ Kandungan N Terpenuhi di Awal: {total_n_dasar:.2f} kg (Target Total: {n_target:.1f} kg)")
st.text(f"✔ Kandungan P Terpenuhi di Awal: {total_p_dasar:.2f} kg (Target Total: {p_target:.1f} kg)")
st.text(f"✔ Kandungan K Terpenuhi di Awal: {total_k_dasar:.2f} kg (Target Total: {k_target:.1f} kg)")

st.subheader("Sisa Kebutuhan Pupuk Kocor Susulan:")
if kg_pupuk_veg == 0 and kg_pupuk_flo == 0 and kg_pupuk_fru == 0:
    st.balloons()
    st.warning("Nutrisi dari Pupuk Dasar Anda sudah sangat tinggi! Dosis kocor susulan bisa sangat minimal atau dihentikan sementara agar tanaman tidak kelebihan hara (overdosis).")
else:
    st.success(f"🔹 **Pupuk Fase Vegetatif ({int(n_veg)}-{int(p_veg)}-{int(k_veg)}):** {kg_pupuk_veg:.1f} kg")
    st.success(f"🔹 **Pupuk Fase Pembungaan ({int(n_flo)}-{int(p_flo)}-{int(k_flo)}):** {kg_pupuk_flo:.1f} kg")
    st.success(f"🔹 **Pupuk Fase Pembuahan ({int(n_fru)}-{int(p_fru)}-{int(k_fru)}):** {kg_pupuk_fru:.1f} kg")

    st.markdown("---")
    st.subheader("📅 Jadwal Rekomendasi Lapangan (Sistem Kocor):")
    st.info(f"📅 **Fase Vegetatif (7-28 HST):** Kocor **{kg_pupuk_veg/4:.1f} kg** per minggu (Total 4 kali aplikasi).")
    st.info(f"📅 **Fase Pembungaan (35-45 HST):** Kocor **{kg_pupuk_flo/2:.1f} kg** per 10 hari (Total 2 kali aplikasi).")
    st.info(f"📅 **Fase Pembuahan (55-85+ HST):** Kocor **{kg_pupuk_fru/4:.1f} kg** per siklus petikan (Total 4 kali aplikasi dasar).")

# Copyright
st.write("created by @stenlymandagi")
