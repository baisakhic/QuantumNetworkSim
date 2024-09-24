import math
import sys


class Coincidence_Monitor():
    N = 2 #TODO - make dynamic
    dark_count_rate = 1000
    efficiency = .1
    co_incidence_window = 1.0/10**9
    basis = ""
    basis_map = {}
    bell_inequality = {}
    photons_A = []
    photons_B = []


    def handle_receive_data_event(self, event):
        # print("Handle receive data")
        #TODO calculation
        sender = event.get_sender()
        if sender == "A":
            self.photons_A.append(event)
        elif sender == "B":
            self.photons_B.append(event)
        return []


    def calculate(self):
        count_rate_A = len(self.photons_A)
        count_rate_B = len(self.photons_B)
        coincidence_clicks = 0

        A = self.photons_A
        B = self.photons_B
        for itemA in A:
            timeA = itemA.get_time()
            remove_b = False
            remove_b_item = None
            for itemB in B:
                timeB = itemB.get_time()
                if math.fabs(timeA - timeB) <= self.co_incidence_window:
                    if itemA.value != -1 and itemB.value != -1:
                        d = {}
                        if self.basis in self.bell_inequality.keys():
                            d = self.bell_inequality[self.basis]
                        key = str(itemA.value) + str(itemB.value)
                        no = 1
                        if key in d.keys():
                            no = d[key]+1
                        d[key] = no
                        self.bell_inequality[self.basis] = d
                        #print(self.basis + " :: " + key + " : " + str(no))
                        #print(self.bell_inequality)
                        # coincidence_clicks += 1
                        # if itemA.entanglement:
                        #     aliceStr = "Entangled Photon"
                        # else:
                        #     aliceStr = "Dark Count Photon"
                        #
                        # if itemB.entanglement:
                        #     bobStr = "Entangled Photon"
                        # else:
                        #     bobStr = "Dark Count Photon"


                        #print("Alice - " + aliceStr + " :: Bob - " + bobStr)
                        # self.bell_inequality.pop("-1-1")
                        #self.basis_map[self.basis] = coincidence_clicks
                    remove_b = True
                    remove_b_item = itemB
                    break
            if remove_b:
                B.remove(remove_b_item)
                continue
        self.photons_A = []
        self.photons_B = []
        return count_rate_A, count_rate_B, coincidence_clicks


    def calculate_fidelity(self):
        numerator = 0
        denominator = 0
        for basis in self.basis_map.keys():
            #TODO - Calculate validity
            if basis in ["HH", "VV"]:
                numerator += self.basis_map[basis]
            denominator += self.basis_map[basis]
        return numerator/denominator*100

    def calculate_bell_inequality(self):
        chsh = 0
        #print(self.bell_inequality)
        simple_map = {"Z": '0', "X": '1'}
        total_shots = sum(self.bell_inequality["XX"][y] for y in self.bell_inequality["XX"])
        for basis in self.bell_inequality:
            elements = self.bell_inequality[basis]
            for element in elements:
                parity = (-1) ** (int(element[0]) + int(element[1]))
                chsh += parity * elements[element]
            # parity = (-1)**(int(simple_map[element[0]])+int(simple_map[element[1]]))
            # if element == "ZZ":
            #     chsh += parity*self.basis_map[element]
            # if element == "ZX":
            #     chsh += parity*self.basis_map[element]
            # if element == "XZ":
            #     chsh -= parity*self.basis_map[element]
            # if element == "XX":
            #     chsh += parity*self.basis_map[element]
        #print(F"Total value for CHSH: {chsh}")
        #print(F"After division of shots: {chsh/total_shots}")
        # need to calculate chsh for each angle, so clear the basis_map after we do it each time
        self.basis_map.clear()
        self.bell_inequality.clear()
        if total_shots is None or total_shots == 0:
            return 0
        return chsh/total_shots