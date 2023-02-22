import pandas as pd

Section = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Y']
LinkDataframe = pd.DataFrame(columns=['Link', 'Section'])


for S in Section:
    #### Load in Datasets from the large text files
    with open(f'C:/Users/eeo21/Documents/Startup_Datasets/CPC_Classifications_List/cpc-section-{S}_20220801.txt') as f:
        lines = f.readlines()

    for line in lines:
        Line_Elements = line.split("\t")





