#!/usr/bin/env python3
class Point:
    """Defines a point in 2D.

    >>> p = Point(3,5)
    >>> p.x
    3
    >>> p.y
    5
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """Returns the string representation of a point.

        >>> p = Point(3,5)
        >>> p
        Point(3,5)
        """
        return "Point({},{})".format(self.x,self.y)

class Rect:
    """Defines a rectangle in 2D.

    >>> r = Rect(3, 1, 5, 7)
    >>> r.top
    3
    >>> r.bottom
    1
    >>> r.left
    5
    >>> r.right
    7
    """
    
    def __init__(self, top, bottom, left, right):
        assert left <= right
        assert bottom <= top
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    @staticmethod
    def bounding(points):
        """Computes the bounding box of a set of points.

        >>> points = [Point(1,2), Point(3,4)]
        >>> br = Rect.bounding(points)
        >>> br.top
        4
        >>> br.bottom
        2
        >>> br.left
        1
        >>> br.right
        3
        """
        min_x = min(points, key=lambda p: p.x).x
        min_y = min(points, key=lambda p: p.y).y
        max_x = max(points, key=lambda p: p.x).x
        max_y = max(points, key=lambda p: p.y).y
        return Rect(max_y, min_y, min_x, max_x)

class Quadtree:
    """A tree which splits the points into 4 quadrants.

    Quadrants:
    1|0
    -+-
    2|3

    >>> points = []
    >>> points.append(Point(1,1))
    >>> points.append(Point(1,2))
    >>> points.append(Point(2,1))
    >>> points.append(Point(2,2))
    >>> q = Quadtree(points)
    >>> q.quadrants[0].point
    Point(2,2)
    >>> q.quadrants[1].point
    Point(1,2)
    >>> q.quadrants[2].point
    Point(1,1)
    >>> q.quadrants[3].point
    Point(2,1)
    """
    
    def __init__(self, points, br = None):
        """Initializes a Quadtree.

        >>> points = []
        >>> points.append(Point(1,1))
        >>> points.append(Point(1,4))
        >>> points.append(Point(4,1))
        >>> points.append(Point(4,4))
        >>> points.append(Point(2,2))
        >>> points.append(Point(2,3))
        >>> points.append(Point(3,2))
        >>> points.append(Point(3,3))
        >>> q = Quadtree(points)
        """
        self.empty = True
        self.br = br

        if br == None:
            self.br = Rect.bounding(points)

        if len(points) == 1:
            self.point = points[0]

        if len(points) > 1:
            self.empty = False
            self.splitx = (self.br.left + self.br.right)/2
            self.splity = (self.br.top + self.br.bottom)/2
            quadrants = [[], [], [], []]
            for p in points:
                if p.x <= self.splitx:
                    if p.y <= self.splity:
                        quadrants[2].append(p)
                    else:
                        quadrants[1].append(p)
                else:
                    if p.y <= self.splity:
                        quadrants[3].append(p)
                    else:
                        quadrants[0].append(p)
            self.quadrants = [Quadtree(quadrants[0], Rect(self.br.top,
                                                          self.splity,
                                                          self.splitx,
                                                          self.br.right)),
                              Quadtree(quadrants[1], Rect(self.br.top,
                                                          self.splity,
                                                          self.br.left,
                                                          self.splitx)),
                              Quadtree(quadrants[2], Rect(self.splity,
                                                          self.br.bottom,
                                                          self.br.left,
                                                          self.splitx)),
                              Quadtree(quadrants[3], Rect(self.splity,
                                                          self.br.bottom,
                                                          self.splitx,
                                                          self.br.right))]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
