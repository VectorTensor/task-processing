import redis
import json
import time

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def consume():
    while True:
        _, message = redis_client.brpop('task_queue')
        decoded_message = json.loads(message)
        print("Processing message...")
        try:
            t = decoded_message['time']
            time.sleep(t)

        except Exception as e:
            print(f"Json decode error {e}")
            continue
        
        print(f"Consumed: {message}")


if __name__ == "__main__":
    consume()
