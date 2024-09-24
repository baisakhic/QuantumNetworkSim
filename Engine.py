import sys

import GlobalVars
import Receiver
from Entanglement_Source import Entanglement_Source
from Send_Entanglement_Event import Send_Entanglement_Event
from Abstract_Source import Abstract_Source
from GlobalVars import cm
import argparse, math
import numpy as np


def main(state_id, test_bell, time):
    if test_bell:
        # Lazy copy and paste of the engine code from below
        basis_states = ["Z", "X"]
        num_angles = 15
        angles = np.linspace(0, 2*np.pi, num_angles)
        all_basis_states = []
        chsh = {}
        for angle in angles:
            for alice in basis_states:
                for bob in basis_states:
                    all_basis_states.append(alice + bob)
                    Receiver.set_basis(alice, bob)
                    Receiver.set_angle(angle)
                    Receiver.last_ping_time = {"A": 0, "B": 0}
                    cm.basis = alice + bob
                    q = []
                    e = Entanglement_Source(state_id, time)
                    a = Abstract_Source(time)
                    q.extend(e.run())
                    q.extend(a.run())
                    q = sorted(q, key=lambda x: x.time)
                    count = 0

                    while(len(q) > 0):
                        event = q.pop(0)
                        # if event.time > last_time:
                        #     last_time += 1
                        #     print(str(count) + " :: " + event.to_string())
                        # print(F"before first execute {event.to_string()}, event.")
                        event_list = event.execute()
                        for e in event_list:
                            # print(F"After first execute, looping through new event items {e.to_string()}")
                            
                            q_bar = q[count + 1:] #? q_bar = remaining items in master queue
                            # print(F"q_bar length {len(q_bar)}")
                            pos = count + 1 #? grab position of next item in master queue
                            for item in q_bar: # loop through items in master queue
                                # print(F"After first execute, looping through q_bar items {item.to_string()}")
                                if item.time > e.time: # make sure each next event item in master queue happens AFTER current event
                                    break
                                pos += 1
                            # print(F"position: {pos}")
                            q.insert(pos, e)
                        # q.extend(event_list)
                        # q = sorted(q, key=lambda x: x.time)
                        # print(F"count before +1: {count}")
                        count += 1

                    count_rate_a, count_rate_b, coincidence_rate = cm.calculate()
                    # print("BASIS " + alice + bob + " : Count Rate for Alice = " + str(count_rate_a) + " :: " + " Count Rate for Bob = " + str(count_rate_b) + " :: Co-incidence Clicks = " + str(coincidence_rate))
            chsh_val = cm.calculate_bell_inequality()
            chsh[angle*180/np.pi] = chsh_val
            print("Angle: " + str(round(angle*180/np.pi, 2)) + " :: CHSH Value: " + str(chsh_val))
        #print(F"Angles: {angles}")
        print(F"CHSH Witness Results: {chsh}")
    else:
        basis_states = ["H", "V"]
        all_basis_states = []

        for alice in basis_states:
            for bob in basis_states:
                last_time = 0

                all_basis_states.append(alice + bob)
                Receiver.set_basis(alice, bob)
                Receiver.last_ping_time = {"A": 0, "B": 0}
                cm.basis = alice + bob
                q = []
                e = Entanglement_Source(state_id, time)
                a = Abstract_Source(time)
                q.extend(e.run())
                q.extend(a.run())
                q = sorted(q, key=lambda x: x.time)
                count = 0

                while(len(q) > 0):
                    event = q.pop(0)
                    # if event.time > last_time:
                    #     last_time += 1
                    #     print(str(count) + " :: " + event.to_string())
                    # print(F"before first execute {event.to_string()}, event.")
                    event_list = event.execute()
                    for e in event_list:
                        # print(F"After first execute, looping through new event items {e.to_string()}")
                        
                        q_bar = q[count + 1:] #? q_bar = remaining items in master queue
                        # print(F"q_bar length {len(q_bar)}")
                        pos = count + 1 #? grab position of next item in master queue
                        for item in q_bar: # loop through items in master queue
                            # print(F"After first execute, looping through q_bar items {item.to_string()}")
                            if item.time > e.time: # make sure each next event item in master queue happens AFTER current event
                                break
                            pos += 1
                        # print(F"position: {pos}")
                        q.insert(pos, e)
                    # q.extend(event_list)
                    # q = sorted(q, key=lambda x: x.time)
                    # print(F"count before +1: {count}")
                    count += 1
                    # if count == 1000:
                    #     exit()
                count_rate_a, count_rate_b, coincidence_rate = cm.calculate()
                print("BASIS " + alice + bob + " : Count Rate for Alice = " + str(count_rate_a) + " :: " + " Count Rate for Bob = " + str(count_rate_b) + " :: Co-incidence Clicks = " + str(coincidence_rate))
        print("Fidelity = " + str(cm.calculate_fidelity()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--state", choices=[0, 1, 2, 3], type=int, help="Input Entangled State")
    parser.add_argument("-b", "--bell", action="store_true", help="Run Bell Inequality Test")
    parser.add_argument("-t", "--time", type=float, help="Simulation Run Time")
    args = parser.parse_args()
    state = 0
    time = 30
    test_bell = False
    if args.state:
        state = args.state
    if args.bell:
        test_bell = True
    if args.time:
        time = args.time
    string = "State = " + str(state) + " :: Time = " + str(time)
    if test_bell:
        string = string + " :: Scenario - Bell Inequality Test"
    print(string)
    main(state, test_bell, time)
