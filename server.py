from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, os, time

app = Flask(__name__)
CORS(app)

ALLOWED = {
    "nmap": 120, "masscan": 60, "ping": 30, "whois": 30, "dig": 20,
    "curl": 30, "hydra": 300, "john": 300, "sqlmap": 180, "nikto": 180,
    "dirb": 120, "gobuster": 120, "bash": 30, "python3": 60,
    "echo": 5, "ls": 5, "cat": 5, "git": 60, "wget": 120,
    "pip": 120, "pip3": 120, "apt": 300, "apt-get": 300,
    "netstat": 15, "ss": 15, "ip": 15, "ifconfig": 15, "traceroute": 60,
    "ssh": 60, "nc": 60, "netcat": 60, "tcpdump": 60,
}

@app.route('/')
def index():
    return jsonify({"status": "💀 Eliot's Mask Server Running", "tools": len(ALLOWED)})

@app.route('/api/execute', methods=['POST'])
def execute():
    data = request.json
    if not data or 'command' not in data:
        return jsonify({"error": "Missing command", "output": ""}), 400
    
    command = data['command'].strip()
    base = command.split()[0] if command else ""
    
    if base not in ALLOWED:
        return jsonify({"error": f"'{base}' not allowed", "output": ""}), 403
    
    timeout = data.get('timeout', ALLOWED.get(base, 60))
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        output = (result.stdout or "") + (result.stderr or "")
        return jsonify({"output": output[:8000], "success": result.returncode == 0})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out", "output": ""}), 408
    except Exception as e:
        return jsonify({"error": str(e), "output": ""}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
