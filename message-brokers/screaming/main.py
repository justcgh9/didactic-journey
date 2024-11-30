import pika
import json

RABBITMQ_HOST = "localhost"
FILTERED_QUEUE = "filtered_messages"
SCREAMED_QUEUE = "screamed_messages"

def on_message_received(ch, method, properties, body):
    try:
        message = json.loads(body)
        message_text = message.get("message", "")

        message["message"] = message_text.upper()

        print(f"Message screamed: {message}")

        channel.queue_declare(queue=SCREAMED_QUEUE)
        channel.basic_publish(
            exchange="",
            routing_key=SCREAMED_QUEUE,
            body=json.dumps(message)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=FILTERED_QUEUE)

channel.basic_consume(
    queue=FILTERED_QUEUE,
    on_message_callback=on_message_received
)

print(f"Waiting for messages in queue '{FILTERED_QUEUE}'...")
channel.start_consuming()
