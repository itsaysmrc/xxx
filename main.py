import os
import sys
import importlib
from typing import Dict, Any

# ANSI Renk Kodları (Termux, iOS a-Shell / iSH ve PC ile tam uyumlu)
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RESET = "\033[0m"

BANNER = f"""{C_CYAN}{C_BOLD}
  _  _____  ____   __          __     _      _  ________ _____  
 | |/ / _ \|  _ \  \ \        / /\   | |    | |/ /  ____|  __ \ 
 | ' / | | | | | |  \ \  /\  / /  \  | |    | ' /| |__  | |__) |
 |  <| | | | | | |   \ \/  \/ / /\ \ | |    |  < |  __| |  _  / 
 | . \ |_| | |_| |    \  /\  / ____ \| |____| . \| |____| | \ \ 
 |_|\_\___/|____/      \/  \/_/    \_\______|_|\_\______|_|  \_\\
{C_RESET}{C_GREEN}          » MODÜLER OSINT & GÜVENLİK SUİTİ «{C_RESET}
"""

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def load_modules() -> Dict[str, Any]:
    """modules/ klasöründeki geçerli tüm araçları otomatik içe aktarır."""
    modules = {}
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")

    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir, exist_ok=True)
        return modules

    for file in sorted(os.listdir(modules_dir)):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            try:
                mod = importlib.import_module(f"modules.{module_name}")
                if hasattr(mod, "META") and hasattr(mod, "run"):
                    modules[module_name] = mod
            except Exception as e:
                print(f"{C_RED}[!] Modül yüklenemedi: {file} -> {e}{C_RESET}")

    return modules

def main():
    while True:
        clear_screen()
        print(BANNER)
        modules = load_modules()

        if not modules:
            print(f"{C_YELLOW}[*] 'modules/' klasöründe geçerli modül bulunamadı.{C_RESET}\n")
            print(" [0] Çıkış")
        else:
            print(f"{C_BOLD}Yüklü Araçlar ({len(modules)} Adet):{C_RESET}")
            mod_keys = list(modules.keys())
            for idx, key in enumerate(mod_keys, 1):
                meta = modules[key].META
                title = meta.get("title", key)
                desc = meta.get("desc", "Açıklama yok")
                print(f" {C_CYAN}[{idx}]{C_RESET} {C_BOLD}{title:<38}{C_RESET} - {C_DIM}{desc}{C_RESET}")

            print(f"\n {C_RED}[0]{C_RESET} Çıkış\n")

        choice = input(f"{C_YELLOW}Seçiminiz > {C_RESET}").strip()

        if choice == "0":
            print(f"\n{C_GREEN}KOD WALKER kapatıldı.{C_RESET}")
            sys.exit(0)

        if choice.isdigit():
            c_idx = int(choice) - 1
            mod_keys = list(modules.keys())
            if 0 <= c_idx < len(mod_keys):
                selected_module = modules[mod_keys[c_idx]]
                clear_screen()
                print(f"{C_CYAN}--- {selected_module.META.get('title', mod_keys[c_idx])} ---{C_RESET}\n")
                try:
                    selected_module.run()
                except KeyboardInterrupt:
                    print(f"\n{C_YELLOW}[!] İşlem durduruldu.{C_RESET}")
                except Exception as e:
                    print(f"\n{C_RED}[!] Hata: {e}{C_RESET}")

                input(f"\n{C_DIM}Menüye dönmek için Enter'a basın...{C_RESET}")
            else:
                input(f"{C_RED}Geçersiz numara. Devam etmek için Enter'a basın...{C_RESET}")

if __name__ == "__main__":
    main()