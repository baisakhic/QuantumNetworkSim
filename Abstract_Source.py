from Send_Dark_Count_Event import Send_Dark_Count_Event

class Abstract_Source:
   total_time = 30
   avg_rate = 1.0/1000

   def __init__(self, time):
        self.total_time = time

   def generate_dark_event(self, recipient, time):
        event = Send_Dark_Count_Event(recipient, time)
        return event

   def run(self):
       event_list = []
       time_interval = 0
       while time_interval <= self.total_time:
           time_interval += self.avg_rate
           eventA = self.generate_dark_event("A", time_interval)
           eventB = self.generate_dark_event("B", time_interval)
           event_list.append(eventA)
           event_list.append(eventB)
       return event_list

