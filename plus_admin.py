import math

def get_plus_admin(kode: str, harga_jual: float):
    kode = kode.upper().strip()

    # --- Khusus flat harga ---
    flat_map = {
        "SMDNS4": 20000,
        "ADMN25GB3": 13000,
        "TDHPM33": 13000,
        "TDHP11": 47000,
        "XLDHRM500": 11000,
        "IDFI7": 37000,
        "SDFB1": 13000,
        "TDHPM57": 23000,
        "XLTF20": 22000,
        "TDHPM11": 5000,
        "SMDUT2": 90000,
        "ADBT8": 40000,
        "FFR145": 20000,
        "ADMN1GB5": 15000,
        "FFR150": 21000,
        "STFP75": 77000,
        "IRP30": 33000,
        "ADBT6": 30000,
        "XLDXC10": 60000,
    }

    if kode in flat_map:
        return flat_map[kode]

    # harga_bulat biasanya dipakai untuk rules berikutnya
    harga_bulat = math.floor(harga_jual / 1000) * 1000

    # --- BRIBKT ---
    if kode == "BRIBKT":
        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999999:
            return harga_bulat + 10000
        elif 2000000 <= harga_bulat <= 2999999:
            return harga_bulat + 15000
        elif 3000000 <= harga_bulat <= 3999999:
            return harga_bulat + 20000
        elif 4000000 <= harga_bulat <= 6000000:
            return harga_bulat + 23000

    # --- GPYB3KT ---
    if kode == "GPYB3KT":
        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999999:
            return harga_bulat + (10000 - 1000)
        elif 2000000 <= harga_bulat <= 2999999:
            return harga_bulat + (15000 - 1000)
        elif 3000000 <= harga_bulat <= 3999999:
            return harga_bulat + (20000 - 1000)
        elif 4000000 <= harga_bulat <= 6000000:
            return harga_bulat + (23000 - 1000)

    # --- DNAB2KT ---
    if kode == "DNAB2KT":
        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999999:
            return harga_bulat + 10000
        elif 2000000 <= harga_bulat <= 2999999:
            return harga_bulat + 15000
        elif 3000000 <= harga_bulat <= 3999999:
            return harga_bulat + 20000
        elif 4000000 <= harga_bulat <= 6000000:
            return harga_bulat + 23000

    # --- BCABKT ---
    if kode == "BCABKT":
        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999999:
            return harga_bulat + 10000
        elif 2000000 <= harga_bulat <= 2999999:
            return harga_bulat + 15000
        elif 3000000 <= harga_bulat <= 3999999:
            return harga_bulat + 20000
        elif 4000000 <= harga_bulat <= 6000000:
            return harga_bulat + 23000

    # --- DNAB1KT ---
    if kode == "DNAB1KT":
        if 0 <= harga_bulat <= 200000:
            return harga_bulat + 2000
        elif 200001 <= harga_bulat <= 300000:
            return harga_bulat + 3000

            # --- BPTITELKOM ---
    if kode == "BPTITELKOM":
        return harga_bulat + 4000

    # --- BIFHM ---
    if kode == "BIFHM":
        return harga_bulat + 3000

    # --- BOMNI ---
    if kode == "BOMNI":
        return harga_bulat + 4000

    # --- BPIND ---
    if kode == "BPIND":
        return harga_bulat + 3000

    # --- SR series (SR5 = 5k, SR10 = 10k, +2k) ---
    if kode.startswith("SR"):
        try:
            sr_val = int(kode[2:])  # ambil angka setelah "SR"
            if sr_val > 0:
                return sr_val * 1000 + 2000
        except ValueError:
            pass

    # --- DNAKT1..50 (DNAKTxx + 2k) ---
    if kode.startswith("DNAKT"):
        try:
            dna_val = int(kode[5:])  # ambil angka setelah "DNAKT"
            if 1 <= dna_val <= 50:
                return dna_val * 1000 + 2000
        except ValueError:
            pass

    # --- BRIKT special ---
    if kode.startswith("BRIKT"):
        try:
            bri_val = int(kode[5:])  # ambil angka setelah "BRIKT"
            if 10 <= bri_val <= 50:
                return bri_val * 1000 + 3000
            elif 55 <= bri_val <= 950:
                return bri_val * 1000 + 5000
            elif bri_val == 1000:
                return bri_val * 1000 + 10000
        except ValueError:
            pass

    # --- BCAKT special ---
    if kode.startswith("BCAKT"):
        try:
            bca_val = int(kode[5:])  # ambil angka setelah "BCAKT"
            if 10 <= bca_val <= 50:
                return bca_val * 1000 + 3000
            elif 55 <= bca_val <= 950:
                return bca_val * 1000 + 5000
            elif bca_val == 1000:
                return bca_val * 1000 + 10000
        except ValueError:
            pass

            # --- DNAKT55..1000 (DNAKT special rules) ---
    if kode.startswith("DNAKT"):
        dna_val = int(kode[5:])
        if 55 <= dna_val <= 200:
            return dna_val * 1000 + 2000
        elif 205 <= dna_val <= 300:
            return dna_val * 1000 + 3000
        elif 350 <= dna_val <= 400:
            return dna_val * 1000 + 4000
        elif 450 <= dna_val <= 950:
            return dna_val * 1000 + 5000
        elif dna_val == 1000:
            return dna_val * 1000 + 10000
        return None

    # --- MANDKT series (ikut BRIKT55..1000) ---
    if kode.startswith("MANDKT"):
        man_val = int(kode[6:])
        if 55 <= man_val <= 950:
            return man_val * 1000 + 5000
        elif man_val == 1000:
            return man_val * 1000 + 10000
        return None

    # --- BNIKT series (ikut BRIKT55..1000) ---
    if kode.startswith("BNIKT"):
        bni_val = int(kode[5:])
        if 55 <= bni_val <= 950:
            return bni_val * 1000 + 5000
        elif bni_val == 1000:
            return bni_val * 1000 + 10000
        return None

    # --- GRBVD special ---
    if kode.startswith("GRBVD"):
        grb_val = int(kode[5:])
        if 10 <= grb_val <= 200:
            return grb_val * 1000 + 3000
        elif grb_val == 250:
            return grb_val * 1000 + 4000
        elif grb_val == 500:
            return grb_val * 1000 + 5000
        return None

    # --- GPYKT, LINKKT, OVOKT, SHPKT (ikut DNAKT rules) ---
    if kode.startswith(("GPYKT", "LINKKT", "OVOKT", "SHPKT")):
        # ambil angka setelah huruf T terakhir
        t_index = kode.rfind("T")
        g_val = int(kode[t_index + 1:])
        if 1 <= g_val <= 50:
            return g_val * 1000 + 2000
        elif 55 <= g_val <= 200:
            return g_val * 1000 + 2000
        elif 205 <= g_val <= 300:
            return g_val * 1000 + 3000
        elif 350 <= g_val <= 400:
            return g_val * 1000 + 4000
        elif 450 <= g_val <= 950:
            return g_val * 1000 + 5000
        elif g_val == 1000:
            return g_val * 1000 + 10000
        return None

    # --- PLNKT special ---
    if kode.startswith("PLNKT"):
        pln_val = int(kode[5:])
        if pln_val in (20, 50, 100):
            return pln_val * 1000 + 2000
        elif pln_val == 200:
            return pln_val * 1000 + 3000
        elif pln_val == 500:
            return pln_val * 1000 + 5000
        elif pln_val == 1000:
            return pln_val * 1000 + 7000
        return None

    # --- BRIVATG ---
    if kode == "BRIVATG":
        if harga_jual % 1000 >= 500:
            harga_bulat = ((harga_jual + 999) // 1000) * 1000  # RoundUp ke ribuan
        else:
            harga_bulat = (harga_jual // 1000) * 1000          # RoundDown ke ribuan

        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999000:
            return harga_bulat + 10000
        elif 2000000 <= harga_bulat <= 2999000:
            return harga_bulat + 15000
        elif 3000000 <= harga_bulat <= 3999000:
            return harga_bulat + 20000
        elif 4000000 <= harga_bulat <= 6999000:
            return harga_bulat + 23000
        elif harga_bulat >= 7000000:
            return int(harga_bulat * 1.004)
        return None

    # --- BTJAGO (selalu dibulatkan ke bawah) ---
    if kode == "BTJAGO":
        harga_bulat = (harga_jual // 1000) * 1000  # selalu round down

        if 1 <= harga_bulat <= 50000:
            return harga_bulat + 3000
        elif 51000 <= harga_bulat <= 999000:
            return harga_bulat + 5000
        elif 1000000 <= harga_bulat <= 1999000:
            return harga_bulat + 10000
        elif 2000000 <= harga_bulat <= 2999000:
            return harga_bulat + 15000
        elif 3000000 <= harga_bulat <= 3999000:
            return harga_bulat + 20000
        elif 4000000 <= harga_bulat <= 6999000:
            return harga_bulat + 23000
        elif harga_bulat >= 7000000:
            return int(harga_bulat * 1.004)
        return None

    # --- IR series (IRxx + 3k fix) ---
    if kode.startswith("IR"):
        ir_val = int(kode[2:])
        if ir_val > 0:
            return ir_val * 1000 + 3000

    # --- TR series (TRxx + 3k fix) ---
    if kode.startswith("TR"):
        tr_val = int(kode[2:])
        if tr_val > 0:
            return tr_val * 1000 + 3000

    # --- XAR series (XARxx + 2k fix) ---
    if kode.startswith("XAR"):
        xar_val = int(kode[3:])
        if xar_val > 0:
            return xar_val * 1000 + 2000

            # --- GPYB1KT (sama seperti DNAB1KT) ---
    if kode == "GPYB1KT":
        harga_bulat = int(harga_jual / 1000) * 1000
        if 0 <= harga_bulat <= 200_000:
            return harga_bulat + 2000
        elif 200_001 <= harga_bulat <= 300_000:
            return harga_bulat + 3000
        return None

    # --- FFR series (harga fix) ---
    if kode.startswith("FFR"):
        try:
            ffr_val = int(kode[3:])
        except ValueError:
            return None

        mapping_ffr = {
            20: 5000,
            55: 10000,
            75: 12000,
            100: 15000,
            140: 20000,
            200: 28000,
            210: 28000,
            250: 35000,
            355: 48000,
            360: 50000,
            400: 55000,
            475: 63000,
            545: 75000,
            720: 95000,
        }
        return mapping_ffr.get(ffr_val, None)

    return None
