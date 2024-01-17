
import json
import os

dir = os.listdir('../static/images/babs2')

lan_dic = {
    'F' : "fr",
    'I' : "it",
    "D" : "de"
}

id_range = slice(0,3)
lang_range = slice(4,5)
name_range = slice(6,None)
max_id = 117

files = []
for file in dir:
    files.append((file[id_range],
                  lan_dic[file[lang_range]],
                  file[name_range].split('.png')[0])
                )

#sort names by id and language
files.sort(key=lambda x: x[1])
files.sort(key=lambda x: x[0])

json_dic = {}
for id in range(0,max_id):
    string_id = str(id).zfill(3)
    icon_dic={}
    list = []
    for f in files:
        if(f[0]==string_id):
            list.append(f)
            icon_dic[f[1]]=(f[2])
    if(list):
        json_dic["ICON_"+string_id]=icon_dic

with open("../static/images/babs_2_dictionary.json", "w") as outfile:
    json.dump(json_dic, outfile, indent=4)
