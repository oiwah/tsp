#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math

class TSP:
    """This is a class of many algos for solving TSP"""

    def __init__(self, filename):
        self.fn = filename

    def readFile(self):
        lineN = 0
        cities = []
        filename = self.fn + '.tsp'
        input = open(filename, 'r')

        for line in input.readlines():
            line = line.strip()
            if (line == "EOF"):
                break
            
            lineN = lineN + 1
            if (lineN < 7):
                if (lineN == 1):
                    print line
                continue
            else:
                city = line.split()
                cities.append(city)

        return cities

    def optimalDist(self, cities):
        filename = self.fn + '.opt.tour'
        lineN = 0
        
        if (filename == 'kroA100.opt.tour'):
            lineN = -1
        elif (filename == 'ts225.opt.tour'):
            print 'There is no opt tour file for ts225'
            return []

        input = open(filename, 'r')
        toList = [-1 for i in range(len(cities))]
        print len(toList)

        for line in input.readlines():
            line = line.strip()

            lineN = lineN + 1
            if (lineN == 5):
                start = int(line) -1
                pred = start
            elif (lineN > 5):
                if (int(line) ==  -1):
                    break

                to = int(line) - 1
                toList[pred] = to
                pred = to

        toList[pred] = start
        return toList

    def calcDist(self, i, j, cities):
        city1 = (float(cities[i][1]), float(cities[i][2]))
        city2 = (float(cities[j][1]), float(cities[j][2]))
        xdist = city1[0] - city2[0]
        ydist = city1[1] - city2[1]
        dist = math.sqrt(xdist * xdist + ydist * ydist)
        return int(round(dist))

    def createDistMap(self, cities):
        rlen = len(cities)

        distMap = []
        for i in range(rlen):
            distMapOfACity = []
            for j in range(rlen):
                dist = self.calcDist(i, j, cities)
                distMapOfACity.append(dist)
            distMap.append(distMapOfACity)
        return distMap

    def createDistList(self, cities, rlen):
        distList = []
        for i in range(rlen):
            distListOfACity = []
            for j in range(rlen):
                if (i == j):
                    continue
                dist = self.calcDist(i, j, cities)
                distListOfACity.append((dist, j))
            distListOfACity.sort()
            distList.append(distListOfACity)
        return distList

    def printTrans(self, to, totalDist, distTrans):
        print "->", to,
        distTrans = distTrans + " -> " + str(totalDist)
        return distTrans

    def prettyPrint(self, toList, distMap):
        if (len(toList) == 0):
            return

        distTrans = ""

        pred = 0
        to = toList[0]
        print pred, "->", to,
        totalDist = distMap[pred][to]
        distTrans = distTrans + str(totalDist)

        while (to != 0):
            pred = to
            to = toList[to]
            totalDist = totalDist + distMap[pred][to]
            distTrans = self.printTrans(to, totalDist, distTrans)
        print ""
        print distTrans
        return

    def greedyOne(self, cities):
        rlen = len(cities)
        distList = self.createDistList(cities, rlen)

        toList = [-1 for i in range(rlen)]
        state = set([0])

        cur = 0
        totalDist = 0

        for n in range(rlen - 1):
            for i in range(rlen - 1):
                cand = distList[cur][i]
                if (cand[1] not in state):
                    totalDist, toList[cur], cur = totalDist + cand[0], cand[1], cand[1]
                    state.add(cand[1])

        for i in range(rlen - 1):
            cand = distList[cur][i]
            if (cand[1] == 0):
                totalDist, toList[cur] = totalDist + cand[0], cand[1]

        return toList, totalDist

    def greedyTwo(self, cities):
        rlen = len(cities)
        distList = self.createDistList(cities, rlen)
    
        toList = [-1 for i in range(rlen)]
        state = set()
        totalDist = 0

        for cur in range(rlen - 1):
            for i in range(rlen - 1):
                judge = True
                cand = distList[cur][i]
                if (cand[1] in state):
                    continue

                to = toList[cand[1]]
                while (to != -1 and to != cur):
                    to = toList[to]
                    
                if (to == cur):
                    continue
            
                state.add(cand[1])
                totalDist, toList[cur] = totalDist + cand[0], cand[1]
                break

        for i in range(rlen - 1):
            cand = distList[rlen - 1][i]
            if (cand[1] not in state):
                totalDist, toList[rlen - 1] = totalDist + cand[0], cand[1]

        return toList, totalDist

    def localSearch(self, cities, distMap, greedy):
        (toList, totalDist) = greedy(cities)
        rlen = len(cities)

        for i in range(rlen):
            for j in range(rlen):
                if (i == j or i == toList[j]):
                    continue

                curDist = distMap[i][toList[i]] + distMap[j][toList[j]]
                candDist = distMap[i][j] + distMap[toList[i]][toList[j]]
                if (curDist > candDist):
                    totalDist = totalDist - (curDist - candDist)
                
                    toJ = toList[j]

                    pred2 = toList[i]
                    pred = toList[pred2]
                    while (pred != toJ):
                        next = toList[pred]
                        toList[pred] = pred2
                        pred2 = pred
                        pred = next

                    toList[toList[i]] = toJ
                    toList[i] = j
    
        return toList, totalDist

    def kbestDP(self, cities, distMap, k=1, prs=5):
        rlen = len(cities)
        distList = self.createDistList(cities, rlen)

        kbest = [[(0, set([start]), [-1 for i in range(rlen)], start)]
                 for start in range(rlen)]

        for iterN in range(rlen - 1):
            newkbest = [[] for i in range(rlen)]
            for cur in range(rlen):
                for lbest in range(len(kbest[cur])):
                    flg = 0
                    for i in range(rlen - 1):
                        if (flg + 1 > k):
                            break

                        start = kbest[cur][lbest]
                        to = distList[cur][i][1]
                        if (to in start[1]):
                            continue
                        newset = start[1].copy()
                        newset.add(to)
                        newToList = start[2] * 1
                        newToList[cur] = to
                        newstart = (start[0] + distList[cur][i][0],
                                    newset, newToList, start[3])
                        newkbest[to].append(newstart)
                        flg = flg + 1

            for i in range(rlen):
                newkbest[i].sort()
                newkbest[i] = newkbest[i][:prs]
            kbest = newkbest

        newkbest = [[] for i in range(rlen)]
        for cur in range(rlen):
            for lbest in range(len(kbest[cur])):
                start = kbest[cur][lbest]
                to = start[3]
                newToList = start[2] * 1
                newToList[cur] = to
                newstart = (start[0] + distMap[cur][to],
                            start[1], newToList, start[3])
                newkbest[to].append(newstart)

        for i in range(rlen):
            newkbest[i].sort()
            newkbest[i] = newkbest[i][:prs]
        kbest = newkbest
    
        tmpmin = sys.maxint
        minN = -1
        for i in range(rlen):
            if (len(kbest[i]) > 0):
                cand = kbest[i][0]
                if (tmpmin > cand[0]):
                    tmpmin = cand[0]
                    minN = i

        return kbest[minN][0][2], kbest[minN][0][0]
