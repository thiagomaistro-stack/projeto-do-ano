from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/dns")
def dns():
    return render_template("dns.html")

@app.route("/ip-local")
def ip_local_page():
    return render_template("ip_local.html")

@app.route("/firewall")
def firewall():
    return render_template("firewall.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():
    return render_template("login.html")

# APIs

@app.route("/api/dns")
def api_dns():
    site = request.args.get("site")
    ip = socket.gethostbyname(site)
    return jsonify({"site": site, "ip": ip})

@app.route("/api/ip-local")
def api_ip_local():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return jsonify({"hostname": hostname, "ip": ip})

if __name__ == "__main__":
    app.run(debug=True)