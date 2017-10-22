import sqlite3
import re
from Person import Person
from Score import Score
from Voice import Voice
from pathlib import Path
from Edition import Edition
from Score_Author import Score_Author
from Edition_Author import Edition_Author
from Print import Print

def main():

    # Database and table creation
    sqlfile = Path("scorelib.dat")
    if sqlfile.is_file() == 0:
        conn = sqlite3.connect('scorelib.dat')
        cursor = conn.cursor()
        f = open("scorelib.sql")
        full_sql = f.read()
        sql_commands = full_sql.split(';')
        for sql_command in sql_commands:
            cursor.execute(sql_command)
            print(sql_command)
        cursor.close()
    else:
        conn = sqlite3.connect('scorelib.dat')


    def getAuthors(string):
        composers = []
        editors = []

        for line in string.split('\n'):
            composer = re.match("Composer:(.*)", line)
            editor = re.match("Editor:(.*)", line)
            if composer != None:
                composers.append(re.sub( '\([0-9/+-]+\)', '', composer.group(1) ).strip())
            if editor != None:
                editors.append(re.sub( '\([0-9/+-]+\)', '', editor.group(1) ).strip())

        for composer in composers:
            #print("insertString", (string + "\nAuthor:" + composer ))
            Score_Author(conn, (string + "\nAuthor:" + composer)).store()
        for editor in editors:
            #print("insertString", (string + "\nAuthor:" + editor ))
            Edition_Author(conn, (string + "\nAuthor:" + editor)).store()

    # Process a single line of input.
    def process(k, v):
        #Person Table
        global insertString, voice1, voice2
        if k == 'Composer':
            insertString = "INSERT STRING START"
            voice1=""
            voice2=""
            for c in v.split(';'):
                p = Person(conn, c.strip())
                p.store()
                insertString += "\nComposer:" + c.strip()
        if k == 'Editor':
            p = Person(conn, v.strip())
            p.store()
            insertString += "\nEditor:" + v
        #Score Table
        if k == 'Genre':
            insertString += "\nGenre:" + v
        if k == 'Key':
            insertString += "\nKey:" + v
        if k == 'Composition Year':
            insertString += "\nComposition Year:" + v
        if k == 'Incipit':
            insertString += "\nIncipit:" + v
            #push it in!
            Score(conn, insertString).store()
            if voice1 != "":
                Voice(conn, (insertString + voice1)).store()
            if voice2 != "":
                Voice(conn, (insertString + voice2)).store()
            Edition(conn, insertString).store()
            getAuthors(insertString)
            Print(conn, insertString).store()
        #Voice Table
        if k == 'Voice 1':
            voice1 = "\nVoice 1:" + v
        if k == 'Voice 2':
            voice2 = "\nVoice 2:" + v
        if k == 'Voice 3':
            voice2 = "\nVoice 3:" + v
        #Edition Table
        if k == 'Publication Year':
            insertString += "\nPublication Year:" + v
        if k == 'Edition':
            insertString += "\nEdition:" + v
        #Print Table
        if k == 'Partiture':
            insertString += "\nPartiture:" + v



    # Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
    rx = re.compile(r"(.*): (.*)")
    for line in open('scorelib.txt', 'r', encoding='utf-8'):
        m = rx.match(line)
        if m is None: continue
        process(m.group(1), m.group(2))

    conn.commit()
    conn.close()
    print("\nAll done.. ")

if __name__ == '__main__':
    main()