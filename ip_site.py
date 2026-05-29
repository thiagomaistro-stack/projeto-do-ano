def ip_site():
    import socket

    site = input("digite o nome do site (ex: www.anvi.com.br):")
    ip_site = socket.gethostbyname(site)

    print(f"O IP do {site} é: {ip_site}")

ip_site()
