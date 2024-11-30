import pika
import json

RABBITMQ_HOST = "localhost"
RECEIVED_QUEUE = "received_messages"
FILTERED_QUEUE = "filtered_messages"

STOP_WORDS = {"bird-watching", "ailurophobia", "mango"}

def contains_stop_words(message_text: str) -> bool:
    return any(word in message_text for word in STOP_WORDS)

def on_message_received(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(message)
        message_text = message.get("message", "")

        if contains_stop_words(message_text):
            print(f"Message discarded due to stop words: {message}")
        else:
            print(f"Message forwarded: {message}")

            channel.queue_declare(queue=FILTERED_QUEUE)
            channel.basic_publish(
                exchange="",
                routing_key=FILTERED_QUEUE,
                body=json.dumps(message)
            )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=RECEIVED_QUEUE)

channel.basic_consume(
    queue=RECEIVED_QUEUE,
    on_message_callback=on_message_received
)

print(f"Waiting for messages in queue '{RECEIVED_QUEUE}'...")
channel.start_consuming()
