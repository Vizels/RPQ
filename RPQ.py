import pandas as pd
import numpy as np
import time

class RPQ:
    def __init__ (self, data_set : int):
        name = "data." + str(data_set)
    
        data = []
        with open("rpq.data.txt") as f:
            content = f.readlines()
            for index, line_content in enumerate(content):
                if name in line_content:
                    rows_num = int(content[index + 1])
                    break
            
            data = content[index + 2 : index + 2 + rows_num]
            
        self.rows_num = rows_num

        for i in range(len(data)):
            # remove '\n' from the end of the line and split data by space
            data[i] = list(map(int, data[i][:-1].split(' ')))


        self.order = list(range(0, rows_num))

        self.dataframe = pd.DataFrame(data, columns = ["r", "p", "q"])


    def calculate_Cmax(self, order = None):
        """
        s (czas rozpoczęcia operacji) = max{r,t}, gdzie
        t = czas zakończenia poprzedniej operacji,
        r = czas dojazdu aktualnej operacji
        """
        is_print = False

        if order == None:
            is_print = True
            order = self.order

        t = 0
        Cmax = 0
        for i in order:
            t = max(self.dataframe['r'][i], t) + self.dataframe['p'][i]

            if (t + self.dataframe['q'][i]) > Cmax:
                Cmax = t + self.dataframe['q'][i] 

        self.Cmax = Cmax

        if is_print:
            print(f"Cmax = {Cmax}")

        return Cmax


    def print_order(self, order):
        print("Order:")

        for i in order:
            print(i+1, end = " ")

        print()
        # print("Order: ", *order+1)#, sep=' ')
        

    def sortR(self):
        sorted_by_r = self.dataframe.sort_values(by = 'r')

        # create a dictionary with indexes of the rows in the dataframe and empty values
        calculated_order = []
        
        for i in range(self.rows_num):
            r = sorted_by_r.index[i]
            calculated_order.append(r)
    
        self.calculated_order = calculated_order

        return calculated_order
    
    def sortRQ(self):
        sorted_by_r = self.dataframe.sort_values(by = ['r'])
        sorted_by_q = self.dataframe.sort_values(by = ['q'], ascending = False)

        new_order = []

        while len(sorted_by_r) > 0 and len(sorted_by_q) > 0:

            r = sorted_by_r.index[0]
            sorted_by_r.drop(r, inplace=True)
            sorted_by_q.drop(r, inplace=True)

            q = sorted_by_q.index[0]
            sorted_by_q.drop(q, inplace=True)
            sorted_by_r.drop(q, inplace=True)

            new_order.extend((r,q))


        self.calculated_order = new_order
    
    def Schrage(self):
        dataR = self.sortR()
        ready = []  # Initialize ready queue
        t = 0       # Initialize time
        order = []  # Initialize order list
        last = min(dataR, key=lambda x: self.dataframe.loc[x, 'q'])
        dataR.remove(last)
        
        while dataR or ready:
            while dataR and self.dataframe.loc[dataR[0], 'r'] <= t:  # Add tasks whose release time has passed to the ready queue
                ready.append(dataR.pop(0))

            if not ready:  # If no tasks are ready, move time to the next available task's release time
                t = self.dataframe.loc[dataR[0], 'r']
                continue

            # Choose the task with the highest q value from the ready queue
            max_q_task = max(ready, key=lambda x: self.dataframe.loc[x, 'q'] - self.dataframe.loc[x, 'p'])
            ready.remove(max_q_task)  # Remove chosen task from ready queue
            order.append(max_q_task)  # Add chosen task to order list

            t += self.dataframe.loc[max_q_task, 'p']

        order.append(last)
        
        
        return order

    def experimental_permutations_algorithm(self):
        # Complexity - O(n^3)

        #new_order = self.sortR()
        new_order = self.Schrage()

        actual_Cmax = self.calculate_Cmax(new_order)

        #print(self.dataframe['r'][0])
        for _ in range(len(new_order)):
            for i in range(len(new_order[0:-1])):
                new_order[i], new_order[i+1] = new_order[i+1], new_order[i]
                new_Cmax = self.calculate_Cmax(new_order)

                if new_Cmax > actual_Cmax:
                    new_order[i], new_order[i+1] = new_order[i+1], new_order[i]
                else:
                    actual_Cmax = new_Cmax
        
        self.calculated_order = new_order
        print(new_order)

        self.set_calculated_as_default()
        
        #self.calculate_Cmax()

    def set_calculated_as_default(self):
        self.order = self.calculated_order

        
            
def count_sum():
    sum = 0

    for i in range(1, 5):
        rpq = RPQ(i)
        
        time_start = time.time()
        rpq.experimental_permutations_algorithm()
        time_end = time.time()

        print(f"Time: {time_end - time_start}")

        sum += rpq.calculate_Cmax()

    print(sum)


#KZW_wt_13-15_lab1

if __name__ == "__main__":
    
    # rpq = RPQ(1)

    count_sum()

    pass
    



