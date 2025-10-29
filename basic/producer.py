"""
Script to send single messages to a queue.
"""
import pika


RABBITMQ_HOST = "localhost"
QUEUE_NAME = "single-queue"
SINGLE_MESSAGE = "Hello World!"

# Establishing connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

# Create queue to send messages
# durable options determine whether a queue will survive a broker restart. It's about
# queue persistence, not message persistence
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Sending a message by using the default exchange
channel.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=SINGLE_MESSAGE
)

print(f"Send {SINGLE_MESSAGE}")

# Be sure that network buffers where flushed by closing the connection
connection.close()
