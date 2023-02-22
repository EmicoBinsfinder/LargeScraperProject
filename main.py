import pandas as pd

Section = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Y']
LinkDataframe = pd.DataFrame(columns=['Link', 'Section'])


for S in Section:
    #### Load in Datasets from the large text files
    with open(f'C:/Users/eeo21/Documents/Startup_Datasets/CPC_Classifications_List/cpc-section-{S}_20220801.txt') as f:
        lines = f.readlines()

    for line in lines:
        Line_Elements = line.split("\t")
        ClassCode = Line_Elements[0]
        if len(ClassCode) <= 4:
            continue
        link = f'https://patents.google.com/xhr/query?url=q%3D{ClassCode}%26oq%3D{ClassCode}&exp=&download=true'
        entry = [link, ClassCode]
        LinkDataframe.loc[len(LinkDataframe)] = entry
        print(entry)

LinkDataframe.to_csv('Desktop')




