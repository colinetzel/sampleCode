# Colin Etzel
# Written for Python 2.7.12
# Execution: python powerPageRank.py graph.txt

# Runs pagerank algorithm on supplied graph.txt
# graph.txt nodes are newline-delimited
# graph.txt edges are space-delimited after the node ID (1st number is node)
#IE:
#<nodeID> <edge1> <edge2> \n
#<nodeID2> <edge1> <edge2>

# hardcoded values:
# teleportation probability = 0.15
# Uses power method with 5 iterations
# 5 maximum outgoing edges per node



import numpy as np
import sys


def main():
    if(len(sys.argv) != 2):
        print("Usage: powerPageRank.py <graphTextFile>")
        return
    try:
        sourceFile = open(sys.argv[1],"r")
    except:
        print("Invalid input file.")
        return
    nodes = []
    maxEdges = 5 # maximum outgoing edges per node
    alpha = 0.15 # teleport probability
    numIterations = 5
    adjacencyMap = {}
    for line in sourceFile:
        myLine = line.rstrip()
        myLine = myLine.split("\t")
        toEdge = myLine[1:]
        if(myLine[0] != ""):
            adjacencyMap[myLine[0]] = toEdge
            nodes.append(myLine[0])

    numNodes = len(nodes)
    sourceFile.close()
    workMatrix = np.zeros((len(nodes), len(nodes)))

    
    for node in nodes: #rows
        if adjacencyMap[node] == []: #no buddies!
            for i in range(numNodes): #columns
                workMatrix[nodes.index(node)][i] = 1/float(numNodes)
        else:
            numEdges = len(adjacencyMap[node])
            curEdges = adjacencyMap[node]
            for edge in curEdges:
                workMatrix[nodes.index(node)][nodes.index(edge)] = 1/float(numEdges)*(1-alpha)
            teleportFraction = alpha/float(numNodes)
            for i in range(numNodes):
                workMatrix[nodes.index(node)][i] += teleportFraction

    currentMatrix = workMatrix;
    for i in range(numIterations):
        currentMatrix = np.dot(currentMatrix, workMatrix)

    distributions = {}

    for i in range(numNodes):
        mySum = 0
        for j in range(numNodes):
            mySum += currentMatrix[j][i]
        distributions[nodes[i]] = mySum
        
    q = 1
    print("\nRank: Node: Score")
    for key, value in sorted(distributions.iteritems(), key = lambda (k,v): (v,k), reverse = True):
        print "%i: %s: %s" % (q, key, value)
        q += 1
        if q > 10:
            break


main()