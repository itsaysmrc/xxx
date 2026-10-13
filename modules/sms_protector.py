import re

META = {
    "title": "SMS & Çağrı Tehdit Teşhisi (Protector)",
    "desc": "Şüpheli SMS metinlerini, tuzak bağlantıları ve oltalama kalıplarını puanlar."
}

def run():
    print("Şüpheli SMS / Mesaj Analiz Paneli")
    sender = input("Gönderen Numara / Başlık (Örn: 05xxxxxxxxx veya B002) [Boş geçilebilir]: ").strip()
    message = input("Gelen Mesaj Metni: ").strip()

    if not message:
        print("[-] Hata: İncelenecek mesaj metni girmelisiniz.")
        return

    risk_score = 0
    warnings = []

    # 1. URL / Link Tespiti
    url_pattern = r"(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[^\s]*)"
    extracted_urls = re.findall(url_pattern, message)
    if extracted_urls:
        risk_score += 35
        warnings.append(f"Mesajda {len(extracted_urls)} web bağlantısı bulundu: {', '.join(extracted_urls)}")

    # 2. Oltalama Kalıpları
    threat_patterns = {
        "Kargo / Paket Tuzağı": ["kargo", "teslim edilemedi", "adresinizi guncelleyin", "paketiniz", "ptt", "yurtici"],
        "Finans / Banka Oltalama": ["hesabiniz", "askiya", "kart aidati", "hesap ozeti", "iade talebi", "sifreniz"],
        "Sahte İcra / Ceza Tehdidi": ["hukuk burosu", "icra takibi", "ceza dosyaniz", "adli makam", "uzlasma"],
        "Yasadışı Bahis / Hediye": ["bonus", "kazandiniz", "ucretsiz kupon", "deneme bonusu", "freespin"]
    }

    text_lower = message.lower()
    for cat, words in threat_patterns.items():
        matched = [w for w in words if w in text_lower]
        if matched:
            risk_score += 25
            warnings.append(f"Oltalama Kalıbı [{cat}]: '{matched[0]}'")

    # 3. Yasal BTK Operatör Kodu Denetimi (B001, B002 vb.)
    has_b_code = bool(re.search(r"B\d{3}", message))
    if not has_b_code and (extracted_urls or risk_score > 0):
        risk_score += 20
        warnings.append("Mesajda BTK yasal operatör kodu (Bxxx) bulunmuyor (Yetkisiz Başlık).")

    risk_score = min(risk_score, 100)

    print("\n" + "="*45)
    print("         GÜVENLİK TEŞHİS RAPORU")
    print("="*45)

    if risk_score >= 60:
        level_str = "\033[91mKRİTİK TEHDİT / YÜKSEK İHTİMALLİ OLTALAMA\033[0m"
    elif risk_score >= 30:
        level_str = "\033[93mORTA DÜZEY ŞÜPHELİ RİSK\033[0m"
    else:
        level_str = "\033[92mDÜŞÜK RİSK / GÜVENLİ GÖRÜNÜYOR\033[0m"

    print(f"Risk Skoru      : %{risk_score}")
    print(f"Tehdit Durumu   : {level_str}")
    print("\nBulgular:")
    for w in warnings:
        print(f" [!] {w}")
    if not warnings:
        print(" [+] Belirgin bir tehdit veya dolandırıcılık kalıbına rastlanmadı.")
    print("="*45)