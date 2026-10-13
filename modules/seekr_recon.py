import requests

META = {
    "title": "Seekr OSINT Motoru (GitHub Deep Recon)",
    "desc": "Derin GitHub analizi, gizli commit e-postaları ve açık anahtar keşfi."
}

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RESET = "\033[0m"

HEADERS = {
    "User-Agent": "KodWalker-Seekr/1.0",
    "Accept": "application/vnd.github.v3+json"
}

def run():
    target = input(f"{C_YELLOW}Hedef GitHub Kullanıcı Adı: {C_RESET}").strip()
    if not target:
        print(f"{C_RED}[-] Hata: Kullanıcı adı boş bırakılamaz.{C_RESET}")
        return

    print(f"\n{C_CYAN}[*] '{target}' için Seekr Derin Keşif Motoru başlatılıyor...{C_RESET}")

    # 1. Profil Bilgisi
    try:
        r = requests.get(f"https://api.github.com/users/{target}", headers=HEADERS, timeout=8)
        if r.status_code == 404:
            print(f"{C_RED}[-] Hata: '{target}' adlı GitHub kullanıcısı bulunamadı.{C_RESET}")
            return
        elif r.status_code != 200:
            print(f"{C_RED}[-] GitHub API Hatası (HTTP {r.status_code}){C_RESET}")
            return
        p = r.json()
    except Exception as e:
        print(f"{C_RED}[-] Bağlantı hatası: {e}{C_RESET}")
        return

    print(f"\n{C_BOLD}{'='*50}{C_RESET}")
    print(f"{C_GREEN}{C_BOLD}           SEEKR İSTİHBARAT RAPORU{C_RESET}")
    print(f"{C_BOLD}{'='*50}{C_RESET}")

    print(f" {C_BOLD}Kullanıcı Adı  :{C_RESET} {p.get('login', '-')}")
    print(f" {C_BOLD}Görünen İsim   :{C_RESET} {p.get('name') or 'Belirtilmemiş'}")
    print(f" {C_BOLD}Bio / Durum    :{C_RESET} {p.get('bio') or 'Yok'}")
    print(f" {C_BOLD}Şirket/Kurum   :{C_RESET} {p.get('company') or 'Belirtilmemiş'}")
    print(f" {C_BOLD}Konum Bilgisi  :{C_RESET} {p.get('location') or 'Belirtilmemiş'}")
    print(f" {C_BOLD}Web Sitesi/Blog:{C_RESET} {p.get('blog') or 'Yok'}")
    print(f" {C_BOLD}Twitter/X      :{C_RESET} {p.get('twitter_username') or 'Yok'}")
    print(f" {C_BOLD}Hesap Açılış   :{C_RESET} {p.get('created_at', '-')[:10]}")
    print(f" {C_BOLD}Açık Repolar   :{C_RESET} {p.get('public_repos', 0)} Adet")
    print(f" {C_BOLD}Takipçi Sayısı :{C_RESET} {p.get('followers', 0)}")

    # 2. Anahtar Durumu
    ssh_c, gpg_c = 0, 0
    try:
        r_ssh = requests.get(f"https://api.github.com/users/{target}/keys", headers=HEADERS, timeout=6)
        if r_ssh.status_code == 200:
            ssh_c = len(r_ssh.json())
        r_gpg = requests.get(f"https://api.github.com/users/{target}/gpg_keys", headers=HEADERS, timeout=6)
        if r_gpg.status_code == 200:
            gpg_c = len(r_gpg.json())
    except Exception:
        pass

    print(f"\n{C_CYAN}[*] Kriptografik Anahtar Durumu:{C_RESET}")
    print(f"  • Kamuya Açık SSH Anahtarları : {ssh_c} Adet")
    print(f"  • Doğrulanmış GPG Anahtarları : {gpg_c} Adet")

    # 3. Commit E-posta Avı
    print(f"\n{C_CYAN}[*] PushEvent & Commit Logları Taranıyor...{C_RESET}")
    found_emails = set()
    try:
        r_events = requests.get(f"https://api.github.com/users/{target}/events/public", headers=HEADERS, timeout=10)
        if r_events.status_code == 200:
            for event in r_events.json():
                if event.get("type") == "PushEvent":
                    for c in event.get("payload", {}).get("commits", []):
                        author = c.get("author", {})
                        email = author.get("email", "")
                        name = author.get("name", "")
                        if email and not email.endswith("noreply.github.com"):
                            found_emails.add((name, email))
    except Exception:
        pass

    if found_emails:
        print(f"\n{C_GREEN}{C_BOLD}[+] Tespit Edilen Gerçek Geliştirici E-postaları ({len(found_emails)} Adet):{C_RESET}")
        for name, email in found_emails:
            print(f"  {C_GREEN}✓{C_RESET} {C_BOLD}{name:<20}{C_RESET} -> {C_CYAN}{email}{C_RESET}")
    else:
        profile_email = p.get('email')
        if profile_email:
            print(f"\n{C_GREEN}[+] Profilde Tanımlı E-posta: {profile_email}{C_RESET}")
        else:
            print(f"\n{C_DIM}[-] Son commit loglarında sızmış kamuya açık e-posta bulunamadı.{C_RESET}")

    print(f"\n{C_BOLD}{'='*50}{C_RESET}")