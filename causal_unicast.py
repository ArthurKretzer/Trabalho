import random
import socket
import threading
import time
from queue import Queue

from vector_clock import VectorClock


class CausalCommunication:
    def __init__(self, id, peers, group) -> None:
        self.id = id
        self.peers = peers
        self.port = peers[id]
        self.group = group
        self.vector_clock = VectorClock(id, [0] * len(peers))
        self.buffer = Queue()
        self.lock = threading.Lock()

    def send_message(self, id, message):
        if id != self.id:
            self.vector_clock.addClock(self.id)
            deps = self.vector_clock.getClock()
            message = f"{deps}::{self.id}::{message}::{self.group}"
            print(
                f"\033[92mProcess {self.id}:\033[0m Sending message {message} to \033[93mprocess {id}\033[0m\n"
            )
            self.send(id, message)
        else:
            print(f"\033[92mProcess {self.id}:\033[0m Cannot send message to self.\n")

    def send(self, id, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.peers[id]))
            s.sendall(message.encode("utf-8"))

    def receive_message(self, conn, addr):
        m = conn.recv(1024).decode("utf-8")
        print(f"\033[92mProcess {self.id}:\033[0m Message {m} received.\n")
        self.receive(m)

    def receive(self, message):
        time.sleep(random.uniform(0, 2))

        message = message.split("::")

        incoming_clock = self.vector_clock.extract_logical_clock(message[0])

        sender_id = int(message[1])

        msg = message[2]

        group = message[3]

        self.buffer.put(msg)

        while (~self.buffer.empty()) & self.vector_clock.is_causal_order(
            incoming_clock
        ):
            message = self.buffer.get()
            print(
                f"\033[92mProcess {self.id}:\033[0m Delivered {message} from \033[93mprocess {sender_id}\033[0m with logical clock \033[91m{incoming_clock}\033[0m\n"
            )

            self.vector_clock.adjustClock(incoming_clock)
            self.vector_clock.addClock(self.id)

            print(
                f"\033[92mProcess {self.id}:\033[0m Resulting logical clock \033[91m{self.vector_clock.getClock()}\033[0m\n"
            )

            if group == "C":
                self.replicate_to_group(message)

    def replicate_to_group(self, message):
        pass

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", self.port))
            s.listen()

            print(f"Processo {self.id} iniciado e aguardando conexões...\n")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.receive_message, args=(conn, addr)).start()
