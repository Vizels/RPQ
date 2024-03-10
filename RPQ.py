import pandas as pd

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


        self.default_order = list(range(0, rows_num))

        self.dataframe = pd.DataFrame(data, columns = ["r", "p", "q"])


    def calculate_Cmax(self):
        """
        s (czas rozpoczęcia operacji) = max{r,t}, gdzie
        t = czas zakończenia poprzedniej operacji,
        r = czas dojazdu aktualnej operacji
        """

        t = 0
        Cmax = 0
        for i in self.default_order:
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
        # print("Order: ", *order, sep=' ')
        

    def find_optimal_order(self):
        sorted_by_r = self.dataframe.sort_values(by = 'r')

        sorted_by_q = self.dataframe.sort_values(by = 'q', ascending = False)

        print(sorted_by_r)#, sorted_by_q, sep = '\n')
 
        #create a dictionary with indexes of the rows in the dataframe and empty values
        weights = dict.fromkeys(range(len(self.dataframe)), 0)
        print(weights)

        for i in range(self.rows_num):
            r, q = sorted_by_r.index[i], sorted_by_q.index[i]

            weights[r] += i
            #weights[q] += i
        
        print(weights)
        
        #sort the dictionary by values
        sorted_weights = sorted(weights.items(), key = lambda x: x[1])
        print(sorted_weights)
        
        #print only the indexes of the rows
        #print([x[0] for x in sorted_weights])

        self.actual_order = [x[0] for x in sorted_weights]
        print(self.actual_order)
            

if __name__ == "__main__":
    rpq = RPQ(1)

    rpq.print_order(rpq.default_order)
        
    rpq.calculate_Cmax()  

    rpq.find_optimal_order()  

    rpq.print_order(rpq.actual_order)