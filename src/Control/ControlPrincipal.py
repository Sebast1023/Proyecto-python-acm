import json
from pathlib import Path
import imaplib
import email
from email.header import decode_header


def load_credentials(path="specs/credentials.json"):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No se encontró el archivo de credenciales: {p.resolve()}")
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"El archivo JSON está mal formado: {e}")

    # Validar campos mínimos
    if "email" not in data or "password" not in data:
        raise KeyError("El JSON debe contener las claves 'email' y 'password'")

    return data["email"], data["password"]


# función load_credentials definida como arriba
email_account, password = load_credentials()

IMAP_SERVER = "imap.gmail.com"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(email_account, password)
mail.select("inbox")

status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

if not email_ids:
    print("No hay correos en la bandeja de entrada.")
else:
    latest_email_id = email_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg.get("Subject", ""))[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")

    print("De:", msg.get("From"))
    print("Asunto:", subject)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")

    print("\nContenido:\n", body)

mail.logout()
