import sys

from Receive_Entanglement_Event import Receive_Entanglement_Event
from Receive_Dark_Count_Event import Receive_Dark_Count_Event
from Link import Link

class Link_ES_Receiver(Link):
    def handle_send_entanglement_event(self, event):
        receive_event = []
        receive_event.append(Receive_Entanglement_Event(event.get_recipient(), event.entangle_state, event.get_time() + sys.float_info.min))
        return receive_event

    def handle_send_dark_count_event(self, event):
        receive_event = []
        receive_event.append(Receive_Dark_Count_Event(event.get_recipient(), event.get_time() + sys.float_info.min))
        return receive_event

