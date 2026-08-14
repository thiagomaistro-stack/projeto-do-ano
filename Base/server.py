import http.server
import socket
import ipaddress
import subprocess
import platform
import json
import concurrent.futures
import os
import urllib.parse


PORT = 8000
PUBLIC = os.path.join(os.path.dirname(__file__), "public")


def get_local_network():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    network = ipaddress.ip_network(
        local_ip + "/24",
        strict=False
    )

    if not network.is_private:
        raise RuntimeError("A rede detectada não é uma rede privada.")

    return local_ip, network


def ping(ip):

    system = platform.system().lower()

    if system == "windows":

        command = [
            "ping",
            "-n",
            "1",
            "-w",
            "500",
            str(ip)
        ]

    else:

        command = [
            "ping",
            "-c",
            "1",
            "-W",
            "1",
            str(ip)
        ]

    try:

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )

        return result.returncode == 0

    except Exception:

        return False


def get_hostname(ip):

    try:
        return socket.gethostbyaddr(str(ip))[0]

    except Exception:
        return ""


def scan_network():

    local_ip, network = get_local_network()

    hosts = list(network.hosts())

    found = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=64
    ) as executor:

        results = executor.map(ping, hosts)

        for ip, online in zip(hosts, results):

            if online:

                found.append({
                    "ip": str(ip),
                    "hostname": get_hostname(ip),
                    "local": str(ip) == local_ip
                })

    return {
        "local_ip": local_ip,
        "network": str(network),
        "devices": found
    }


def lookup_domain(domain):

    domain = domain.strip()

    if domain.startswith("http://"):

        domain = urllib.parse.urlparse(domain).hostname

    elif domain.startswith("https://"):

        domain = urllib.parse.urlparse(domain).hostname

    if not domain:
        raise ValueError("Domínio inválido.")

    ipv4 = []
    ipv6 = []

    try:

        ipv4 = socket.gethostbyname_ex(domain)[2]

    except Exception:
        pass

    try:

        results = socket.getaddrinfo(
            domain,
            None,
            socket.AF_INET6
        )

        ipv6 = sorted({
            item[4][0]
            for item in results
        })

    except Exception:
        pass

    if not ipv4 and not ipv6:

        raise ValueError(
            "Não foi possível encontrar IPs para esse domínio."
        )

    return {
        "hostname": domain,
        "ipv4": ipv4,
        "ipv6": ipv6
    }


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            directory=PUBLIC,
            **kwargs
        )


    def send_json(self, data, status=200):

        output = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(output))
        )

        self.end_headers()

        self.wfile.write(output)


    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)


        # -------------------------
        # IP DO SITE
        # -------------------------

        if parsed.path == "/api/lookup":

            params = urllib.parse.parse_qs(
                parsed.query
            )

            domain = params.get(
                "url",
                [""]
            )[0]

            try:

                result = lookup_domain(domain)

                self.send_json(result)

            except Exception as e:

                self.send_json(
                    {"error": str(e)},
                    400
                )

            return


        # -------------------------
        # SCANNER DE REDE
        # -------------------------

        if parsed.path == "/api/scan":

            try:

                result = scan_network()

                self.send_json(result)

            except Exception as e:

                self.send_json(
                    {"error": str(e)},
                    500
                )

            return


        super().do_GET()


server = http.server.ThreadingHTTPServer(
    ("localhost", PORT),
    Handler
)


print()
print("==============================")
print("        MEU PAINEL")
print("==============================")
print()
print(f"http://localhost:{PORT}")
print()
print("CTRL+C para encerrar.")
print()


server.serve_forever()