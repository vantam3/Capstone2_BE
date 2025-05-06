# utils/mistral_api.py
import requests
import os

HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")  # Bạn nên lưu key trong .env

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_mistral(user_input):
    prompt = f"""<|system|>
You are a friendly English tutor helping Vietnamese students practice speaking.
<|user|>
{user_input}
<|assistant|>
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        result = response.json()
        print("[✔] Phản hồi từ Mistral:", result)
        return result[0]["generated_text"]
    except Exception as e:
        return "Sorry, I could not respond at the moment."
