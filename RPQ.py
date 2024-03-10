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
        print("Default order:")
        
        for i in order:
            print(order[i]+1, end = " ")

        print()
        # print("Order: ", *order, sep=' ')
        

    

if __name__ == "__main__":
    rpq = RPQ(1)

    rpq.print_order(rpq.default_order)
        
    rpq.calculate_Cmax()    