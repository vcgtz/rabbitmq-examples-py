# Example of a single Consumer and Producer
<img width="595" height="157" alt="image" src="https://github.com/user-attachments/assets/e2885b37-933e-406e-94ca-a27f3a95aebd" />

## How to run it?
**Start the RabbitMQ Server**
```bash
docker compose up
```

**Start listening to messages by the `Consumer`**

This command will start the consumer to wait for every message that is sent.
```bash
uv run basic/consumer.py
```

**Send messages through the `Producer`**

This command will send a single message (the string `Hello World!`) to the `Consumer` every time it's executed.
```bash
uv run basic/producer.py
```
