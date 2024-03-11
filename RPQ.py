import pandas as pd
import numpy as np

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


    def calculate_Cmax(self):
        """
        s (czas rozpoczęcia operacji) = max{r,t}, gdzie
        t = czas zakończenia poprzedniej operacji,
        r = czas dojazdu aktualnej operacji
        """

        t = 0
        Cmax = 0
        for i in self.order:
            t = max(self.dataframe['r'][i], t) + self.dataframe['p'][i]

            if (t + self.dataframe['q'][i]) > Cmax:
                Cmax = t + self.dataframe['q'][i] 

        self.Cmax = Cmax

        print(f"Cmax = {Cmax}")


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
        

    def set_calculated_as_default(self):
        self.order = self.calculated_order




        
            

if __name__ == "__main__":
    rpq = RPQ(4)

    rpq.print_order(rpq.order)
        
    rpq.calculate_Cmax()  

    rpq.sortRQ()  

    rpq.print_order(rpq.calculated_order)

    rpq.set_calculated_as_default()

    rpq.calculate_Cmax()



