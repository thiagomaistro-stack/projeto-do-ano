import nmap
import socket
import os

# Altere aqui para a rede da sua casa (ex: "192.168.0.0/24" ou "192.168.1.0/24")
REDE_CASA = "192.168.0.0/24" 

def escaneamento_profundo(rede):
    os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"

    nm = nmap.PortScanner()
    
    print(f"Iniciando varredura profunda na rede: {rede}")
    print("Isso pode levar de 10 a 30 segundos...\n")
    nm.scan(hosts=rede, arguments='-sn')
    
    print(f"{'Endereço IP':<16} | {'Status':<8} | {'Nome/Fabricante':<30}")
    print("-" * 60)
    
    for host in nm.all_hosts():
        status = nm[host].state()
        nome_dispositivo = nm[host].hostname() if nm[host].hostname() else "Desconhecido"
        print(f"{host:<16} | {status:<8} | {nome_dispositivo:<30}")

if __name__ == "__main__":
    escaneamento_profundo(REDE_CASA)


