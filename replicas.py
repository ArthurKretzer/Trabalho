from causal_unicast import CausalCommunication


class Replica(CausalCommunication):
    def __init__(self, id, peers, replicas_ids):
        super().__init__(id, peers, "R")
        self.replicas_ids = replicas_ids

    def replicate_to_group(self, message):
        for replica_id in self.replicas_ids:
            if replica_id != self.id:
                self.send_message(replica_id, message)
