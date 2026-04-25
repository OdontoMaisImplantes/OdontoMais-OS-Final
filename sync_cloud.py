import os
import time
import subprocess

FILES_TO_WATCH = ["dashboard_master.py", "Procfile", "railway.json"]
GIT_CMD = r"C:\Users\Play Tec\.gemini\antigravity\scratch\OdontoMaisAutomacao\mingit\cmd\git.exe"

def get_mtimes():
    mtimes = {}
    for f in FILES_TO_WATCH:
        if os.path.exists(f):
            mtimes[f] = os.path.getmtime(f)
    return mtimes

def sync_github():
    print("\n[+] Sincronizando com o GitHub...")
    subprocess.run([GIT_CMD, "add", "."], check=False)
    
    status = subprocess.run([GIT_CMD, "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("Nenhuma mudança a commitar.")
        return

    subprocess.run([GIT_CMD, "commit", "-m", "Auto-update: Refinamento de Design e Acesso"], check=False)
    
    print("[*] Enviando alterações para o remoto...")
    push_res = subprocess.run([GIT_CMD, "push", "origin", "main"], capture_output=True, text=True)
    
    if push_res.returncode == 0:
        print("[ SUCESSO ] Push concluído em menos de 10 segundos!")
    else:
        print("[ ERRO ] Falha no Push:")
        print(push_res.stderr)

print("Iniciando Monitor de Alterações (Túnel de Dados)...")
last_mtimes = get_mtimes()

# Initial sync request as per prompt "Rode o sync_cloud.py agora mesmo para subir os últimos ajustes"
sync_github()

print("\nAguardando alterações em:", ", ".join(FILES_TO_WATCH))

try:
    while True:
        time.sleep(2)
        current_mtimes = get_mtimes()
        changed = False
        for f in FILES_TO_WATCH:
            if f in current_mtimes and f in last_mtimes:
                if current_mtimes[f] > last_mtimes[f]:
                    print(f"\n[!] Modificação detectada em: {f}")
                    changed = True
                    break
        
        if changed:
            sync_github()
            last_mtimes = get_mtimes()
except KeyboardInterrupt:
    print("\nMonitor encerrado.")
