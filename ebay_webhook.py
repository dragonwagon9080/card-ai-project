from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# MUST match eBay Developer Portal exactly
VERIFICATION_TOKEN = "cardai2026verificationtoken123456"


@app.route("/ebay", methods=["GET"])
def verify():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return "Missing challenge_code", 400

    # Build endpoint from public request host (Cloudflare-safe)
    host = request.headers.get("Host", "")
    endpoint = f"https://{host}/ebay"

    # REQUIRED eBay hash order:
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


@app.route("/ebay", methods=["POST"])
def receive_notification():
    data = request.json

    print("\n📩 eBay Notification Received:")
    print(data)
    print()

    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)