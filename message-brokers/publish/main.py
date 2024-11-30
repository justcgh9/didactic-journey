import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

RABBITMQ_HOST = "localhost"
SCREAMED_QUEUE = "screamed_messages"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zvukovat@gmail.com"
SMTP_PASSWORD = "geeq rrjm cjaq knag"

RECIPIENTS = ["a.kabardiyadi@innopolis.university", "k.strelnikova@innopolis.university", "m.oinoshev@innopolis.university", "n.petukhov@innopolis.university", "i.nasibullina@innopolis.university"]

def send_email(subject: str, body: str, recipients: list):
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(SMTP_USER, recipients, msg.as_string())
        server.quit()
        print(f"Email sent to {recipients}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_message_received(ch, method, properties, body):
    try:
        message = json.loads(body)
        message_text = message.get("message", "")
        from_field = message.get("from", "Unknown")

        subject = f"New Message from {from_field}"
        body = f"Message Content:\n\n{message_text}"

        send_email(subject, body, RECIPIENTS)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=SCREAMED_QUEUE)

channel.basic_consume(
    queue=SCREAMED_QUEUE,
    on_message_callback=on_message_received
)

print(f"Waiting for messages in queue '{SCREAMED_QUEUE}'...")
channel.start_consuming()
