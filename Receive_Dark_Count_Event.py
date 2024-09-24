from Event import Event
from Receiver import Receiver

class Receive_Dark_Count_Event(Event):
    def __init__(self, recipient, time):
        self.recipient = recipient
        self.time = time

    def execute(self):
        receiver = Receiver(self.recipient)
        event_list = receiver.handle_receive_dark_count_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Receive Dark Count Event"