import imaplib
import email
from email.header import decode_header
import getpass

IMAP_SERVER = "imap.gmail.com"
EMAIL_ADDRESS = input("Digite o email: ")
PASSWORD = getpass.getpass("Digite a senha do email gerada para o script: ")

mail = imaplib.IMAP4_SSL(IMAP_SERVER)


try:
    mail.login(EMAIL_ADDRESS, PASSWORD)
    print("Login bem-sucedido!")
except imaplib.IMAP4.error as e :
    print("Falha no login:", e)
    exit()

status, messages = mail.select("inbox")
if status != "OK":
    print("Falha ao selecionar a caixa de entrada.")
    exit()

status, email_ids = mail.search(None, "UNSEEN")
email_id_list = email_ids[0].split()

print(f"Você tem {len(email_id_list)} emails não lidos.")

for email_id in email_id_list:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    if status != "OK":
        print(f"Falha ao buscar o email ID {email_id.decode()}.")
        continue

    msg = email.message_from_bytes(msg_data[0][1])

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")
    from_ = msg.get("From")

    print("------------------")
    print(f"Assunto: {subject}")
    print(f"De: {from_}")

    if msg.is_multipart():
        for part in msg.walk():

            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                print("Corpo do email:")
                print(body)
                break
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            body = msg.get_payload(decode=True).decode()
            print("Corpo do email:")
            print(body)

    print("="*50)

