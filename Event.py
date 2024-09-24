from abc import abstractmethod

class Event:
    time = 0

    @abstractmethod
    def execute(self):
        return []

    @abstractmethod
    def to_string(self):
        return "Event executed at " + str(round(self.time, 3))

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time