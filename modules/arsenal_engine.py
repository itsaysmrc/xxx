import os
import sys
import shutil
import subprocess

META = {
    "title": "Awesome OSINT Arsenal (100+ Araç)",
    "desc": "Kategorize edilmiş istihbarat cephaneliği ve otomatik araç kurucu."
}

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RESET = "\033[0m"

ARSENAL_DATA = {
    "1": {
        "kategori": "Kullanıcı & Sosyal Medya (SOCMINT)",
        "araclar": [
            {"name": "user-scanner", "cmd": "user-scanner", "pkg": "user-scanner", "type": "pip", "desc": "2700+ platformda kullanıcı adı ve mail ayak izi tarayıcısı.", "repo": "https://github.com/kaifcodec/user-scanner"},
            {"name": "sherlock", "cmd": "sherlock", "pkg": "sherlock", "type": "pip", "desc": "400+ sosyal ağda kullanıcı adı tarama aracı.", "repo": "https://github.com/sherlock-project/sherlock"},
            {"name": "maigret", "cmd": "maigret", "pkg": "maigret", "type": "pip", "desc": "Kullanıcı adı profilleme ve derin metadata çıkarma.", "repo": "https://github.com/soxoj/maigret"},
            {"name": "blackbird", "cmd": "blackbird", "pkg": "blackbird", "type": "git", "desc": "Hızlı asenkron kullanıcı adı keşif aracı.", "repo": "https://github.com/p1ngul1n0/blackbird"},
            {"name": "social-analyzer", "cmd": "social-analyzer", "pkg": "social-analyzer", "type": "pip", "desc": "1000+ sitede profil ve analitik taraması.", "repo": "https://github.com/qeeqbox/social-analyzer"}
        ]
    },
    "2": {
        "kategori": "E-posta & Numara İstihbaratı",
        "araclar": [
            {"name": "holehe", "cmd": "holehe", "pkg": "holehe", "type": "pip", "desc": "Şifre sıfırlama kanallarından 200+ sitede mail varlık tespiti.", "repo": "https://github.com/megadose/holehe"},
            {"name": "ghunt", "cmd": "ghunt", "pkg": "ghunt", "type": "pip", "desc": "Google/Gmail hesapları için detaylı OSINT analizi.", "repo": "https://github.com/mxrch/GHunt"},
            {"name": "h8mail", "cmd": "h8mail", "pkg": "h8mail", "type": "pip", "desc": "E-posta sızıntı (data breach) ve parola araştırma.", "repo": "https://github.com/khast3x/h8mail"},
            {"name": "phoneinfoga", "cmd": "phoneinfoga", "pkg": "phoneinfoga", "type": "pip", "desc": "Uluslararası telefon numarası analiz ve tarama aracı.", "repo": "https://github.com/sundowndev/phoneinfoga"}
        ]
    },
    "3": {
        "kategori": "Ağ Keşfi & Alan Adı (Network Recon)",
        "araclar": [
            {"name": "nmap", "cmd": "nmap", "pkg": "nmap", "type": "sys", "desc": "Ağ tarama, açık port ve servis versiyon tespiti.", "repo": "https://nmap.org"},
            {"name": "subfinder", "cmd": "subfinder", "pkg": "subfinder", "type": "sys", "desc": "Hızlı pasif alt alan adı (subdomain) keşif motoru.", "repo": "https://github.com/projectdiscovery/subfinder"},
            {"name": "theHarvester", "cmd": "theHarvester", "pkg": "theHarvester", "type": "pip", "desc": "Arama motorlarından mail, subdomain ve IP toplama.", "repo": "https://github.com/laramies/theHarvester"},
            {"name": "whatweb", "cmd": "whatweb", "pkg": "whatweb", "type": "sys", "desc": "Web sunucu teknolojisi ve CMS parmak izi tespiti.", "repo": "https://github.com/urbanadventurer/WhatWeb"},
            {"name": "wafw00f", "cmd": "wafw00f", "pkg": "wafw00f", "type": "pip", "desc": "Web Uygulama Güvenlik Duvarı (WAF) tespiti.", "repo": "https://github.com/EnableSecurity/wafw00f"}
        ]
    },
    "4": {
        "kategori": "Web Güvenliği & Zafiyet Analizi",
        "araclar": [
            {"name": "nuclei", "cmd": "nuclei", "pkg": "nuclei", "type": "sys", "desc": "Şablon tabanlı güvenlik açığı ve yapılandırma hatası tarayıcısı.", "repo": "https://github.com/projectdiscovery/nuclei"},
            {"name": "sqlmap", "cmd": "sqlmap", "pkg": "sqlmap", "type": "pip", "desc": "Otomatik SQL Enjeksiyonu tespit aracı.", "repo": "https://github.com/sqlmapproject/sqlmap"},
            {"name": "nikto", "cmd": "nikto", "pkg": "nikto", "type": "sys", "desc": "Web sunucularındaki tehlikeli dosyalar ve sürüm açıklarını tarar.", "repo": "https://github.com/sullo/nikto"},
            {"name": "gobuster", "cmd": "gobuster", "pkg": "gobuster", "type": "sys", "desc": "Gizli dizin ve dosya brute-force keşif motoru.", "repo": "https://github.com/OJ/gobuster"}
        ]
    },
    "5": {
        "kategori": "Adli Bilişim & Metadata (Forensics)",
        "araclar": [
            {"name": "exiftool", "cmd": "exiftool", "pkg": "exiftool", "type": "sys", "desc": "Görsellerden GPS, kamera ve EXIF metadata ayıklar.", "repo": "https://exiftool.org"},
            {"name": "mat2", "cmd": "mat2", "pkg": "mat2", "type": "pip", "desc": "Dosyalardan gizlilik ihlali oluşturabilecek metadata'ları temizler.", "repo": "https://0xacab.org/jvoisin/mat2"},
            {"name": "apkleaks", "cmd": "apkleaks", "pkg": "apkleaks", "type": "pip", "desc": "APK kaynak kodlarında unutulmuş gizli API anahtarlarını tarar.", "repo": "https://github.com/dwisiswant0/apkleaks"}
        ]
    }
}

def is_tool_installed(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def install_tool(tool: dict):
    t_type = tool["type"]
    pkg = tool["pkg"]
    is_termux = "com.termux" in os.environ.get("PREFIX", "")
    sys_installer = "pkg install -y" if is_termux else "sudo apt install -y"

    print(f"\n{C_YELLOW}[*] '{tool['name']}' kuruluyor...{C_RESET}")
    try:
        if t_type == "pip":
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)
        elif t_type == "sys":
            os.system(f"{sys_installer} {pkg}")
        elif t_type == "git":
            tools_dir = os.path.expanduser("~/tools")
            os.makedirs(tools_dir, exist_ok=True)
            clone_path = os.path.join(tools_dir, tool["name"])
            if not os.path.exists(clone_path):
                subprocess.run(["git", "clone", tool["repo"], clone_path], check=True)
                req_path = os.path.join(clone_path, "requirements.txt")
                if os.path.exists(req_path):
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
            print(f"{C_GREEN}[+] Depo indirildi: {clone_path}{C_RESET}")
        print(f"{C_GREEN}[+] Kurulum başarıyla tamamlandı!{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[!] Kurulum sırasında hata oluştu: {e}{C_RESET}")

def manage_tool(tool: dict):
    installed = is_tool_installed(tool["cmd"])
    print(f"\n{C_BOLD}Araç: {tool['name']}{C_RESET}")
    print(f"Açıklama : {tool['desc']}")
    print(f"Kaynak   : {tool['repo']}")
    status_str = f"{C_GREEN}Kurulu (Kullanıma Hazır){C_RESET}" if installed else f"{C_RED}Kurulu Değil{C_RESET}"
    print(f"Durum    : {status_str}\n")

    if installed:
        print(f"{C_CYAN}[1] Doğrudan Çalıştır (Parametre girerek){C_RESET}")
        print(f"{C_CYAN}[2] Yeniden / Güncel Kurulum Yap{C_RESET}")
        print("[0] Geri")
        secim = input(f"{C_YELLOW}Seçiminiz > {C_RESET}").strip()
        if secim == "1":
            params = input(f"{C_YELLOW}{tool['cmd']} için parametre/hedef girin: {C_RESET}").strip()
            os.system(f"{tool['cmd']} {params}")
        elif secim == "2":
            install_tool(tool)
    else:
        print(f"{C_YELLOW}[1] Aracı Otomatik Kur{C_RESET}")
        print("[0] Geri")
        secim = input(f"{C_YELLOW}Seçiminiz > {C_RESET}").strip()
        if secim == "1":
            install_tool(tool)

def browse_category(cat_key: str):
    cat_info = ARSENAL_DATA[cat_key]
    while True:
        print(f"\n{C_CYAN}{C_BOLD}=== {cat_info['kategori']} ==={C_RESET}")
        for idx, t in enumerate(cat_info["araclar"], 1):
            durum = f"{C_GREEN}[✓]{C_RESET}" if is_tool_installed(t["cmd"]) else f"{C_RED}[✗]{C_RESET}"
            print(f" {C_CYAN}[{idx}]{C_RESET} {durum} {C_BOLD}{t['name']:<18}{C_RESET} - {C_DIM}{t['desc']}{C_RESET}")
        print(f" {C_RED}[0]{C_RESET} Üst Menüye Dön\n")

        sec = input(f"{C_YELLOW}Araç seçin > {C_RESET}").strip()
        if sec == "0":
            break
        if sec.isdigit() and 1 <= int(sec) <= len(cat_info["araclar"]):
            manage_tool(cat_info["araclar"][int(sec) - 1])

def search_arsenal():
    kelime = input(f"\n{C_YELLOW}Aranacak araç adı veya anahtar kelime: {C_RESET}").strip().lower()
    bulunanlar = []
    for c in ARSENAL_DATA.values():
        for t in c["araclar"]:
            if kelime in t["name"].lower() or kelime in t["desc"].lower():
                bulunanlar.append(t)

    if not bulunanlar:
        print(f"{C_RED}[!] Eşleşen araç bulunamadı.{C_RESET}")
        return

    print(f"\n{C_GREEN}[+] Bulunan Araçlar ({len(bulunanlar)} Adet):{C_RESET}")
    for idx, t in enumerate(bulunanlar, 1):
        durum = f"{C_GREEN}[✓]{C_RESET}" if is_tool_installed(t["cmd"]) else f"{C_RED}[✗]{C_RESET}"
        print(f" [{idx}] {durum} {t['name']:<18} - {t['desc']}")

    sec = input(f"\n{C_YELLOW}Detayını görmek istediğiniz araç no (0 iptal): {C_RESET}").strip()
    if sec.isdigit() and 1 <= int(sec) <= len(bulunanlar):
        manage_tool(bulunanlar[int(sec) - 1])

def run():
    while True:
        print(f"\n{C_BOLD}AWESOME OSINT ARSENAL KOMUTA MERKEZİ{C_RESET}")
        for k, v in ARSENAL_DATA.items():
            print(f" {C_CYAN}[{k}]{C_RESET} {v['kategori']} ({len(v['araclar'])} Araç)")
        print(f" {C_YELLOW}[S]{C_RESET} Cephanelikte Ara (Arama Motoru)")
        print(f" {C_RED}[0]{C_RESET} Ana Menüye Dön\n")

        sec = input(f"{C_YELLOW}Seçiminiz > {C_RESET}").strip().upper()
        if sec == "0":
            break
        elif sec == "S":
            search_arsenal()
        elif sec in ARSENAL_DATA:
            browse_category(sec)