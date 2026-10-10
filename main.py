import math
import itertools

class Convex_Polygons:

    def isConvex(self):
        v = self.vertices
        n = self.n
# check1
        if(len(v) != len(set(v))): return False

# check2
        if(n < 3): return False

        iter_vertices = itertools.cycle(self.vertices)
        sum = 0
        i = 0
        fir = next(iter_vertices)
        sec = next(iter_vertices)
        thir = next(iter_vertices)
        while i < n:
            newAngle = self.calc_angle(fir, sec, thir)
            if(newAngle == 180):
                return False
            sum += newAngle
            fir = sec
            sec = thir
            thir = next(iter_vertices)
            i += 1
        if math.isclose(sum, 180*(n-2), abs_tol=1e-6):
            return True
        else:
            return False

    @classmethod
    def calc_angle(cls, p1, p2, p3):
        a = (p1[0] - p2[0], p1[1] - p2[1])  # вектор p2-p1
        b = (p3[0] - p2[0], p3[1] - p2[1])  # вектор p2-p3
        vect_prod = abs(a[0] * b[1] - a[1] * b[0])   # модуль векторного произведения    
        scal_prod = a[0] * b[0] + a[1] * b[1]   # скалярного произведения
        phi =  math.degrees( math.atan2(vect_prod, scal_prod) )
        return phi


    # @classmethod
    # def calc_angle(cls, p1, p2, p3):
    #     '''Считаем угол в очередности p1, p2 и p3'''
    #     a = math.dist(p1, p2)
    #     b = math.dist(p2, p3)
    #     c = math.dist(p1, p3)

    #     if math.isclose(a+b, c, abs_tol=1e-6):
    #         return 180

    #     return math.degrees(math.acos((a**2 + b**2 - c**2)/(2*a*b)))

    @classmethod
    def calc_square_triangle(cls, p1, p2, p3):
        '''Возвращает площадь треугольника через векторное произведение'''
        return abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2

    def calc_square(self):
        list_triangles = self.triangulate()
        square = 0
        for tr in list_triangles:
            square += self.calc_square_triangle(tr[0], tr[1], tr[2])
        return square

    def calc_perimeter(self):
        v = self.vertices
        n = self.n
        iterVertices = itertools.cycle(v)
        fir = next(iterVertices)
        sec = next(iterVertices)
        ans = 0
        for i in range (n):
            ans += math.dist(sec, fir)
            fir = sec
            sec = next(iterVertices)
        return ans


    def __init__(self, vertices):
        self.vertices = vertices
        self.n = len(vertices)
        self.flag_convex = self.isConvex()

        if not self.isConvex():
            raise ValueError("многоугольник невыпуклый или вырожденный")
    
        # if(self.flag_convex):
        #     print("This is convex")
        # else:
        #     print("This is non-convex")


    def triangulate(self):    # для выпуклого!
        n = self.n
        v = self.vertices
        ans = []
        # [p1, p2, p3, p4, p5, p6, p7]
        for i in range(1, n-1):
            ans.append([v[0], v[i], v[i+1]])
        return ans


poly = Convex_Polygons([(0, 0), (1, 2), (3, 9)])

v1 = [(0, 0), (1, 2), (5, 6)]

v2 = [(0, 0), (4, 0), (4, 4), (0, 4)]

v3 = [(0, 0), (0, 4), (4, 4), (4, 0)]
v4 = [(0, 0), (4, 2), (0, 4), (1, 2)]
v5 = [(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)]

v6 = [(0, 0), (1, 1), (2, 2)]

v7 = [(0, 0), (4, 0), (4, 4), (0, 4)]

v8 = [(0,0), (4,0), (4,0), (0,4)]

for x in (v1, v2, v3, v4, v5, v6, v7, v8):
    try:
        poly = Convex_Polygons(x)
    except ValueError as e:
        print("отвергнут:", e)
    else:
        print("площадь:", poly.calc_square())
        print("триангуляция:", poly.triangulate())

