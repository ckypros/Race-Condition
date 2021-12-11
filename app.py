from typing import List
import threading
import random
import time

def getBuffer(n: int) -> List[int]:
    return [0] * n

# Buffer is array of ints, n length initialized to 0

# Producer executes shorts bursts of random duration, length k1
# During each k1, adds 1 to next k1 slots of buffer % n

# Consumer bursts of random duration, length k2
# During each k2, reads next k2 slots and resets each to 0

# if slot contains number > 1, consumer has fallen behind, race condition

def get_producer(buffer: List[int]) -> None:
    n: int = len(buffer)
    next_in: int = 0
    k1_low: int = 1
    k1_high: int = 30
    t1_low: int = 1
    t1_high: int = 3
    while True:
        k1: int = random.randint(k1_low, k1_high)
        print("PRODUCER -- k1:", k1, "next_in:", next_in)
        for i in range(k1):
            buffer[(next_in + i) % n] += 1
        next_in = (next_in + k1) % n
        t1: int = random.randint(t1_low, t1_high)
        print("PRODUCER -- sleeping for t1:", t1, "next_in:", next_in)
        time.sleep(t1)


def get_consumer(buffer: List[int]) -> None:
    n: int = len(buffer)
    next_out: int = 0
    k2_low: int = 1
    k2_high: int = 10
    t2_low: int = 1
    t2_high: int = 3
    while True:
        t2: int = random.randint(t2_low, t2_high)
        print("CONSUMER -- sleeping for t2:", t2, "next_out:", next_out)
        time.sleep(t2)
        k2: int = random.randint(k2_low, k2_high)
        print("CONSUMER -- k2:", t2, "next_out:", next_out)
        for i in range(k2):
            data: int = buffer[(next_out + i) % n]
            if (data > 1): 
                print("-" * 30, "RACE CONDITION", "-" * 30)
            buffer[(next_out + i) % n] = 0
        next_out = (next_out + k2) % n

def print_buffer(buffer: List[int]) -> None:
    while True:
        interval: int = 1
        time.sleep(interval)
        print(buffer)
        

if __name__ == "__main__":
    n: int = 100
    buffer: List[int] = getBuffer(n)

    # Create threads
    producer: threading.Thread = threading.Thread(target=get_producer, args=([buffer]), name='producer')
    consumer: threading.Thread = threading.Thread(target=get_consumer, args=([buffer]), name='consumer')
    printer: threading.Thread = threading.Thread(target=print_buffer, args=([buffer]), name='printer')

    # Start threads
    producer.start()
    consumer.start()
    printer.start()

    producer.join()
    consumer.join()
    printer.join()