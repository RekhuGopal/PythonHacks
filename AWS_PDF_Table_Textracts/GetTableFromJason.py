# Python program to read
# json file


import json
from operator import contains
from trp import Document

# Opening JSON file
f = open('F:\RekhuAll\GitRepos\PythonHacks\AWS_PDF_Table_Textracts\Sample1_MarkedUp.json')

# returns JSON object as
# a dictionary
data = json.load(f)

doc = Document(data)

for page in doc.pages:
    for table in page.tables:
        print((page.tables).index(table))
        Table = []
        for r, row in enumerate(table.rows):
            rowst = {}
            i = 0
            for c, cell in enumerate(row.cells):
                if (page.tables).index(table) == 1 and (table.rows).index(row) > 1 :
                    print((table.rows)[1])
                    #rowst[((table.rows)[1].cells)[i]] = cell
                if (page.tables).index(table) == 0 and (table.rows).index(row) > 0 :
                    print((table.rows)[0])
                    #rowst[((table.rows)[1].cells)[i]] = cell
                i +=1
                Table.append(rowst)
        print(Table)
            

# Closing file
f.close()
