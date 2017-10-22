import re
from DBItem import DBItem

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.born = self.died = None
        self.name = re.sub( '\([0-9/+-]+\)', '', string ).strip()
        # extracting years of birth & death

        m = re.search( "([0-9]+)--([0-9]+)", string )
        if not m is None:
            self.born = int( m.group( 1 ) )
            self.died = int( m.group( 2 ) )

    def fetch_id(self):
        self.cursor.execute("select id from person where name = ?", (self.name,))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

            self.cursor.execute("select case when born is null then 1 else 0 end from person where name = ? ",(self.name,))
            born = self.cursor.fetchone()
            self.cursor.execute("select case when died is null then 1 else 0 end from person where name = ? ",(self.name,))
            died = self.cursor.fetchone()

            if born==1 and self.born != None:
                print("updating '%s'" % self.name)
                self.cursor.execute("update person set born = ? where name = ? ", (self.born, self.name))
            if died==1 and self.died != None:
                print("updating '%s'" % self.name)
                self.cursor.execute("update person set died = ? where name = ? ", (self.died, self.name))


    def do_store(self):
            print("storing person")
            self.cursor.execute("insert into person (name, born, died) values (?, ?, ?)", (self.name, self.born, self.died))
