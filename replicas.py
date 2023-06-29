from total_order_broadcast import TotalOrderBroadcast


class Replica(TotalOrderBroadcast):
    def __init__(self, id, peers, replicas_ids, leader_id):
        super().__init__(id, peers, "R", leader_id)
        self.replicas_ids = replicas_ids

    def replicate_to_group(self, message):
        for replica_id in self.replicas_ids:
            if replica_id != self.id:
                self.send_message(replica_id, message)

    def commit_to_group(self, message):
        for replica_id in self.replicas_ids:
            if replica_id != self.id:
                self.send(replica_id, message)
