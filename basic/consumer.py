"""
Script to receive single messages from a queue.
"""
import os
import sys
import pika


RABBITMQ_HOST = "localhost"
QUEUE_NAME = "single-queue"

def main():
    # Establishing connection with the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Make sure the queue exists. This declaration is idempotent
    # If we are sure that the queue already exists we can omit this, if not, it's a
    # good practice to repeat declaring the queue in both sender and receiver programs
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # To receive messages we need to subscribe a callback function to a queue. Whenever we
    # receive a message, this callback function is called by the Pika library.
    def callback(ch, method, properties, body):
        print(f"Received {body}")

    channel.basic_consume(
        queue=QUEUE_NAME,
        auto_ack=True,
        on_message_callback=callback
    )

    # Never-ending loop that waits for data and runs callbacks whenever necessary
    print("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")

        try:
            sys.exit(0)
        except:
            os._exit(0)
