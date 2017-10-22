import re
from DBItem import DBItem

class Score_Author( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )

        self.scoreId = None
        self.composerId = None
        self.composition_year = None
        self.genre = None
        self.key = None
        self.incipit = None
        self.composer = None

        for line in string.split('\n'):
            composer = re.match("Author:(.*)", line)
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
            if composer != None:
                self.composer = composer.group(1).strip()

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

        self.cursor.execute(selectString,(parameters))
        res = self.cursor.fetchone()
        if not res is None:
            self.scoreId = res[0]


        self.cursor.execute("select id from person where name = ?  ", (self.composer,))
        res = self.cursor.fetchone()
        if not res is None:
            self.composerId = res[0]

    def fetch_id(self):
        self.cursor.execute("select id from score_author where score = ? and composer = ? ", (self.scoreId, self.composerId))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        print("storing score author ")
        self.cursor.execute("insert into score_author (score, composer) values (?, ?)", (self.scoreId, self.composerId))
