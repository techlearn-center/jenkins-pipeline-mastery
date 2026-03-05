from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "order-service", "version": "1.0.0"})

@app.route("/api/orders")
def get_orders():
    return jsonify({
        "orders": [
            {"id": 1, "product": "Widget", "quantity": 5, "price": 9.99},
            {"id": 2, "product": "Gadget", "quantity": 2, "price": 24.99},
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
