import multiprocessing
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from filters.protocol import Filter
from pipe import Pipe

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zvukovat@gmail.com"
SMTP_PASSWORD = "geeq rrjm cjaq knag"

RECIPIENTS = ["alisher.100704@gmail.com", "strelnikova.kira354@gmail.com"]

class PublishFilter(Filter):
    def __init__(self, inputs: list[Pipe], outputs: list[Pipe]):
        super().__init__()
        self.inputs, self.outputs = inputs, outputs
       

    def send_email(self, subject: str, body: str, recipients: list):
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

    def run(self):
        self._process = multiprocessing.Process(target=self.target)
        self.process.start()

    def target(self):
        while True:
            for input_pipe in self.inputs:
                message = input_pipe.recv()
                print(f"publish {message}")
                self.send_email(f"New message from {message.from_}", f"Message Content:\n\n{message.message}", RECIPIENTS)
                for output_pipe in self.outputs:
                    output_pipe.send(message)
