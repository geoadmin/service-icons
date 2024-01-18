
import json
import os
import pandas as pd

id_range = slice(0,3)
name_range = slice(6,None)

# read by default 1st sheet of an excel file
df = pd.read_excel('../../tmp/Namenliste.xlsx')
print(df)

json_dic = {}
for index, row in df.iterrows():
    string_id=row['D'][id_range]
    icon_dic={
                "de": row['D'][name_range].split('.svg')[0],
                "fr": row['F'][name_range].split('.svg')[0],
                "it": row['I'][name_range].split('.svg')[0]
              }
    json_dic["ICON_"+string_id]=icon_dic

with open("../json/babs_2_dictionary.json", "w") as outfile:
    json.dump(json_dic, outfile, indent=4)
