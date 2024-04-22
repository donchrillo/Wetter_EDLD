import smtplib, ssl
from email.message import EmailMessage
import logging


def SendError(message):
    port = 465  # For starttls
    smtp_server = "<SERVER_ADRESS>"
    sender_email = "<sender_mailadress>"
    receiver_email = "<receiver_mailadress>"
    password = "<PASSWORT>"
    message = message


    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Fehler in EDLE'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Konfiguriere das Logging
    logging.basicConfig(filename='logfile.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    
    try:
        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logging.error(f"Fehler bei Sendmail: {e}")


if __name__ == '__main__':
    SendError("Error Text")
