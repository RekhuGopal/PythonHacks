# Python program to read
# json file


import json
from operator import contains
from trp import Document

# Opening JSON file
f = open('F:\RekhuAll\AWS\AWS_PDF_Table_Textracts\Sample1_MarkedUp.json')

# returns JSON object as
# a dictionary
data = json.load(f)

doc = Document(data)

for page in doc.pages: 
    for line in page.lines:
        for word in line.words:
            print(len(word))



'''
for page in doc.pages:
    for table in page.tables:
        print((page.tables).index(table))
        Table = []
        for r, row in enumerate(table.rows):
            i = 0
            rowst = {}
            for c, cell in enumerate(row.cells):
                if (page.tables).index(table) == 0 and (table.rows).index(row) > 0 :
                    rowst[str((table.rows)[0].cells[i])] = str(cell)
                if (page.tables).index(table) == 1 and (table.rows).index(row) > 1 :
                    rowst[str((table.rows)[1].cells[i])] = str(cell)
                i +=1
            if (page.tables).index(table) == 0 and (table.rows).index(row) > 0 :
                Table.append(rowst)
            if (page.tables).index(table) == 1 and (table.rows).index(row) > 1 :
                Table.append(rowst)
        print(Table)
'''            

# Closing file
f.close()
