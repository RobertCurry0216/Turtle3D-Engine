if __name__ == '__main__':
    import Shapes2D
else:
    from Shapes import Shapes2D
from math import sin, cos, tan, radians

class Matrix:
    @staticmethod
    def proj():
        f_near = 0.1
        f_far = 1000
        f_fov = 100
        f_aspect = 800 / 800
        f_fov_rad = 1 / tan(f_fov * 0.5 / 180.0 * 3.14159)

        a = f_aspect * f_fov_rad
        b = f_fov_rad
        c = f_far / (f_far - f_near)
        d = (-f_far * f_near) / (f_far - f_near)
        return[
            [a,0,0,0],
            [0,b,0,0],
            [0,0,c,1],
            [0,0,d,0]
        ]

    @staticmethod
    def rot_z(theta):
        a = cos(theta)
        b = sin(theta)
        return [
            [a,b,0,0],
            [-b,a,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

    @staticmethod
    def rot_x(theta):
        a = cos(theta / 2)
        b = sin(theta / 2)
        return [
            [1,0,0,0],
            [0,a,b,0],
            [0,-b,a,0],
            [0,0,0,1]
        ]

    @staticmethod
    def rot_y(theta):
        a = cos(theta / 2)
        b = sin(theta / 2)
        return [
            [a,0,b,0],
            [0,1,0,0],
            [-b,0,a,0],
            [0,0,0,1]
        ]


class Vector3D(Shapes2D.Vector):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self._coords.append(z)

    @property
    def Z(self):
        return self._coords[2]

    @Z.setter
    def Z(self, z):
        self._coords[2] = z

    def by_matrix(self, m):
        x = self.X * m[0][0] + self.Y * m[1][0] + self.Z * m[2][0] + m[3][0]
        y = self.X * m[0][1] + self.Y * m[1][1] + self.Z * m[2][1] + m[3][1]
        z = self.X * m[0][2] + self.Y * m[1][2] + self.Z * m[2][2] + m[3][2]
        w = self.X * m[0][3] + self.Y * m[1][3] + self.Z * m[2][3] + m[3][3]

        if w != 0:
            return Vector3D(x/w, y/w, z/w)
        else:
            print('div by 0')
            return Vector3D(x, y, z)
        

class Triangle3D:
    def __init__(self, p1, p2, p3, set_turtle=None):
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

        self._points = [
            Vector3D(*p1),
            Vector3D(*p2),
            Vector3D(*p3)
        ]

    def __repr__(self):
        p1 = '{}, {}, {}'.format(*self._points[0])
        p2 = '{}, {}, {}'.format(*self._points[1])
        p3 = '{}, {}, {}'.format(*self._points[2])
        return f'{self.__class__.__name__}([{p1}], [{p2}], [{p3}])'

    def __getitem__(self, item):
        return self._points[item]

    def draw(self, _turtle=None):
        p1, p2, p3 = self

        try:
            if _turtle == None:
                t = self._turtle
            else:
                t = _turtle
            draw_line(p1, p2, t)
            draw_line(p2, p3, t)
            draw_line(p3, p1, t)
        except Exception as e:
            print(e)

    def by_matrix(self, m):
        p1, p2, p3 = self
        return Triangle3D(
            p1.by_matrix(m),
            p2.by_matrix(m),
            p3.by_matrix(m)
        )

    def translate(self, vector):
        return Triangle3D(
            self[0] + vector,
            self[1] + vector,
            self[2] + vector,
            self._turtle
        )
    
    def scale(self, *nums):
        return Triangle3D(
            self[0] * nums[0],
            self[1] * nums[1],
            self[2] * nums[2],
            self._turtle
        )


def draw_line(sp, ep, _turtle, colour=(255,255,255)):
    x1, y1, *_ = sp
    x2, y2, *_ = ep
    _turtle.color(colour)
    _turtle.pu()
    _turtle.goto(x1, y1)
    _turtle.pd()
    _turtle.goto(x2, y2)
    _turtle.pu()


if __name__ == '__main__':
    from turtle import *
    import time
    start_time = time.time()


    t = Turtle()
    wn = Screen()
    wn.setup(800, 800)
    wn.bgcolor(0,0,0)
    wn.colormode(255)
    wn.tracer(0)
    wn.title('Turtle3D Engine')
    
    t.ht()
    t.shape(None)
    t.speed(0)
    t.width(1)

    cube = [
        # south face
        Triangle3D([0,0,0],[0,1,0],[1,1,0], set_turtle=t),
        Triangle3D([0,0,0],[1,1,0],[1,0,0], set_turtle=t),

        # east face
        Triangle3D([1,0,0],[1,1,0],[1,1,1], set_turtle=t),
        Triangle3D([1,0,0],[1,1,1],[1,0,1], set_turtle=t),

        # north face
        Triangle3D([1,0,1],[1,1,1],[0,1,1], set_turtle=t),
        Triangle3D([1,0,1],[0,1,1],[0,0,1], set_turtle=t),

        # west face
        Triangle3D([0,0,1],[0,1,1],[0,1,0], set_turtle=t),
        Triangle3D([0,0,1],[0,1,0],[0,0,0], set_turtle=t),

        # top face
        Triangle3D([0,1,0],[0,1,1],[1,1,1], set_turtle=t),
        Triangle3D([0,1,0],[1,1,1],[1,1,0], set_turtle=t),

        # bottom face
        Triangle3D([1,0,1],[0,0,1],[0,0,0], set_turtle=t),
        Triangle3D([1,0,1],[0,0,0],[1,0,0], set_turtle=t)
    ]

    while True:
        t.clear()
        theta = time.time() - start_time
        for tri in cube:
            tri.by_matrix(Matrix.rot_x(theta))\
                .by_matrix(Matrix.rot_y(theta))\
                .by_matrix(Matrix.rot_z(theta))\
                .translate(Vector3D(0,0,3))\
                .by_matrix(Matrix.proj())\
                .scale(300, 300, 300)\
                .draw(t)
        wn.update()

