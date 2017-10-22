import re
from DBItem import DBItem

class Voice( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )

        self.voiceNumber = None
        self.scoreId = None
        self.name = None
        self.genre = None
        self.key = None
        self.composition_year = None
        self.incipit = None

        for line in string.split('\n'):
            v1 = re.match("Voice 1:(.*)", line)
            v2 = re.match("Voice 2:(.*)", line)
            v3 = re.match("Voice 3:(.*)", line)
            genre = re.match("Genre:(.*)", line)
            key = re.match("Key:(.*)", line)
            composition_year = re.match("Composition Year:(.*)", line)
            incipit = re.match("Incipit:(.*)", line)
            if v1 != None:
                self.name = re.sub('\(Voice 1:\)', '', v1.group(1)).strip()
            if v2 != None:
                self.name = re.sub('\(Voice 2:\)', '', v2.group(1)).strip()
            if v3 != None:
                self.name = re.sub('\(Voice 3:\)', '', v3.group(1)).strip()
            if genre != None:
                self.genre = genre.group(1).strip()
            if key != None:
                self.key = key.group(1).strip()
            if composition_year != None:
                self.composition_year = composition_year.group(1).strip()
            if incipit != None:
                self.incipit = incipit.group(1).strip()


        if re.search( "Voice 1:", string):
            self.voiceNumber = 1
        if re.search( "Voice 2:", string):
            self.voiceNumber = 2
        if re.search( "Voice 3:", string):
            self.voiceNumber = 3

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

    def fetch_id(self):
        fetchQuery = "select id from voice where "
        fetchParam = []
        if self.voiceNumber == None:
            fetchQuery += "number is null "
        else:
            fetchQuery += "number = ? "
            fetchParam += [self.voiceNumber]
        if self.scoreId == None:
            fetchQuery += "and score is null "
        else:
            fetchQuery += "and score = ? "
            fetchParam += [self.scoreId]
        if self.name == None:
            fetchQuery += "and name is null"
        else:
            fetchQuery += "and name = ? "
            fetchParam += [self.name]

        self.cursor.execute(fetchQuery,(fetchParam))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]


    def do_store(self):
            print("storing voice ")
            self.cursor.execute("insert into voice (number, score, name) values (?, ?, ?)", (self.voiceNumber, self.scoreId, self.name))
