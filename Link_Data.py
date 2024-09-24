from Receive_Data_Event import Receive_Data_Event
from Link import Link
import sys

class Link_Data(Link):

    def handle_send_data_event(self, event):
        receive_event = []
        receive_event.append(Receive_Data_Event(event.get_sender(), event.get_time() + sys.float_info.min, event.entanglement, event.value))
        return receive_event