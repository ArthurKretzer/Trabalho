import ast


class VectorClock:
    def __init__(self, id, vector_clock):
        self.id = id
        self.vector_clock = vector_clock

    def getClock(self):
        return self.vector_clock

    def addClock(self, id):
        self.vector_clock[id] += 1

    def adjustClock(self, incoming_clock):
        for i in range(len(incoming_clock)):
            self.vector_clock[i] = max(self.vector_clock[i], incoming_clock[i])

    def extract_logical_clock(self, string):
        return ast.literal_eval(string)

    def is_causal_order(self, incoming_clock):
        return self.compare_vector_clocks(incoming_clock) >= 0

    def compare_vector_clocks(self, incoming_clock):
        if len(incoming_clock) != len(self.vector_clock):
            raise ValueError("Vector clocks must have the same length.")

        for i in range(len(incoming_clock)):
            if i != self.id:
                if incoming_clock[i] < self.vector_clock[i]:
                    return -1
                elif incoming_clock[i] > self.vector_clock[i]:
                    return 1

        return 0
