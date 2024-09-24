from Send_Entanglement_Event import Send_Entanglement_Event
from State import State
import numpy as np
import math
import random

class Entanglement_Source:
    average_time = 5 #per second
    execution_time = 30 #second
    poisson_lam = 15000
    state_val = None

    def __init__(self, state, time):
        self.state_val = state
        self.execution_time = time

    @staticmethod
    def nextTime(rate_parameter):
        return -math.log(1.0 - random.random()) / rate_parameter

    def generate_entanglement_event(self, recipient, time):
        event = Send_Entanglement_Event(recipient, time)
        return event

    def run(self):
        event_list = []
        time_interval = 0
        while time_interval <= self.execution_time:
            nt = self.nextTime(self.poisson_lam)
            time_interval += nt
            state = State(self.state_val)
            eventA = self.generate_entanglement_event("A", time_interval)
            eventB = self.generate_entanglement_event("B", time_interval)
            eventA.set_State(state)
            eventB.set_State(state)
            event_list.append(eventA)
            event_list.append(eventB)
        return event_list
