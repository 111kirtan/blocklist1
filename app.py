from flask import Flask, request, jsonify

app = Flask(__name__)

# Zoom API credentials
ZOOM_API_KEY = "j2BoDzHJQaClLZPTxKB6gQ"
ZOOM_API_SECRET = "zVn7zs3Odyt2K59jo9TwlGPPhNkGDvpa"

# Load the blocklist
def load_blocklist():
    try:
        with open('blocklist.csv', 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

@app.route('/check-call', methods=['POST'])
def check_call():
    data = request.json
    phone_number = data.get('phone_number')

    # Check if the number is in the blocklist
    blocklist = load_blocklist()
    if phone_number in blocklist:
        return jsonify({"status": "blocked", "message": "This number is blocked."}), 403
    
    return jsonify({"status": "allowed", "message": "Call permitted."})

@app.route('/blocklist', methods=['GET', 'POST'])
def manage_blocklist():
    if request.method == 'GET':
        blocklist = load_blocklist()
        return jsonify(list(blocklist))
    
    if request.method == 'POST':
        new_number = request.json.get('phone_number')
        with open('blocklist.csv', 'a') as f:
            f.write(new_number + '\n')
        return jsonify({"status": "success", "message": "Number added to blocklist."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
