import http.server
import json
import pprint
import socketserver
import sqlite3
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8000

class myHandler(http.server.SimpleHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):

        tempDict = {}
        musicDict = {}

        sqlfile = Path("scorelib.dat")
        if sqlfile.is_file() == 1:
            conn = sqlite3.connect('scorelib.dat')
            cursor = conn.cursor()
        else:
            message = "scorelib.dat is missing!"

        query_dict = parse_qs(urlparse(self.path).query)

        try:
            composer = str(query_dict['q']).strip('[]').strip("'")
            print(composer)
            cursor.execute(
                "select print.id, person.name, score.genre, score.key, score.incipit, score.year from person "
                "join score_author on person.id = score_author.composer "
                "join score on score_author.score = score.id "
                "join edition on score.id = edition.score "
                "join print on edition.id = print.edition "
                "where person.name like ? ", ('%' + composer + '%',))
            result = cursor.fetchall()
            if result != []:
                for row in result:
                    # key = "'Print': '" + str(row[0]) + "'"
                    tempDict[row[0]] = {'Composer': row[1], 'Genre:': row[2], 'Key': row[3], 'Incipit': row[4],
                                        'Year': row[5]}
                    musicDict['Print'] = tempDict

                    for k, v in musicDict.items():
                        print(k, v)

                    try:
                        datatype = str(query_dict['f']).strip('[]').strip("'")
                        if datatype == "json":
                            message = (json.dumps(musicDict))
                        elif datatype == "html":
                            htmlLines = []
                            for textLine in pprint.pformat(musicDict).splitlines():
                                htmlLines.append('<br/>%s' % textLine)
                                message = '\n'.join(htmlLines)
                    except KeyError:
                        print("data type is missing")
            else:
                message = "no result"

        except KeyError:
            message = "search query is missing"

        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return


try:
    with socketserver.TCPServer(("", PORT), myHandler) as httpd:
        httpd.serve_forever()


except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    httpd.socket.close()