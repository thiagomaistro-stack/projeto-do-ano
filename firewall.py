from scapy.all import *

# Regra: Adicione aqui o IP que você deseja bloquear
IP_BLOQUEADO = "192.168.0.4"

def analisar_pacote(pacote):
    # Verifica se o pacote tem a camada de IP
    if pacote.haslayer(IP):
        ip_origem = pacote[IP].src
        ip_destino = pacote[IP].dst

        # Se o pacote envolver o IP bloqueado
        if ip_origem == IP_BLOQUEADO or ip_destino == IP_BLOQUEADO:
            print(f"[!] TRÁFEGO DETECTADO: {ip_origem} -> {ip_destino}")
            
            # Se for uma conexão TCP, nós forçamos a queda dela enviando um Reset (RST)
            if pacote.haslayer(TCP):
                print(f"[X] Bloqueando e derrubando conexão TCP...")
                
                # Cria um pacote de corte de conexão
                pacote_rst = IP(src=pacote[IP].dst, dst=pacote[IP].src) / \
                             TCP(sport=pacote[TCP].dport, dport=pacote[TCP].sport, 
                                 flags="R", seq=pacote[TCP].ack)
                
                # Envia o bloqueio para a rede
                send(pacote_rst, verbose=False)

print("[*] Iniciando Firewall com Scapy (Windows)...")
print(f"[*] Monitorando e bloqueando tráfego de/para: {IP_BLOQUEADO}")
print("[*] Pressione Ctrl+C para encerrar.\n")

try:
    # Captura os pacotes continuamente na placa de rede
    sniff(prn=analisar_pacote, store=0)
except KeyboardInterrupt:
    print("\n[*] Desligando o firewall...")
