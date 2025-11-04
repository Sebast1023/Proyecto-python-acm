import imaplib
import email
from email.header import decode_header
from ControlConexion import ControlConexion


class ControlPrincipal:
    def __init__(self):
        self.control_conexion = ControlConexion()
        self.ejecutar()

    def ejecutar(self):
        try:
            email_account, password = self.control_conexion.obtener_credenciales()
            self.leer_ultimo_correo(email_account, password)
        except Exception as e:
            print("❌ Error al iniciar la aplicación:", e)

    def leer_ultimo_correo(self, email_account, password):
        IMAP_SERVER = "imap.gmail.com"

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_account, password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        if not email_ids:
            print("📭 No hay correos en la bandeja de entrada.")
            mail.logout()
            return

        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg.get("Subject", ""))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        sender = msg.get("From")
        print(f"\n📬 De: {sender}")
        print(f"📨 Asunto: {subject}\n")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")

        print("💬 Contenido del correo:")
        print(body)

        mail.logout()
