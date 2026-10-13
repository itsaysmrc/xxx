import requests

META = {
    "title": "IP & Domain Coğrafi İstihbarat",
    "desc": "IP adresi veya alan adının sunucu konumu, ISP ve ASN bilgilerini sorgular."
}

def run():
    target = input("Hedef IP veya Domain (Örn: 8.8.8.8 veya site.com): ").strip()
    target = target.replace("https://", "").replace("http://", "").split("/")[0]

    print(f"\n[*] İstihbarat çekiliyor: {target}")
    try:
        res = requests.get(f"http://ip-api.com/json/{target}?fields=status,message,country,city,isp,as,query", timeout=6).json()
        if res.get("status") == "success":
            print(f"\n[+] IP Adresi  : \033[92m{res.get('query')}\033[0m")
            print(f"[+] Konum      : {res.get('country')} / {res.get('city')}")
            print(f"[+] ISP        : {res.get('isp')}")
            print(f"[+] ASN        : {res.get('as')}")
        else:
            print(f"[-] Başarısız: {res.get('message')}")
    except Exception as e:
        print(f"[-] Hata: {e}")