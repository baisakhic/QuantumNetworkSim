from Event import Event
from Link_Data import Link_Data


class Send_Data_Event(Event):

    def __init__(self, sender, time, entanglement, value):
        self.sender = sender
        self.time = time
        self.entanglement = entanglement
        self.value = value

    def get_sender(self):
        return self.sender


    def execute(self):
        link = Link_Data()
        event_list = link.handle_send_data_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Send Data Event"