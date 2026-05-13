import imaplib
import os
import email
from email.header import decode_header
import requests
from openai import OpenAI

EMAIL_USER = "YOUR_EMAIL@gmail.com"
EMAIL_PASS = "YOUR_APP_PASSWORD"
OPENROUTER_KEY = "YOUR_OPENROUTER_API_KEY"
MODEL_LIST_URL = "https://shir-man.com/api/free-llm/top-models"

def get_best_model():
    try:
        r = requests.get(MODEL_LIST_URL)
        data = r.json()
        model_id = data['models'][0]['id']
        return model_id
    except Exception:
        print("Warning: Fetching model failed. Using fallback: openrouter/free")
        return "openrouter/free"

def get_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "prompt.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

def classify_email(text):
    response = client.chat.completions.create(
        model=get_best_model(),
        messages=[
            {"role": "system", "content": get_prompt()},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def process_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    
    if messages[0]:
        for num in messages[0].split():
            status, data = mail.fetch(num, "(RFC822)")
            res, msg = data[0]
            full_msg = email.message_from_bytes(msg)

            subject = decode_header(full_msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            body = ""
            if full_msg.is_multipart():
                for part in full_msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = full_msg.get_payload(decode=True).decode()

            print(f"\nProcessing email: {subject}")
            tag = classify_email(body)
            print(f"Result (Tag): {tag}")

    mail.logout()

if __name__ == "__main__":
    process_emails()