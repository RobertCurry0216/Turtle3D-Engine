if __name__ == '__main__':
    import Shapes2D
else:
    from Shapes import Shapes2D

from math import sin, cos, tan, radians, sqrt
from turtle import *


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
        a = cos(theta)
        b = sin(theta)
        return [
            [1,0,0,0],
            [0,a,b,0],
            [0,-b,a,0],
            [0,0,0,1]
        ]

    @staticmethod
    def rot_y(theta):
        a = cos(theta)
        b = sin(theta)
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
    def z(self):
        return self._coords[2]

    @z.setter
    def z(self, z):
        self._coords[2] = z

    def by_matrix(self, m):
        x = self.x * m[0][0] + self.y * m[1][0] + self.z * m[2][0] + m[3][0]
        y = self.x * m[0][1] + self.y * m[1][1] + self.z * m[2][1] + m[3][1]
        z = self.x * m[0][2] + self.y * m[1][2] + self.z * m[2][2] + m[3][2]
        w = self.x * m[0][3] + self.y * m[1][3] + self.z * m[2][3] + m[3][3]

        if w != 0:
            return Vector3D(x/w, y/w, z/w)
        else:
            print('div by 0')
            return Vector3D(x, y, z)

    def cross(self, other):
        pass
        

class Triangle3D:
    def __init__(self, p1, p2, p3):
        self._points = [
            Vector3D(*p1),
            Vector3D(*p2),
            Vector3D(*p3)
        ]
        self._normal_dot_product = 0

    def __repr__(self):
        p1 = '{}, {}, {}'.format(*self._points[0])
        p2 = '{}, {}, {}'.format(*self._points[1])
        p3 = '{}, {}, {}'.format(*self._points[2])
        return f'{self.__class__.__name__}(({p1}), ({p2}), ({p3}))'

    def __getitem__(self, item):
        return self._points[item]

    def draw(self, camera, colour=None, wireframe=False):
        """ Draws the triangle to the screen using the given turtle from the camera"""
        p1, p2, p3 = self
        norm = self.normal
        if norm.dot(self[0] - camera.location) < 0 or wireframe:
            if colour:
                # shading
                dp = norm.dot(camera.light_direction)
                #print(dp)

                shaded_col = tuple(max(int(c * dp), 0) for c in colour)

                # draw the triangle
                camera.pu()
                camera.goto(p1.x, p1.y)
                camera.color(shaded_col)
                camera.begin_fill()
                camera.pd()
                camera.goto(p2.x, p2.y)
                camera.goto(p3.x, p3.y)
                camera.goto(p1.x, p1.y)
                camera.end_fill()
                camera.pu()
            else:
                camera.pu()
                camera.goto(p1.x, p1.y)
                camera.pd()
                camera.goto(p2.x, p2.y)
                camera.goto(p3.x, p3.y)
                camera.goto(p1.x, p1.y)
                camera.pu()

    def by_matrix(self, m):
        """ proforms matrix multiplications on all points with the given matrix """
        p1, p2, p3 = self
        return Triangle3D(
            p1.by_matrix(m),
            p2.by_matrix(m),
            p3.by_matrix(m)
        )

    def project(self):
        return self.by_matrix(Matrix.proj())

    def translate(self, vector):
        return Triangle3D(
            self[0] + vector,
            self[1] + vector,
            self[2] + vector,
        )
    
    def scale(self, *nums):
        return Triangle3D(
            self[0] * nums[0],
            self[1] * nums[1],
            self[2] * nums[2],
        )

    @property
    def normal(self):
        """ Returns a unit vector of the triangles face """
        a = self[1] - self[0]
        b = self[2] - self[0]
        x = (a.y * b.z) - (a.z * b.y)
        y = (a.z * b.x) - (a.x * b.z)
        z = (a.x * b.y) - (a.y * b.x)
        n = sqrt(x*x + y*y + z*z)

        return Vector3D(x/n, y/n, z/n)


class Camera(Turtle):
    def __init__(self, x=0, y=0, z=0):
        super().__init__()
        self.location = Vector3D(x, y, z)
        self.ht()
        self.shape(None)
        self.speed(0)
        self.light_direction = Vector3D(0,0.5,-1)

    @property
    def light_direction(self):
        return self._light_direction_vector

    @light_direction.setter
    def light_direction(self, vec):
        """ Normalizes the light direction vector """
        x, y, z = vec
        l = sqrt(x*x + y*y + z*z)
        self._light_direction_vector = Vector3D(x/l, y/l, z/l)
        return True


if __name__ == '__main__':
    from turtle import *
    import time
    start_time = time.time()

    cam = Camera(0,0,0)
    wn = cam.screen
    wn.setup(800, 800)
    wn.bgcolor(0,0,0)
    wn.colormode(255)
    wn.tracer(0)
    wn.title('Turtle3D Engine')
    
    cube = [
        # south face
        Triangle3D([0,0,0],[0,1,0],[1,1,0]),
        Triangle3D([0,0,0],[1,1,0],[1,0,0]),

        # east face
        Triangle3D([1,0,0],[1,1,0],[1,1,1]),
        Triangle3D([1,0,0],[1,1,1],[1,0,1]),

        # north face
        Triangle3D([1,0,1],[1,1,1],[0,1,1]),
        Triangle3D([1,0,1],[0,1,1],[0,0,1]),

        # west face
        Triangle3D([0,0,1],[0,1,1],[0,1,0]),
        Triangle3D([0,0,1],[0,1,0],[0,0,0]),

        # top face
        Triangle3D([0,1,0],[0,1,1],[1,1,1]),
        Triangle3D([0,1,0],[1,1,1],[1,1,0]),

        # bottom face
        Triangle3D([1,0,1],[0,0,1],[0,0,0]),
        Triangle3D([1,0,1],[0,0,0],[1,0,0])
    ]

    cam = Camera(0,0,0)
    while True:
        cam.clear()
        theta = time.time() - start_time
        for tri in cube:
            tri.by_matrix(Matrix.rot_x(theta))\
                .by_matrix(Matrix.rot_z(theta / 2))\
                .translate(Vector3D(0,0,4))\
                .project()\
                .scale(600, 600, 600)\
                .draw(cam, (255,255,255))
        wn.update()

