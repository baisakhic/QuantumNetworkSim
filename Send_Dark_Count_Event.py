from Event import Event
from Link_ES_Receiver import Link_ES_Receiver

class Send_Dark_Count_Event(Event):

    def __init__(self, recipient, time):
        self.recipient = recipient
        self.time = time

    def get_recipient(self):
        return self.recipient

    def execute(self):
        link = Link_ES_Receiver()
        event_list = link.handle_send_dark_count_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Send Dark Count Event"