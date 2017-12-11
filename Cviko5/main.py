import json
from bokeh.plotting import figure, show
from pprint import pprint
from numpy import pi
from bokeh.models import ColumnDataSource
import random
from operator import *
from collections import OrderedDict

#randomColor = ("#%06x" % random.randint(0, 0xFFFFFF))

electionResults = {}

with open('election.json') as data_file:
    data = json.load(data_file)
#pprint(data)

shorts = []
votes = []
color = []
name = []


for party in data:
    partyDict = {}
    try:
        #shorts.append(party['short'])
        partyDict['short'] = party['short']
    except KeyError:
        #shorts.append((party['name'])[:10])
        partyDict['short'] = ((party['name'])[:10])
    #votes.append(party['votes'])
    partyDict['votes'] = party['votes']
    try:
        #color.append(party['color'])
        partyDict['color'] = party['color']
    except KeyError:
        #color.append('#000000')
        partyDict['color'] = ("#%06x" % random.randint(0, 0xFFFFFF))
    #name.append(party['name'])
    partyDict['name'] = party['name']
    electionResults[party['number']] = partyDict

print(electionResults)

#sortedElections = sorted(electionResults.items(), key=lambda x:getitem(x[1],'votes'))
#sortedElections = OrderedDict(sorted(electionResults.items(), key=lambda x:[0][3], reverse=True))
#pprint(sortedElections)


for key, val in electionResults.items():
    votes.append(val['votes'])
    shorts.append(val['short'])
    color.append(val['color'])
    name.append(val['name'])

src = ColumnDataSource( data = {
    'labels': labels,
    'scores' : scores,
    'starts' : starts,
    'ends' : ends,
    'colors' : colors} )


output_file("pie2.html")
p = figure
p.wedge =

p = figure( x_range = shorts )
p.vbar( x = shorts , top = votes, width = 0.5, fill_color = color )
p.xaxis.major_label_orientation = 1
show( p )


