import phonenumbers
from phonenumbers import geocoder, carrier, number_type

META = {
    "title": "PhoneInfoga Motoru (Numara OSINT)",
    "desc": "Gelişmiş telefon numarası istihbarat, hat türü ve operatör keşfi."
}

def run():
    num = input("Hedef Telefon Numarası (Örn: +905321234567): ").strip()
    if not num:
        print("[-] Hata: Numara boş bırakılamaz.")
        return

    try:
        p = phonenumbers.parse(num, None)
        is_valid = phonenumbers.is_valid_number(p)
        
        print("\n" + "="*50)
        print("           PHONEINFOGA RECON RAPORU")
        print("="*50)
        print(f" Uluslararası Format : {phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f" E.164 Formatı       : {phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)}")
        print(f" Ülke Kodu           : +{p.country_code}")
        print(f" Ulusal Numara       : {p.national_number}")
        print(f" Geçerlilik          : {'\033[92mGEÇERLİ\033[0m' if is_valid else '\033[91mGEÇERSİZ\033[0m'}")
        print(f" Coğrafi Bölge       : {geocoder.description_for_number(p, 'tr') or 'Bilinmiyor'}")
        print(f" Operatör / Taşıyıcı : {carrier.name_for_number(p, 'tr') or 'Bilinmiyor'}")
        
        # Hat Türü Tespiti
        n_type = number_type(p)
        types_map = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobil / Hücresel",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Sabit Hat (Ev / İş)",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Sabit veya Mobil",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Ücretsiz Hat (800 vb.)",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Katma Değerli / Ücretli Hat",
            phonenumbers.PhoneNumberType.VOIP: "VoIP (İnternet Üzerinden Ses)"
        }
        print(f" Hat Türü            : {types_map.get(n_type, 'Bilinmiyor / Diğer')}")
        print("="*50)
    except Exception as e:
        print(f"[-] Hata: {e}")