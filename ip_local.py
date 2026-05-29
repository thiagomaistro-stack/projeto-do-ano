def ip_local():
    import socket

    # Obtém o nome da máquina
    hostname = socket.gethostname()
    # Traduz o nome da máquina para o endereço IP local
    ip_local = socket.gethostbyname(hostname)

    print(f"Nome do Host: {hostname}")
    print(f"IP Local: {ip_local}")
ip_local()
