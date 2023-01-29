import pandas as pd

def prepare_dataframe(filename):
    data=pd.read_excel(filename,sheet_name=None)
    return data

def infection_circle(data,infectedID):
    infectedID=str(infectedID)
    #print(data)
    infection_data=data[infectedID]
    #print(infection_data)
    final_dataframe=data[infectedID]
    
    for i in infection_data['person2']:
        i=str(i)
        if i in data:
            final_dataframe=final_dataframe.append(data[(i)])


    return final_dataframe

data=prepare_dataframe('Book1.xlsx')
final_dataframe=infection_circle(data,2)
final_dataframe.to_csv('infection.xlsx')