import json
from datetime import datetime, timezone

import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Message(BaseModel):
    from_: str = Field(..., alias="from", min_length=1)
    message: str = Field(..., min_length=1)

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "received_messages"

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat() 
    raise TypeError("Type not serializable")

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection

@app.post("/messages")
def post_message(message: Message):
    try:
        data = message.dict(by_alias=True)
        data['created_at'] = datetime.now(timezone.utc)

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(data, default=datetime_serializer)
        )

        connection.close()

        return {"status": "Message sent to RabbitMQ"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
