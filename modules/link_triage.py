import requests

META = {
    "title": "Şüpheli Link & Yönlendirme Analizi",
    "desc": "Kısaltılmış/gizlenmiş URL zincirini takip eder, hedef adresi açığa çıkarır."
}

def run():
    target = input("İncelenecek URL: ").strip()
    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    print(f"\n[*] Bağlantı taranıyor: {target}")
    try:
        r = requests.get(target, timeout=8, allow_redirects=True, headers={"User-Agent": "KodWalker/1.0"})
        if r.history:
            print("\n[+] Yönlendirme Adımları:")
            for step in r.history:
                print(f"    {step.status_code} -> {step.url}")

        print(f"\n[+] Nihai Hedef Adres : \033[92m{r.url}\033[0m")
        print(f"[+] HTTP Yanıt Kodu   : {r.status_code}")

        # Basit risk kelime denetimi
        risk_flags = [kw for kw in ["login", "verify", "account", "bank", "free", "gift", "apk"] if kw in r.url.lower()]
        if risk_flags:
            print(f"\033[91m[!] UYARI: Nihai adreste şüpheli anahtar kelimeler bulundu: {', '.join(risk_flags)}\033[0m")
    except Exception as e:
        print(f"[-] Hata: {e}")