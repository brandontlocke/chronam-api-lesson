#!/usr/bin/env python

import json

with open('chronamresults.json') as json_file:
    data = json.load(json_file)
    for p in data['items']:
        filename = p['date']+'_'+p['title']+'_'+"pg"+p['page']
        file = open(filename.replace(" ", "").replace(".", "")+".txt", "w")
        file.write(p['ocr_eng'])
file.close()
