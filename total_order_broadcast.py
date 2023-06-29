import random
import time

from causal_unicast import CausalCommunication


class TotalOrderBroadcast(CausalCommunication):
    def __init__(self, id, peers, group, leader_id=None):
        super().__init__(id, peers, group)
        self.id = id
        self.peers = peers
        self.port = peers[id]
        self.group = group
        self.leader_id = leader_id
        self.msg_seq = 0

    def broadcast(self, id, message):
        message = f"{self.id}::{message}::{self.group}%broadcast"
        self.send(id, message)

    def deliver(self, message):
        if self.id == self.leader_id:
            self.msg_seq += 1
            self.commit_to_group(message + f"::{self.msg_seq}" + "%commit")
            print(
                f"\033[92mProcess {self.id}:\033[0m Delivered {message} from \033[93mprocess {self.id}\033[0m with sequence number \033[91m{self.msg_seq}\033[0m\n"
            )

    def commit_to_group(self, message):
        pass

    def commit(self, message):
        time.sleep(random.uniform(0, 2))
        message = message.split("::")
        sender_id = int(message[0])
        msg = message[1]
        msg_seq = int(message[3])

        self.buffer.put(msg)

        while (~self.buffer.empty()) & ((self.msg_seq + 1) <= msg_seq):
            if (self.msg_seq + 1) == msg_seq:
                message = self.buffer.get()
                print(
                    f"\033[92mProcess {self.id}:\033[0m Delivered {message} from \033[93mprocess {sender_id}\033[0m with sequence number \033[91m{msg_seq}\033[0m\n"
                )

                self.msg_seq += 1
