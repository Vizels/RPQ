import pandas as pd


class RPQ:
    def __init__ (self, data_set : int):
        name = "data." + str(data_set)
        
    

data_sets = ("data.1", "data.2", "data.3", "data.4")


chosen_data = data_sets[0]

data = []

with open("rpq.data.txt") as f:
    content = f.readlines()
    for index, line_data in enumerate(content):
        if chosen_data in line_data:
            rows_num = int(content[index + 1])
            break
    
    data_list = content[index + 2 : index + 2 + rows_num]
    
    for i in range(len(data_list)):
        data_list[i] = list(map(int, data_list[i][:-1].split(' ')))

    data = data_list
    # s (czas rozpoczęcia operacji = max{r,t}, gdzie t = czas zakończenia poprzedniej operacji, r = czas dojazdu aktualnej operacji)

df = pd.DataFrame(data, columns = ["r", "p", "q"])

print(df)

default_order = list(range(0, rows_num))

print(*default_order, sep=' ')

t = 0
Cmax = 0
for i in default_order:
    t = max(df['r'][i], t) + df['p'][i]

    if (t + df['q'][i]) > Cmax:
        Cmax = t + df['q'][i] 

print(Cmax)



