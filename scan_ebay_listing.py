from openai import OpenAI
import requests
import base64
import json

# =========================
# IMPORT YOUR NEW SYSTEMS
# =========================

from parallel_normalizer import normalize_parallel
from parallel_scoring import score_parallel

# =========================
# CONFIG
# =========================

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# HELPERS
# =========================

def image_url_to_base64(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Could not download image: {url}")

    return base64.b64encode(response.content).decode("utf-8")


# =========================
# AI ANALYSIS
# =========================

def analyze_card_image(image_url):

    print("Downloading image...")

    base64_image = image_url_to_base64(image_url)

    print("Sending image to OpenAI Vision...")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert sports card analyzer.

Extract as much information as possible.

Return ONLY valid JSON.

Fields:
- player_name
- year
- sport
- brand
- set
- card_number_front
- card_number_back
- serial_number
- print_run
- observed_colors
- estimated_card_type

- graded (true/false)
- grading_company (PSA, BGS, SGC, CGC, NONE)
- grade (e.g. PSA 10, BGS 9.5, SGC 10, null if not graded)
- cert_number (string or null)

Use null if unknown.

If the card is in a slab (plastic case), detect:
- grading company logo
- grade label text
- cert number if visible
Do NOT guess cert numbers. Only extract if clearly visible.

Do NOT estimate value or rarity.
Only extract factual observable data from the image.
"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this sports card image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    result = response.choices[0].message.content

    # clean JSON output
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return result


# =========================
# MAIN
# =========================

def main():

    image_url = input("Paste eBay IMAGE url: ").strip()

    result = analyze_card_image(image_url)

    print("\n===== RAW AI RESULT =====\n")
    print(result)

    try:
        parsed = json.loads(result)

        # =========================
        # PARALLEL NORMALIZATION
        # =========================

        raw_parallel = parsed.get("parallel")
        clean_parallel = normalize_parallel(raw_parallel)
        score = score_parallel(clean_parallel)

        parsed["parallel_normalized"] = clean_parallel
        parsed["parallel_score"] = score

        print("\n===== ENHANCED CARD DATA =====\n")

        for key, value in parsed.items():
            print(f"{key}: {value}")

        print("\n===== SUMMARY =====")
        print("Parallel:", clean_parallel)
        print("Score:", score)

    except Exception as e:
        print("\nJSON parsing failed.")
        print(e)


if __name__ == "__main__":
    main()