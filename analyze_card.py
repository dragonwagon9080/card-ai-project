from openai import OpenAI
import base64

# -----------------------------
# OpenAI API Key
# -----------------------------
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# -----------------------------
# Encode image to base64
# -----------------------------
def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# -----------------------------
# Load image
# -----------------------------
base64_image = encode_image("images/front.jpg")

# -----------------------------
# Send image to AI
# -----------------------------
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Analyze this sports card image and identify:\n"
                        "- player name\n"
                        "- year\n"
                        "- brand\n"
                        "- set\n"
                        "- card number\n"
                        "- serial number\n"
                        "- grader and grade if visible\n\n"
                        "Return the result as clean JSON."
                    )
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

# -----------------------------
# Print result
# -----------------------------
print(response.choices[0].message.content)