from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pika
import json

app = FastAPI()

class Message(BaseModel):
    from_: str = Field(..., alias="from", min_length=1)
    message: str = Field(..., min_length=1)

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "received_messages"

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection

@app.post("/messages")
def post_message(message: Message):
    try:
        data = message.dict(by_alias=True)

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(data)
        )

        connection.close()

        return {"status": "Message sent to RabbitMQ"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
