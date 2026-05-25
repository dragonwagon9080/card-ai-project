from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================

VERIFICATION_TOKEN = os.getenv(
    "EBAY_VERIFICATION_TOKEN",
    "cardai2026verificationtoken123456"
)

# =========================
# HEALTH CHECK
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "service": "eBay Webhook Running"
    }), 200


# =========================
# HELPERS
# =========================
def get_public_endpoint():
    """
    Render + proxy safe URL detection
    """
    host = request.headers.get("X-Forwarded-Host", request.headers.get("Host", ""))
    return f"https://{host}/ebay"


# =========================
# EBAY VERIFICATION (CHALLENGE)
# =========================
@app.route("/ebay", methods=["GET"])
def verify():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return jsonify({"error": "Missing challenge_code"}), 400

    endpoint = get_public_endpoint()

    # eBay required hash order:
    # challengeCode + verificationToken + endpoint
    hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{endpoint}"
    response_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    print("\n--- eBay Challenge Debug ---")
    print("challenge_code:", challenge_code)
    print("endpoint:", endpoint)
    print("hash:", response_hash)
    print("---------------------------\n")

    return jsonify({
        "challengeResponse": response_hash
    }), 200


# =========================
# EBAY NOTIFICATIONS (FUTURE PIPELINE)
# =========================
@app.route("/ebay", methods=["POST"])
def receive_notification():
    try:
        data = request.get_json(force=True, silent=True)

        print("\n📩 eBay Notification Received:")
        print(data)
        print()

        return "", 204

    except Exception as e:
        print("Notification error:", str(e))
        return jsonify({"error": "invalid payload"}), 400


# =========================
# MAIN (RENDER COMPATIBLE)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)