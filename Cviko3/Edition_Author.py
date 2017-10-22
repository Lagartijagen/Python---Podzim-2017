import re
from DBItem import DBItem

class Edition_Author( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )

        self.editionId = None
        self.editorId = None
        self.scoreId = None
        self.genre = None
        self.key = None
        self.incipit = None
        self.composer = None
        self.editor = None
        self.year = None
        self.composition_year = None

        for line in string.split('\n'):
            editor = re.match("Author:(.*)", line)
            year = re.match("Publication Year:(.*)", line)
            name = re.match("Edition:(.*)", line)
            genre = re.match("Genre:(.*)", line)
            key = re.match("Key:(.*)", line)
            composition_year = re.match("Composition Year:(.*)", line)
            incipit = re.match("Incipit:(.*)", line)
            if genre != None:
                self.genre = genre.group(1).strip()
            if key != None:
                self.key = key.group(1).strip()
            if composition_year != None:
                self.composition_year = composition_year.group(1).strip()
            if incipit != None:
                self.incipit = incipit.group(1).strip()
            if editor != None:
                self.editor = editor.group(1).strip()
            if year != None:
                self.year = year.group(1).strip()
            if name != None:
                self.name = name.group(1).strip()

        selectString = "Select id from score where "
        parameters = []
        if self.composition_year == None:
            selectString += "year is null "
        else:
            selectString += "year = ? "
            parameters += [self.composition_year]
        if self.genre == None:
            selectString += "and genre is null "
        else:
            selectString += "and genre = ? "
            parameters += [self.genre]
        if self.key == None:
            selectString += "and key is null "
        else:
            selectString += "and key = ? "
            parameters += [self.key]
        if self.incipit == None:
            selectString += "and incipit is null"
        else:
            selectString += "and incipit = ?"
            parameters += [self.incipit]

        self.cursor.execute(selectString, (parameters))
        res = self.cursor.fetchone()
        if not res is None:
            self.scoreId = res[0]

        selectString2 = "Select id from edition where "
        parameters2 = []
        if self.name == None:
            selectString2 += "name is null "
        else:
            selectString2 += "name = ? "
            parameters2 += [self.name]
        if self.year == None:
            selectString2 += "and year is null "
        else:
            selectString2 += "and year = ? "
            parameters2 += [self.year]

        selectString2 += "and score = ? "
        parameters2 += [self.scoreId]

        self.cursor.execute(selectString2, (parameters2))
        res =  self.cursor.fetchone()
        if not res is None:
            self.editionId = res[0]

        self.cursor.execute("select id from person where name = ?  ", (self.editor,))
        res = self.cursor.fetchone()
        if not res is None:
            self.editorId = res[0]

    def fetch_id(self):
        self.cursor.execute("select id from edition_author where edition = ? and editor = ? ", (self.editionId, self.editorId))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        print("storing edition editor ")
        self.cursor.execute("insert into edition_author (edition, editor) values (?, ?)", (self.editionId, self.editorId))
