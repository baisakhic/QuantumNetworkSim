from Event import Event
from GlobalVars import cm

class Receive_Data_Event(Event):
    sender = ""
    data = None

    def __init__(self, sender, time, entanglement, value):
        self.sender = sender
        self.time = time
        self.entanglement = entanglement
        self.value = value

    def get_sender(self):
        return self.sender

    def execute(self):
        event_list = cm.handle_receive_data_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Receive Data Event"