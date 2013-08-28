#!/usr/bin/python
import re
import sys
import math
import random
import operator
from bisect import insort
from bisect import bisect

/*
	Copyright 2010 Jason Berlinsky

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/ 

class Point:pass
class Node:
	#node.pointCount = len(points)
	#node.points = None
	#node.leftChild = None
	#node.rightChild = None
	def printOut(self,depth = 0):
		for i in range(0,depth):
			print "....",
		print "point count =", self.pointCount, "rect =", self.hyperRect.toString(), "points =",self.points
		if (self.leftChild is not None):
			for i in range(0,depth):
				print "....",
			print "left: "
			self.leftChild.printOut(depth+1)
		if (self.rightChild is not None):
			for i in range(0,depth):
				print "....",
			print "right: "
			self.rightChild.printOut(depth+1)
	def buildBoundingHyperRect(self,points):
		self.hyperRect = HyperRect()
		self.hyperRect.buildBoundingHyperRect(points)
 
def getFastDistance(a,b):
	dim = len(b);
	total = 0;
	for i in range(0,dim):
		delta = a[i] - b[i];
		total = total + (delta *delta)
	return total
 
class Neighbors:
	def add(self,node,query):
		for i in range(0,node.pointCount):
			dist = getFastDistance(node.points[i].data,query)
			if (dist < self.minDistanceSquared):
				item = [dist,node.points[i]]
				insort(self.points,item)
				if (len(self.points) > self.k):
					self.points = self.points[0:self.k]
 
		if (len(self.points) == self.k):
			self.minDistanceSquared = self.points[self.k-1][0]
		return;
 
class HyperRect:
	def buildBoundingHyperRect(self,points):
		self.k = len(points[0].data)
		self.dims  = range(0,self.k) 
		high = points[0].data[:]
		low = points[0].data[:]
		for i in range(0,len(points)):
			for j in self.dims:
				point = points[i].data[j]
				if (high[j]  < point):
					high[j] = point
				if (low[j] > point):
					low[j] = point	
		self.high = high
		self.low = low
		return 
 
	def getWidestDimension(self):
		widest =0
		widestDim =-1
		for i in self.dims:
			width = self.high[i] -  self.low[i]
			if (width > widest):
				widestDim =i
				widest = width
		self.widest = widest;
		self.widestDim = widestDim;	
		return self.widestDim
	def getWidestDimensionWidth(self):
		return self.widest
	def toString(self):
		return "high =",self.high,"low =",self.low,
	def getMinDistance(self,query):
		total = 0
		for i in self.dims:
			delta = 0.0
			if (self.high[i] < query[i]):
				delta = query[i] - self.high[i]
			elif (self.low[i] > query[i]):
				delta = self.low[i] - query[i]
			total = total + (delta*delta)
		return total;
def buildKdHyperRectTree(points,rootMin=3):
	global nodes;
	if (points is None or len(points) ==0):
		return None
	n = Node() # make a new node
	n.buildBoundingHyperRect(points) 	# build the hyper rect for these points
						# this will fight the top left and botom
						# right of all given points.
 
	leaf = len(points) <= rootMin; #check if this
	splitDim  = -1
 
	if (not leaf):
		splitDim = n.hyperRect.getWidestDimension()    # get the widest dimension to split n
						            	# to maximize splitting affect
		if (n.hyperRect.getWidestDimensionWidth() == 0.0): # do we have a bunch of children at the same point?
			left = True 
	#init the node
	n.pointCount = len(points)
	n.points = None
	n.leftChild = None
	n.rightChild = None
 
	if (leaf or len(points)==0):
		n.points = points # we are a leaf so just store all points in the rect
	else:
		points.sort(key=lambda points: points.data[splitDim]) # sort by the best split att
		median = len(points)/2 	# get the median
								# and split left for small, right for larger
		n.leftChild = buildKdHyperRectTree(points[0:(median+1)],rootMin)
		if (median +1 < len(points)):
			n.rightChild = buildKdHyperRectTree(points[median+1:], rootMin)
	return n;
 
def getKNN(query,node, neighbours,distanceSquared):	
	if (neighbours.minDistanceSquared > distanceSquared):
		if (node.leftChild is None):
			neighbours.add(node,query)
		else:
			distLeft = node.leftChild.hyperRect.getMinDistance(query)
			distRight = node.rightChild.hyperRect.getMinDistance(query)
 
			if (distLeft < distRight):
				getKNN(query,node.leftChild,neighbours,distLeft)
				getKNN(query,node.rightChild,neighbours,distRight)
			else:
				getKNN(query,node.rightChild,neighbours,distRight)
				getKNN(query,node.leftChild,neighbours,distLeft)
# Sample Implementation

dataset = []
# Create some 2-d points

n = 10
idx = 0

# Range for random values
a = -100#Min
b = 100	#Max

# Number of closest neighbors to find

KNN_DEPTH = 1


# Build some random points

for i in range(1,n):
	p = Point()
	p.data = [random.randint(a,b),random.randint(a,b)]
	p.baseIndex = idx
	idx+=1
	dataset.append(p)
	

kd = buildKdHyperRectTree(dataset[:], 10)

print "Finding the nearest "+str(KNN_DEPTH)+" neighbors of each element. . . "

for point in dataset:
	neighbors = Neighbors()
	neighbors.k = KNN_DEPTH+1
	neighbors.points = []
	neighbors.minDistanceSquared = float("infinity")
	getKNN(point.data,kd,neighbors,getFastDistance(kd.hyperRect.high,kd.hyperRect.low))
	name = str(point.baseIndex+1)
	answer = "Closest "+str((neighbors.k-1))+" point(s) to point '"+name+"': "
	for i in range(1,neighbors.k):	
		name = str(neighbors.points[i][1].baseIndex+1)
		answer = answer+" point '"+name+"'"
		if (i!=neighbors.k-1):
			answer= " point '"+answer+"',"
	print answer
