import phonenumbers
from phonenumbers import geocoder, carrier

META = {
    "title": "Telefon Numarası Doğrulama",
    "desc": "Uluslararası format denetimi, hat türü ve operatör tespiti."
}

def run():
    num = input("Telefon Numarası (Örn: 05xxxxxxxxx veya +905xxxxxxxxx): ").strip()
    try:
        p = phonenumbers.parse(num, "TR")
        is_valid = phonenumbers.is_valid_number(p)
        print("\n[+] Analiz Sonuçları:")
        print(f"    E.164 Formatı : {phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"    Geçerlilik    : {'\033[92mGEÇERLİ\033[0m' if is_valid else '\033[91mGEÇERSİZ\033[0m'}")
        print(f"    Bölge/Ülke    : {geocoder.description_for_number(p, 'tr') or 'Bilinmiyor'}")
        print(f"    Operatör      : {carrier.name_for_number(p, 'tr') or 'Bilinmiyor'}")
    except Exception as e:
        print(f"[-] Hata: {e}")