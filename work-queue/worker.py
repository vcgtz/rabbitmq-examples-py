"""
Script to receive single messages from a queue.
"""
import os
import sys
import time
import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "4dm1n"
QUEUE_NAME = "work-queue"

def main():
    # Open the connection to the RabbitMQ server by using a password and user
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        ),
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Define the callback that will be executed for each message and doing the ack
    # manually
    def callback(ch, method, properties, body):
        print(f"Received {body}")
        time.sleep(body.count(b"."))
        print("Task done")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    # The prefetch_count tells RabbitMQnot give more than one message at a time. Or, in other words
    # don´t dispatch new messages to a worker until it has processed and acknowledged the previous
    # one. Instead, it will dispatch it to the next worker that is not still busy
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

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
