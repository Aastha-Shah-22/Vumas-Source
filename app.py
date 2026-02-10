import os
import sqlite3
import subprocess
import yaml
import pickle
import hashlib
import jwt
import requests
from flask import Flask, request, make_response, redirect

app = Flask(__name__)

# 1. Hardcoded Sensitive Information
SECRET_KEY = "super-secret-key-12345"
ADMIN_PASSWORD = "password123"

@app.route('/vulnerable-endpoint', methods=['POST'])
def handle_data():
    # 2. Command Injection
    filename = request.form.get("filename")
    os.system(f"rm {filename}") 

    # 3. SQL Injection
    user_id = request.args.get("id")
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}") 

    # 4. Insecure Deserialization (Pickle)
    data = request.form.get("data")
    obj = pickle.loads(data) 

    # 5. Insecure Deserialization (YAML)
    yaml_config = request.form.get("config")
    config = yaml.load(yaml_config) 

    # 6. Path Traversal
    path = request.args.get("path")
    with open(os.path.join("/var/www/uploads", path), "r") as f:
        content = f.read()

    # 7. Use of Weak Hashing Algorithm
    pass_hash = hashlib.md5(ADMIN_PASSWORD.encode()).hexdigest()

    # 8. Broken Access Control (Insecure Direct Object Reference)
    # No authorization check before fetching sensitive profile
    profile = cursor.execute(f"SELECT * FROM profiles WHERE id = {user_id}")

    # 9. Server-Side Request Forgery (SSRF)
    target_url = request.args.get("url")
    requests.get(target_url) 

    # 10. Reflective Cross-Site Scripting (XSS)
    name = request.args.get("name")
    return f"<h1>Welcome {name}</h1>" 

@app.route('/login')
def login():
    # 11. JWT None Algorithm allowed
    token = request.headers.get("Authorization")
    jwt.decode(token, options={"verify_signature": False}) 

    # 12. Sensitive Cookie without HttpOnly/Secure flags
    resp = make_response("Logged in")
    resp.set_cookie('session_id', '12345') 
    
    # 13. Open Redirect
    target = request.args.get("next")
    return redirect(target)

# 14. Binding to all network interfaces (0.0.0.0)
# 15. Debug mode enabled in production context
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 

# --- Non-Flask specific vulnerabilities below ---

# 16. Use of unsafe subprocess shell=True
def run_command(cmd):
    subprocess.Popen(cmd, shell=True) 

# 17. Use of Cryptographically Weak Pseudo-Random Number Generator
import random
def generate_token():
    return random.random() 

# 18. Hardcoded Bind Address for Sockets
import socket
s = socket.socket()
s.bind(('0.0.0.0', 8080)) 

# 19. Missing Certificate Validation (verify=False)
def fetch_internal():
    requests.get("https://internal-api.local", verify=False)

# 20. XML External Entity (XXE) via untrusted input
from lxml import etree
def parse_xml(xml_string):
    parser = etree.XMLParser(resolve_entities=True)
    tree = etree.fromstring(xml_string, parser)
