from Event import Event
from Receiver import Receiver

class Receive_Entanglement_Event(Event):

    def __init__(self, recipient, state, time):
        self.recipient = recipient
        self.state = state
        self.time = time

    def execute(self):
        receiver = Receiver(self.recipient)
        event_list = receiver.handle_receive_entanglement_event(self)
        return event_list

    def to_string(self):
        string = super().to_string()
        return string + " :: Receive Entanglement Event"