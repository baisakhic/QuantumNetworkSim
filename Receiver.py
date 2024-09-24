import math, random
import sys

from Send_Data_Event import Send_Data_Event

basis_map = {"A": "H", "B": "H"}
last_ping_time = {"A": 0, "B": 0}

angle = 0.0

def set_basis(basis_a, basis_b):
    basis_map["A"] = basis_a
    basis_map["B"] = basis_b

def set_angle(angle_val):
    global angle
    angle = angle_val
    
class Receiver():

    dead_time = 4.0/1000 #4 microsecond
    efficiency = 0.1
    def __init__(self, recipient):
        self.recipient = recipient


    def handle_receive_entanglement_event(self, event):
        global angle
        send_event = []
        current_time = event.get_time()
        state = event.state
        if state.measure(self.recipient, basis_map[self.recipient], angle):
            chance = random.random()
            if chance <= self.efficiency:
                if current_time >= last_ping_time[self.recipient]:
                    last_ping_time[self.recipient] += self.dead_time  # reset timer
                    value = -1
                    if self.recipient == "A":
                        value = state.alice_measure_val
                    else:
                        value = state.bob_measure_val
                    send_event.append(Send_Data_Event(self.recipient, event.get_time() + sys.float_info.min, True, value))
                    # if state.alice_dm is not None and state.bob_dm is not None:
                    #     print(self.recipient + " Detected Entanglement, also detected by other party")
                    # else:
                    #     print(self.recipient + " Detected Entanglement, not (yet) detected by other party")

        return send_event


    def handle_receive_dark_count_event(self, event):
        send_event = []
        current_time = event.get_time()
        chance = random.random()
        if chance <= self.efficiency:
            if current_time >= last_ping_time[self.recipient]:
                last_ping_time[self.recipient] += self.dead_time  # reset timer
                send_event.append(Send_Data_Event(self.recipient, event.get_time() + sys.float_info.min, False, -1))
                # print(self.recipient + " Detected Dark Count")

        return send_event