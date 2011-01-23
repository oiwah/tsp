#!/usr/bin/python
# -*- coding: utf-8 -*-

from TSP import TSP
import time

ber52 = TSP('kroA100')
cities = ber52.readFile()
distMap = ber52.createDistMap(cities)

toList = ber52.optimalDist(cities)
ber52.prettyPrint(toList, distMap)
print

t1 = time.time()
(toList, totalDist) = ber52.greedyOne(cities)
t2 = time.time()
print t2 - t1, 'sec'
ber52.prettyPrint(toList, distMap)
print "totalDistance is ", totalDist
print

t1 = time.time()
(toList, totalDist) = ber52.greedyTwo(cities)
t2 = time.time()
print t2 - t1, 'sec'
ber52.prettyPrint(toList, distMap)
print "totalDistance is ", totalDist
print

t1 = time.time()
(toList, totalDist) = ber52.localSearch(cities, distMap, ber52.greedyOne)
t2 = time.time()
print t2 - t1, 'sec'
ber52.prettyPrint(toList, distMap)
print "totalDistance is ", totalDist
print

t1 = time.time()
(toList, totalDist) = ber52.localSearch(cities, distMap, ber52.greedyTwo)
t2 = time.time()
print t2 - t1, 'sec'
ber52.prettyPrint(toList, distMap)
print "totalDistance is ", totalDist
print

t1 = time.time()
(toList, totalDist) = ber52.kbestDP(cities, distMap)
t2 = time.time()
print t2 - t1, 'sec'
ber52.prettyPrint(toList, distMap)
print "totalDistance is ", totalDist
print
