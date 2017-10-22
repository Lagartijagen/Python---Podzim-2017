import re
from DBItem import DBItem

class Print( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )

        self.partiture = "N"
        self.editionId = None
        self.year = None
        self.composition_year = None
        self.scoreId = None
        self.genre = None
        self.key = None

        for line in string.split('\n'):
            partiture = re.match("Partiture:(.*)", line)
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
            if partiture != None:
                self.partiture = re.sub('\(partial\)', 'P', re.sub('\(yes\)', 'Y', re.sub('\(no\)', 'N', partiture.group(1)))).strip()
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

    def fetch_id(self):
        fetchQuery = "select id from print where "
        fetchParam = []
        if self.partiture == None:
            fetchQuery += "partiture is null "
        else:
            fetchQuery += "partiture = ? "
            fetchParam += [self.partiture]
        if self.editionId == None:
            fetchQuery += "and edition is null "
        else:
            fetchQuery += "and edition = ? "
            fetchParam += [self.editionId]
        self.cursor.execute(fetchQuery, (fetchParam))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        print("storing print")
        self.cursor.execute("insert into print (partiture, edition) values (?, ?)", (self.partiture, self.editionId))
