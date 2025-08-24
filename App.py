import streamlit as st
import pandas as pd
import hashlib
from io import BytesIO
from plus_admin import get_plus_admin  # pakai rules yang ada

st.title("📊 Laporan Harian")

# --- Input manual ---
st.subheader("Input Manual")
st.number_input("Uang Cash",   min_value=0, step=1000, key="uang_cash")
st.number_input("Uang Tarik",  min_value=0, step=1000, key="uang_tarik")
st.number_input("Voucher",     min_value=0, step=1000, key="voucher")
st.number_input("Barang",      min_value=0, step=1000, key="barang")

# --- Helper: proses file ke 2 tabel ---
def proses_file(file_bytes: bytes):
    df_data = pd.read_excel(BytesIO(file_bytes), sheet_name=0, header=2)
    df_data = df_data.loc[:, ~df_data.columns.str.contains("^Unnamed")]

    if "Harga Jual" in df_data.columns:
        df_data["Harga Jual"] = pd.to_numeric(df_data["Harga Jual"], errors="coerce").fillna(0)

    if "Harga Jual" in df_data.columns and "Status" in df_data.columns:
        df_data["Status"] = df_data["Status"].astype(str).str.strip().str.lower()
        df_laporan = df_data[(df_data["Harga Jual"] > 0) & (df_data["Status"] == "sukses")].copy()

        df_laporan.insert(0, "No", range(1, len(df_laporan) + 1))
        kolom_target = ["No", "ID Trx", "Tanggal", "Kode Produk",
                        "No Tujuan", "Harga Jual", "Status", "SN"]
        df_laporan = df_laporan[[c for c in kolom_target if c in df_laporan.columns]]

        if "Tanggal" in df_laporan.columns:
            df_laporan["Jam"] = pd.to_datetime(df_laporan["Tanggal"], errors="coerce").dt.strftime("%H:%M:%S")
            df_laporan = df_laporan.drop(columns=["Tanggal"])
            cols = df_laporan.columns.tolist()
            cols.insert(2, cols.pop(cols.index("Jam")))
            df_laporan = df_laporan[cols]

        # kolom Plus Admin berdasar rules
        df_laporan["Plus Admin"] = df_laporan.apply(
            lambda row: get_plus_admin(row["Kode Produk"], row["Harga Jual"]),
            axis=1
        )

        # taruh di samping Harga Jual
        cols = df_laporan.columns.tolist()
        if "Plus Admin" in cols and "Harga Jual" in cols:
            harga_idx = cols.index("Harga Jual")
            cols.insert(harga_idx + 1, cols.pop(cols.index("Plus Admin")))
            df_laporan = df_laporan[cols]

        return df_data, df_laporan
    else:
        return df_data, None

# --- Upload Excel ---
st.subheader("Upload Data Aplikasi")
uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type="xlsx", key="uploader")

# proses file HANYA jika benar-benar file baru
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_id = f"{uploaded_file.name}-{hashlib.md5(file_bytes).hexdigest()}"
    if st.session_state.get("file_id") != file_id:
        st.session_state["file_id"] = file_id
        df_data, df_laporan = proses_file(file_bytes)
        st.session_state["raw_data"] = df_data
        st.session_state["df_laporan"] = df_laporan
        st.success("✅ Data berhasil diproses dari file baru")

# --- Jika sudah ada data di session_state ---
if st.session_state.get("df_laporan") is not None:
    st.subheader("📋 Tabel Asli (Filtered)")
    st.dataframe(st.session_state["raw_data"], use_container_width=True)

    st.subheader("📋 Tabel Dengan Plus Admin (Editable)")
    df_edit = st.data_editor(
        st.session_state["df_laporan"],
        use_container_width=True,
        num_rows="dynamic",
        disabled=[c for c in st.session_state["df_laporan"].columns if c != "Plus Admin"]
    )

    # --- Highlight tabel khusus jika ada Plus Admin kosong ---
    df_kosong = df_edit[df_edit["Plus Admin"].isna() | (df_edit["Plus Admin"] == 0)]
    if not df_kosong.empty:
        st.subheader("⚠️ Data dengan Plus Admin kosong")
        st.dataframe(df_kosong, use_container_width=True)

    if st.button("Update"):
        # Pastikan kolom Plus Admin numerik (mengatasi input kosong/string)
        df_edit["Plus Admin"] = pd.to_numeric(df_edit["Plus Admin"], errors="coerce").fillna(0).astype(int)
        st.session_state["df_laporan"] = df_edit.copy()
        st.success("✅ Data berhasil diperbarui")

        st.subheader("📋 Tabel Setelah Update")
        st.dataframe(st.session_state["df_laporan"], use_container_width=True)

    if st.button("Generate Laporan"):
        df_final = st.session_state["df_laporan"].copy()
        df_final["Plus Admin"] = pd.to_numeric(df_final["Plus Admin"], errors="coerce").fillna(0)

        total_plus_admin = int(df_final["Plus Admin"].sum())
        total_voucher   = int(st.session_state.get("voucher", 0))
        total_barang    = int(st.session_state.get("barang", 0))

        total_aplikasi_excel = total_plus_admin + total_voucher + total_barang
        total_cash_tarik = int(st.session_state.get("uang_cash", 0)) + int(st.session_state.get("uang_tarik", 0))
        selisih = total_cash_tarik - total_aplikasi_excel

        st.subheader("📑 Hasil Laporan")
        st.write(f"💵 **Cash + Tarik:** Rp {total_cash_tarik:,.0f}")
        st.write(f"🧮 **Total Plus Admin (Excel):** Rp {total_plus_admin:,.0f}")
        st.write(f"🎟️ **Voucher:** Rp {total_voucher:,.0f}")
        st.write(f"📦 **Barang:** Rp {total_barang:,.0f}")
        st.write(f"📱 **Aplikasi (Excel + Voucher + Barang):** Rp {total_aplikasi_excel:,.0f}")
        st.write(f"➖ **Selisih:** Rp {selisih:,.0f}")

# --- Tombol Clear ---
if st.button("Clear All"):
    # hapus SEMUA data termasuk file uploader & input manual
    for k in ["raw_data", "df_laporan", "file_id", "uploader",
              "uang_cash", "uang_tarik", "voucher", "barang"]:
        st.session_state.pop(k, None)
    st.rerun()
