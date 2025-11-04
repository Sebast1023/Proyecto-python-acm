import imaplib
import email
from email.header import decode_header


class ControlCorreo:
    def __init__(self, email_account, password):
        self.email_account = email_account
        self.password = password
        self.server = "imap.gmail.com"
        self.mail = None

    def conectar(self):
        """Conecta al servidor IMAP de Gmail."""
        self.mail = imaplib.IMAP4_SSL(self.server)
        self.mail.login(self.email_account, self.password)
        self.mail.select("inbox")

    def leer_todos(self):
        """Lee todos los correos del buzón y devuelve una lista con sus datos."""
        self.conectar()
        status, messages = self.mail.search(None, "ALL")
        email_ids = messages[0].split()
        correos = []

        for num in email_ids:
            status, msg_data = self.mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Decodificar asunto
            subject, encoding = decode_header(msg.get("Subject", ""))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            # Obtener remitente
            sender = msg.get("From")

            # Obtener cuerpo (solo texto plano)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")

            correos.append({
                "id": num,
                "remitente": sender,
                "asunto": subject,
                "contenido": body
            })

        return correos

    def eliminar_correo(self, correo_id):
        """Elimina un correo específico por su ID."""
        self.mail.store(correo_id, '+FLAGS', '\\Deleted')

    def cerrar(self):
        """Guarda y cierra la sesión."""
        if self.mail:
            self.mail.expunge()  # aplicar eliminaciones
            self.mail.logout()
