"""
custom classes to detect intersection of line segments
see:
    https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    https://www.codeproject.com/tips/862988/find-the-intersection-point-of-two-line-segments
"""
import turtle


class Shape2D:
    def __init__(self, set_turtle=None):
        self._edges = []
        self._points = []
        if set_turtle == True:
            self._turtle = turtle.Turtle()
            self._turtle.ht()
            self._turtle.shape(None)
            self._turtle.speed(0)
            self._turtle.width(1)
        elif set_turtle:
            self._turtle = set_turtle
        else:
            self._turtle = None

    def __repr__(self):
        values = (str(j) for i in self._points for j in i.get())
        return f'{self.__class__.__name__}({", ".join(values)})'

    def __getitem__(self, item):
        return self._points[item]

    def draw(self, colour=None, _turtle=None):
        """ Draw shape with turtle module """
        if not _turtle:
            _turtle = self._turtle
            if not colour:
                colour = 'black'
        _turtle.color(colour)
        _turtle.begin_poly()

        _turtle.pu()
        _turtle.goto(*self._points[0])
        _turtle.pd()
        for p in self._points[1:]:
            _turtle.goto(*p)
        _turtle.goto(*self._points[0])
        _turtle.end_poly()
        _turtle.pu()


class Triangle(Shape2D):
    def __init__(self, *points, set_turtle=None):
        super().__init__(set_turtle)
        if len(points) == 3:
            self._points = points
        elif len(points) == 6:
            x1, y1, x2, y2, x3, y3 = points
            self._points = [
                Vector(x1, y1),
                Vector(x2, y2),
                Vector(x3, y3)
            ]
        else:
            raise ValueError('Unuseable values given')

        self._edges = [Line(p1, p2) for p1, p2 in zip(self._points, self._points[1:] + [self._points[0]])]


class Rectangle(Shape2D):
    def __init__(self, *points):
        super().__init__()
        if len(points) == 2:
            top_left, bottom_right = points
        elif len(points) == 4:
            x1, y1, x2, y2 = points
            top_left = [x1, y1]
            bottom_right = [x2, y2]
        else:
            raise ValueError('coordinates given are unuseable')

        if type(top_left) != Vector:
            top_left = Vector(*top_left)
        if type(bottom_right) != Vector:
            bottom_right = Vector(*bottom_right)

        top_right = Vector(bottom_right.X, top_left.Y)
        bottom_left = Vector(top_left.X, bottom_right.Y)

        self._points = [
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ]

        self._edges = [
            Line(top_left, top_right),
            Line(top_right, bottom_right),
            Line(bottom_right, bottom_left),
            Line(bottom_left, top_left),
        ]


class Line:
    def __init__(self, *points, set_turtle=None):
        self.startpoint = None
        self.endpoint = None
        self.set(*points)
        if set_turtle:
            self._turtle = set_turtle
        else:
            self._turtle = turtle.Turtle()
            self._turtle.ht()
            self._turtle.shape(None)
            self._turtle.speed(0)
            self._turtle.width(1)

    def set(self, *points):
        if len(points) == 2:
            startpoint, endpoint = points
        elif len(points) == 4:
            x1, y1, x2, y2 = points
            startpoint = [x1, y1]
            endpoint = [x2, y2]
        else:
            raise ValueError('coordinates given are unuseable')

        if type(startpoint) == Vector:
            self.startpoint = startpoint
        else:
            self.startpoint = Vector(*startpoint)

        if type(endpoint) == Vector:
            self.endpoint = endpoint
        else:
            self.endpoint = Vector(*endpoint)

    @property
    def ep(self):
        return self.endpoint

    @ep.setter
    def ep(self, point):
        self.endpoint = point

    @property
    def sp(self):
        return self.startpoint

    @sp.setter
    def sp(self, point):
        self.startpoint = point

    def get(self):
        return [self.sp.X, self.sp.Y, self.ep.X, self.ep.Y]

    def __repr__(self):
        return 'Line({}, {}, {}, {})'.format(
            self.sp.X,
            self.sp.Y,
            self.ep.X,
            self.ep.Y
        )

    def __getitem__(self, item):
        return [self.sp, self.ep][item]

    def intersect(self, other, overlap_as_intersect=False):

        def is_zero(a):
            zero = 1 ** (-10)
            return abs(a) < zero

        p = self.sp
        p2 = self.ep
        q = other.sp
        q2 = other.ep
        r = p2 - p
        s = q2 - q
        rxs = r.cross(s)
        qpxr = (q - p).cross(r)

        # If r x s = 0 and (q - p) x r = 0, then the two lines are collinear.
        if is_zero(rxs) and is_zero(qpxr):
            if overlap_as_intersect:
                # 1. If either  0 <= (q - p) * r <= r * r or 0 <= (p - q) * s <= * s
                # then the two lines are overlapping,
                if (0 <= q - p * r <= r * r) or (0 <= p - q * s <= s * s):
                    return True
            # 2. If neither 0 <= (q - p) * r = r * r nor 0 <= (p - q) * s <= s * s
            return False
        # 3. If r x s = 0 and (q - p) x r != 0, then the two lines are parallel and non-intersecting.
        if is_zero(rxs) and not is_zero(qpxr):
            return False

        t = (q - p).cross(s) / rxs
        u = (q - p).cross(r) / rxs

        # 4. If r x s != 0 and 0 <= t <= 1 and 0 <= u <= 1
        # the two line segments meet at the point p + t r = q + u s.
        if not is_zero(rxs) and (0 <= t <= 1) and (0 <= u <= 1):
            return p + (r * t)
        # 5. Otherwise, the two line segments are not parallel but do not intersect.
        return False

    def draw(self, colour=None, _turtle=None):
        if not _turtle:
            _turtle = self._turtle
        if not colour:
            colour = 'black'

        _turtle.color(colour)
        _turtle.pu()
        _turtle.goto(*self.sp)
        _turtle.pd()
        _turtle.goto(*self.ep)
        _turtle.pu()


class Vector:
    """
    used as the points in line segments
    adds vector functionallity for ease of use and readability
    """

    def __init__(self, x, y):
        self._coords = [x, y]

    @property
    def X(self):
        return self._coords[0]

    @X.setter
    def X(self, x):
        self._coords[0] = x

    @property
    def Y(self):
        return self._coords[1]

    @Y.setter
    def Y(self, y):
        self._coords[1] = y

    def get(self):
        return self._coords

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(str(a) for a in self._coords))

    def __add__(self, other):
        values = (a + b for a, b in zip(self._coords, other.get()))
        return self.__class__(*values)

    def __sub__(self, other):
        values = (a - b for a, b in zip(self._coords, other.get()))
        return self.__class__(*values)

    def __mul__(self, other):
        if type(other) == Vector:
            values = (a * b for a, b in zip(self._coords, other.get()))
        else:
            values = (a * other for a in self._coords)
        return self.__class__(*values)

    def __eq__(self, other):
        zero = 1 ** (-10)
        return all(abs(a - b) <= zero for a, b in zip(self.get(), other.get()))

    def __getitem__(self, item):
        return self._coords[item]

    def cross(self, other):
        return (self.X * other.Y) - (self.Y * other.X)


if __name__ == '__main__':
    from turtle import *
    from random import randint

    t = Turtle()
    t.screen.screensize(200, 200)
    t.screen.colormode(255)
    t.screen.tracer(0)

    t.ht()
    t.shape(None)
    t.speed(0)
    t.width(3)

    shapes = [
        Triangle(*(randint(-350, 350) for _ in range(6)), set_turtle=t) for _ in range(8)
    ]

    for shape in shapes:
        shape.draw()

    while True:
        t.screen.update()
