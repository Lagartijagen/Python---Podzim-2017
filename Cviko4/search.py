import sqlite3
import json
import sys
from operator import itemgetter
from pathlib import Path


def main():
    script = sys.argv[0]
    composer = sys.argv[1]
    #composer = "Bach"
    musicDict = {}
    tempDict = {}

    sqlfile = Path("scorelib.dat")
    if sqlfile.is_file() == 1:
        conn = sqlite3.connect('scorelib.dat')
        cursor = conn.cursor()
    else:
        print("scorelib.dat is missing!")

    cursor.execute("select print.id, person.name, score.genre, score.key, score.incipit, score.year from person "
                   "join score_author on person.id = score_author.composer "
                   "join score on score_author.score = score.id "
                   "join edition on score.id = edition.score "
                   "join print on edition.id = print.edition "
                   "where person.name like ? ", ('%'+composer+'%',) )
    result = cursor.fetchall()
    if result != []:
        for row in result:
            #key = "'Print': '" + str(row[0]) + "'"
            tempDict[row[0]] = {'Composer': row[1], 'Genre:': row[2], 'Key': row[3], 'Incipit': row[4], 'Year': row[5]}
            musicDict['Print'] = tempDict
    else:
        print("no result")

    for k, v in musicDict.items():
        print(k, v)

    with open('search.json', 'w') as fp:
        print(json.dump(musicDict, fp))

if __name__ == '__main__':
    main()