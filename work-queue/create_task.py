import sys
import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "4dm1n"
QUEUE_NAME = "work-queue"

# Open the connection to the RabbitMQ server by using a password and user
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    ),
)
channel = connection.channel()

# Declare a new work queue and stablish it as durable, so this means that even the
# RabbitMQ server is restarted, the queue will survive
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Receive a message via CLI or use one by default
message = " ".join(sys.argv[1:]) or "Hello World!"

# Send the message to the work queue and also set the message as persistent, this means
# that the message will survive even if the server is restarted (the persistence
# guarantees aren't strong)
channel.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    )
)

print(f"Send {message}")

connection.close()
