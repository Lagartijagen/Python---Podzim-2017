import numpy
import re

matrix = numpy.loadtxt('matrix.txt', usecols=range(3))
print("\n", matrix)
print("\n", numpy.linalg.det(matrix))
print("\n", numpy.linalg.inv(matrix))

coefficients = numpy.loadtxt('coefficients.txt', usecols=range(1))
print("\n", coefficients)
solution = numpy.linalg.solve(matrix, coefficients)
print("\n", solution)

rMatrix = []
rCoeficients = []

for line in open('equasion.txt', 'r', encoding='utf-8'):
    print(line)
    singleeq = line.split('=', 1)
    left = re.findall(r"([-]{0,1}[ ]*[0-9]*[a-z])", singleeq[0].replace(" ", ""))
    right = re.findall(r"([0-9]+)", singleeq[1].replace(" ", ""))

    i = 0
    pLeft = []
    for entry in left:
        if (re.search(r"([0-9]+)", entry)) is not None:
            pLeft.append(int(re.findall(r"([-]{0,1}[0-9]+)", entry)[0]))
        else:
            if (re.search(r"(-)", entry)) is not None:
                pLeft.append(-1)
            else:
                pLeft.append(1)

    pRight = []
    for entry in right:
        pRight.append(int(entry[0]))

    rMatrix.insert(i, pLeft)
    rCoeficients.insert(i, pRight)
    i =+ 1

a = numpy.asanyarray(rMatrix)
b = numpy.asanyarray(rCoeficients)

rSolution = numpy.linalg.solve((rMatrix), (rCoeficients))

resval = ['x','y','z','a']
ending = ""
i=0
for line in rSolution:
    print(resval[i], " = ", line[0])
    i =+ 1