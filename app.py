# app.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardcoded secret (Trivy/Gitleaks should find this)
DATABASE_PASSWORD = "insecure_admin_password_123"

# Vulnerable endpoint: Cross-Site Scripting (XSS)
@app.route('/greet', methods=['GET'])
def greet():
    # User input is taken directly from URL parameter
    user_name = request.args.get('name', 'Guest')
    
    # This directly embeds user_name into HTML, making it vulnerable to XSS
    # Payload example: ?name=<script>alert('XSSed!')</script>
    html_content = f"<h1>Hello, {user_name}!</h1><p>Welcome to the insecure page.</p>"
    
    return render_template_string(html_content)

@app.route('/')
def home():
    return '<h1>DevSecOps Demo Home</h1><p>Try /greet?name=World</p>'

if __name__ == '__main__':
    # Running on an open port in a container
    app.run(host='0.0.0.0', port=8080)
