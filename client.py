import random

from total_order_broadcast import TotalOrderBroadcast


class Client(TotalOrderBroadcast):
    def __init__(self, id, peers, replicas_ids):
        super().__init__(id, peers, "C")
        self.replicas_ids = replicas_ids
        self.id = id

    def request_write(self, message):
        id = random.choice(self.replicas_ids)
        print(
            f"\033[94mProcess {self.id}:\033[0m Client requesting write of {message} in replica {id}\n"
        )
        self.send_message(id, message)

    def brodcast_request_write(self, message):
        print(
            f"\033[94mProcess {self.id}:\033[0m Client broadcasting write of {message}\n"
        )
        for replica_id in self.replicas_ids:
            self.broadcast(replica_id, message)
