from Event import Event
from Link_ES_Receiver import Link_ES_Receiver

class Send_Entanglement_Event(Event):
    entangle_state = None
    recipient = ""

    def __init__(self, recipient, time):
        self.recipient = recipient
        self.time = time

    def set_State(self, state):
        self.entangle_state = state

    def get_recipient(self):
        return self.recipient

    def get_entanglement_state(self):
        return self.entangle_state

    def execute(self):
        link = Link_ES_Receiver()
        event_list = link.handle_send_entanglement_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Send Entanglement Event"