from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Jenkins Deployment Success!</h1>'

@app.route('/health')
def health():
    return jsonify(status='UP'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)