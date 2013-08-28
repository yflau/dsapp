"""An implementation of kD trees."""
import sys

class KDTree:
    """A 2-dimension tree that is used to quickly find the nearest
    neighbour of a point on a 2D plane.
    
    METHODS
    "nearest_neighbor": Find the nearest neighbour of a point.
    
    ATTIBUTES
    "tree": The kD tree as a 3-tupple
            "(median, leftSubtree, rightSubtree)"."""
    
    def __init__(self, points):
        """Create a new kD tree.
	
        ARGUMENTS
        "points": A list of 2-tuples ("(x, y)") that represents the
                  points on the 2D plane."""
         
        # Preconditions: There is more than one point, and each point
        #   is a 2-tuple
        assert len(points) > 1
        for point in points:
            assert len(point) == 2

        newPoints = self.__uniq(points)
        self.tree = self.__build_tree_r(0, newPoints)

    def __uniq(self, list):
        """Crate a list without duplicate elements

        ARGUMENTS
        "list": A list that may contian duplicate elements.

        RETURNS
        A new list that does not contain any duplicates present in
        "list"."""
        newList = []
        for i in list:
            if i not in newList:
                newList.append(i)

        assert len(newList) <= len(list)
        return newList

    def __build_tree_r(self, depth, points):
        """Recursively build the
        kD tree using a depth-first algorithm. Recursion finishes when the
        number of points reaches 0 or 1 (a leaf).
        
        ARGUMENTS
        "depth": The current depth for the tree.
        "points": The list of points.

        RETURNS
        A node as a 2-tuple: "(value, (leftChild, rightChild))" or a
        leaf as a 2-tuple: "(x-value, y-value)"."""
        if len(points) == 0:
            return ()
        elif len(points) == 1:
            # If the number of points is one, we create a leaf
            assert len(points[0]) == 2
            return points[0]
        
        assert len(points) > 1
	
        # The depth of the tree is used to determine weather we
	#   partition on x (a vertical partition) or y (a horizontal
	#   partition).
        if (depth % 2 == 0):
            # Even Depth: Partition on x
            median, pointsTuple = self.__partition_x(points)
        else:
            # Odd Depth: Partition on y
            median, pointsTuple = self.__partition_y(points)

        leftPoints, rightPoints = pointsTuple

	# Return the a 2-tuple that represents the node. The first
	#   value is the median, the second value is a 2-tuple of the
	#   children. The first child is a list of all nodes less
	#   than the median, the second child is a list of all nodes
	#   greater than or equal to the median value.
        leftChildren = self.__build_tree_r(depth + 1,
                                           leftPoints)
        rightChildren = self.__build_tree_r(depth + 1,
                                            rightPoints)
        return (median, leftChildren, rightChildren)
    
    def __partition_x(self, points):
        """Partiton "points" into two sets based on the median
	x-value.
        
	ARGUMENTS
	"points": A list of points.
        
	RETURNS
	A 2-tuple of points: "(points < median, points >= median)"."""
        
        assert len(points) > 0
        
	# Sort the points by their x-values. The median is the middle
	#   value. 
        points.sort(self.__cmp_by_x)
        medianPoint = len(points)/2
	splitValue = points[medianPoint][0]
        # The following "if" is needed to ensure the points are split
        # into two groups in the event of a "triange" of points such
        # as [(2,2), (4,2), (4,4)] or [(8,5), (8,6), (9,5)]. If this
        # is not done infinite recursion can result. Thanks to Greg
        # Ewing.
        if splitValue == points[0][0]:
            splitValue = splitValue + 1
        # Split the points according to the median value.
        pointsLT, pointsGT = self.__split(splitValue, points, 0)
        
        return (splitValue, (pointsLT, pointsGT))

    def __partition_y(self, points):
        """Partiton "points" into two sets based on the median
	y-value.

	ARGUMENTS
	"points": A list of points.

	RETURNS
	A 2-tuple of points: "(points < median, points >= median)"."""

        assert len(points) > 0

        points.sort(self.__cmp_by_y)
        medianPoint = len(points)/2
	splitValue = points[medianPoint][1]
        # The following "if" is needed to ensure the points are split
        # into two groups in the event of a "triange" of points such
        # as [(2,2), (4,2), (4,4)] or [(8,5), (8,6), (9,5)] If this
        # is not done infinite recursion can result. Thanks to Greg
        # Ewing.
        if splitValue == points[0][1]:
            splitValue = splitValue + 1
        # Split the points according to the median value.
        pointsLT, pointsGT = self.__split(splitValue, points, 1)

        return (splitValue, (pointsLT, pointsGT))

    
    def __split(self, value, sortedPoints, index):
        """Split the points into two sets based on a value
        
        ARGUMENTS
        "value": The value used to split the points.
        "sortedPoints": A list tuples sorted by "index".
        "index": Which value of the tuples to compare.
        
        RETURNS
        A tuple of tuples less than value, and greater than value."""
        if len(sortedPoints) == 0:
            return [[],[]]
        
        head = sortedPoints[0]
        tail = sortedPoints[1:]
        
        if (head[index] < value):
            lt, gt = self.__split(value, tail, index)
            retval = [[head] + lt, gt]
        else:
            retval = [[], sortedPoints]
        return retval

    def __cmp_by_x(self, point1, point2):
	"""Compare points by their x-value.  This method is used to
	sort the list of points.

	ARGUMENTS
	"point1": The first point to compare.
	"point2": The second point to compare.

	RETURNS
	1 if the x-value of "point1" is greater than the x-value of
	"point2", 0 if both points are equal, or -1 otherwise."""
        assert len(point1) == 2
        assert len(point2) == 2
        
        x1 = point1[0]
        x2 = point2[0]
        
        if x1 > x2:
            retval = 1
        elif x1 == x2:
            retval = 0
        else:
            retval = -1

        assert retval in (1, 0, -1)
        return retval

    def __cmp_by_y(self, point1, point2):
	"""Compare points by their y-value.  This method is used to
	sort the list of points.
	
	ARGUMENTS
	"point1": The first point to compare.
	"point2": The second point to compare.

	RETURNS
	1 if the x-value of "point1" is greater than the x-value of
	"point2", 0 if both points are equal, or -1 otherwise."""
        assert len(point1) == 2
        assert len(point2) == 2
        
        y1 = point1[1]
        y2 = point2[1]
        
        if y1 > y2:
            retval = 1
        elif y1 == y2:
            retval = 0
        else:
            retval = -1

        assert retval in (1, 0, -1)
        return retval

    def nearest_neighbor(self, point):
        """Find the nearest neighbour to "point"

        ARGUMENTS
        "point": a 2-tuple "(x, y)".

        RETURNS
        A 2-tuple "(x, y)" that is the nearest point in the kD tree to
        "point"."""

        assert len(point) == 2
        assert len(self.tree) == 3

        xValue, yValue = point
        nearest = self.__nearest_neighbour_search(self.tree,
                                                  xValue, yValue)
        assert len(nearest) == 2
        return nearest
        
    def __nearest_neighbour_search(self, tree, lValue, rValue):
        if len(tree) < 3:
            return tree
        assert len(tree) == 3

        medianValue = tree[0]
        if lValue < medianValue:
            subtree = tree[1]
        else:
            assert lValue >= medianValue
            subtree = tree[2]

        # This is no mistake, the left and right values are swapped on
        #   each recursion. This saves having to record the depth, and
        #   having to do a comparison. Credit for this idea goes to
        #   Jason Smith (no relation).
        retval = self.__nearest_neighbour_search(subtree,
                                                 rValue, lValue)
        # Some internal nodes may only have one child, and we could
        #   have picked the
        if len(retval) == 0:
            if len(tree[1]) == 0:
                subtree = tree[2]
            elif len(tree[2]) == 0:
                subtree = tree[1]
            retval = self.__nearest_neighbour_search(subtree,
                                                 rValue, lValue)
        assert len(retval) == 2
        return retval

if __name__ == '__main__':
    import random, timeit
    
    maxPoints = 1024
    xMax = 1280
    yMax = 1024

    r = random.Random()
    points = []
        
    for i in range(0, maxPoints):
        point = (r.randint(0, xMax), r.randint(0, yMax))
        points.append(point)
    #points=[(6, 1), (5, 5), (9, 6), (3, 6), (4, 9), (4, 0), (7, 9), (2, 9)]
    #sys.stderr.write('Building tree for points\n\t%s\n' % points)
    
    sys.stderr.write('Building Tree... ')
    tree = KDTree(points)
    sys.stderr.write('Done\n')
    #sys.stderr.write('Tree:\n\t%s\n' %tree)
    #sys.stderr.write('Tree as tupple:\n\t%s\n' % (tree.tree,))

    searchPoint = (r.randint(0, xMax), r.randint(0, yMax))
    #searchPoint = (5, 4)
    sys.stderr.write('Nearest neighbour to %s in the tree is... ' %\
                     (searchPoint,))
    nearestPoint = tree.nearest_neighbor(searchPoint)
    sys.stderr.write('%s\n' % (nearestPoint,))

    numTimes = 1000000
    stmt = 'tree.nearest_neighbor(%s)' % (searchPoint,)
    setup = 'from __main__ import KDTree; tree = KDTree(%s)' % points
    sys.stderr.write('Timing search... ')
    timer = timeit.Timer(stmt, setup)
    sec = timer.timeit(numTimes)
    sys.stderr.write('Done (%fs/search)\n' % (sec/numTimes,))
