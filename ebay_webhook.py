from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# =========================
# CONFIG (USE ENV VARS FOR DEPLOYMENT)
# =========================

VERIFICATION_TOKEN = os.getenv(
    "EBAY_VERIFICATION_TOKEN",
    "cardai2026verificationtoken123456"  # fallback for local testing
)

# =========================
# HEALTH CHECK (Render needs this sometimes)
# =========================
@app.route("/", methods=["GET"])
def home():
    return "eBay Webhook Running", 200


# =========================
# EBAY VERIFICATION ENDPOINT
# =========================
@app.route("/ebay", methods=["GET"])
def verify():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return "Missing challenge_code", 400

    # Use Render/Cloudflare safe host header
    host = request.headers.get("Host", "")
    endpoint = f"https://{host}/ebay"

    # REQUIRED eBay order:
    # challengeCode + verificationToken + endpoint
    hash_input = challenge_code + VERIFICATION_TOKEN + endpoint
    response_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    print("\n--- eBay Challenge Debug ---")
    print("challenge:", challenge_code)
    print("endpoint:", endpoint)
    print("hash:", response_hash)
    print("---------------------------\n")

    return jsonify({
        "challengeResponse": response_hash
    }), 200


# =========================
# EBAY NOTIFICATIONS (FUTURE DATA PIPELINE)
# =========================
@app.route("/ebay", methods=["POST"])
def receive_notification():
    data = request.json

    print("\n📩 eBay Notification Received:")
    print(data)
    print()

    return "", 204


# =========================
# MAIN (RENDER COMPATIBLE)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)