import concurrent.futures
import requests

META = {
    "title": "Kullanıcı Adı İstihbaratı (Tookie-OSINT)",
    "desc": "Sosyal ağlar ve servislerde kullanıcı adı ayak izi varlık taraması."
}

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Twitter (X)": "https://x.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Telegram": "https://t.me/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Steam": "https://steamcommunity.com/id/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "GitLab": "https://gitlab.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Vimeo": "https://vimeo.com/{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_site(platform, url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=6, allow_redirects=True)
        if r.status_code == 200 and url in r.url:
            return platform, url, True
        return platform, url, False
    except Exception:
        return platform, url, None

def run():
    username = input(f"{C_YELLOW}Hedef Kullanıcı Adı: {C_RESET}").strip()
    if not username:
        print("[-] Hata: Kullanıcı adı boş bırakılamaz.")
        return

    print(f"\n{C_CYAN}[*] '{username}' hedefi {len(PLATFORMS)} platformda taranıyor...{C_RESET}\n")

    found_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(check_site, platform, template.format(username)): platform 
            for platform, template in PLATFORMS.items()
        }
        for future in concurrent.futures.as_completed(futures):
            platform, url, exists = future.result()
            if exists is True:
                print(f" {C_GREEN}[+]{C_RESET} {C_BOLD}{platform:<16}{C_RESET} : {url}")
                found_count += 1

    print(f"\n{C_GREEN}[+] Tarama tamamlandı. Toplam {found_count} platformda profil bulundu.{C_RESET}")