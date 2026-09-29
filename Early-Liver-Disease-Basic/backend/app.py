from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = '127.0.0.1'
PORT = 5000

class LiverHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json({"status": "ok"})

    def do_GET(self):
        if self.path == '/health':
            self.send_json({"status": "ok"})
        elif self.path == '/':
            self.send_json({"message": "Liver Disease Prediction backend is running"})
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path != '/predict':
            self.send_json({"error": "Not found"}, 404)
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
        except Exception:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        required = [
            'age', 'gender', 'total_bilirubin', 'direct_bilirubin',
            'alkaline_phosphotase', 'alamine_aminotransferase',
            'aspartate_aminotransferase', 'total_proteins', 'albumin',
            'albumin_and_globulin_ratio'
        ]
        missing = [key for key in required if key not in data]
        if missing:
            self.send_json({"error": "Missing fields: " + ', '.join(missing)}, 400)
            return

        # Simple demonstration rule. Later this can be replaced by a trained ML model.
        score = 0
        if float(data['total_bilirubin']) > 1.2: score += 1
        if float(data['direct_bilirubin']) > 0.4: score += 1
        if float(data['alkaline_phosphotase']) > 250: score += 1
        if float(data['alamine_aminotransferase']) > 45: score += 1
        if float(data['aspartate_aminotransferase']) > 45: score += 1
        if float(data['albumin']) < 3.5: score += 1

        probability = min(0.10 + score * 0.14, 0.94)
        prediction = 'Higher Risk' if probability >= 0.50 else 'Lower Risk'

        self.send_json({
            "prediction": prediction,
            "probability": probability,
            "message": "Demo prediction only; not a medical diagnosis."
        })

if __name__ == '__main__':
    print(f'Backend running at http://{HOST}:{PORT}')
    HTTPServer((HOST, PORT), LiverHandler).serve_forever()
