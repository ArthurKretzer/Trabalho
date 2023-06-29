import random
import threading
import time

from client import Client
from replicas import Replica


def create_process_list(n):
    peers = [6000 + i for i in range(n)]

    replicas_ids = [i for i in range(int(n / 2))]

    replicas_list = []
    for i in range(int(n / 2)):
        replicas_list.append(Replica(i, peers, replicas_ids))

    client_list = []
    for i in range(int(n / 2), n):
        print(f"Client id {i}")
        client_list.append(Client(i, peers, replicas_ids))
    return replicas_list, client_list


def test_program():
    number_of_processes = 6
    number_of_messages = 10
    replica_list, client_list = create_process_list(number_of_processes)

    threads = []
    for process in replica_list:
        t = threading.Thread(target=process.start)
        threads.append(t)
        t.start()

    time.sleep(2)  # Wait for process initialization

    messages = [
        "May the force be with you.",
        "The force is strong with this one.",
        "I have the high ground!",
        "These aren't the droids you're looking for.",
        "I am your father.",
        "May the Schwartz be with you.",
        "Live long and prosper.",
        "Resistance is futile.",
        "Do or do not. There is no try.",
        "I'll be back.",
    ]

    for _ in range(number_of_messages):
        client = random.choice(client_list)
        message = random.choice(messages)
        client.request_write(f"\033[95m{message}\033[0m")

    for t in threads:
        t.join()


test_program()
