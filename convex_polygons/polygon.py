import math
import itertools

class Convex_Polygons:

    def isConvex(self):
        """Проверяет, что многоугольник выпуклый и невырожденный.
 
        Критерий: сумма неориентированных углов при вершинах равна
        180 * (n - 2). Многоугольник отвергается, если в нём меньше трёх
        вершин, есть совпадающие вершины или есть вершина с углом 180°
        (три подряд идущие вершины на одной прямой).
 
        Returns:
            bool: True, если многоугольник выпуклый, иначе False.
        """
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

    @staticmethod
    def calc_z_vect_prod(p1, p2, p3):
        """Считает z-компоненту векторного произведения векторов p2->p1 и p2->p3.
 
        Векторы строятся из средней точки p2. Знак результата показывает
        направление поворота при обходе p1 -> p2 -> p3.
 
        Args:
            p1 (tuple[float, float]): Первая точка.
            p2 (tuple[float, float]): Вершина, из которой строятся векторы.
            p3 (tuple[float, float]): Третья точка.
 
        Returns:
            float: Положительное число, если обход p1 -> p2 -> p3 идёт по
                часовой стрелке, отрицательное, если против, и 0, если точки
                лежат на одной прямой.
        """
        a = (p1[0] - p2[0], p1[1] - p2[1])  # вектор p2-p1
        b = (p3[0] - p2[0], p3[1] - p2[1])  # вектор p2-p3
        vect_prod = a[0] * b[1] - a[1] * b[0]
        return vect_prod
    
    @staticmethod
    def calc_scal_prod(p1, p2, p3):
        """Считает скалярное произведение векторов p2->p1 и p2->p3.
 
        Args:
            p1 (tuple[float, float]): Первая точка.
            p2 (tuple[float, float]): Вершина, из которой строятся векторы.
            p3 (tuple[float, float]): Третья точка.
 
        Returns:
            float: Скалярное произведение. Положительное для острого угла
                при p2, нулевое для прямого, отрицательное для тупого.
        """
        a = (p1[0] - p2[0], p1[1] - p2[1])  # вектор p2-p1
        b = (p3[0] - p2[0], p3[1] - p2[1])  # вектор p2-p3
        scal_prod = a[0] * b[0] + a[1] * b[1]   # скалярное произведение
        return scal_prod

    @staticmethod
    def set_order(vertices):
        """Приводит вершины к обходу против часовой стрелки.
 
        Args:
            vertices (list[tuple[float, float]]): Вершины выпуклого
                многоугольника в порядке обхода.
 
        Returns:
            list[tuple[float, float]]: Вершины в порядке против часовой
                стрелки.
        """
        '''Возвращает упорядоченный список вершин (т.е. порядок против часовой стрелки)'''
        p1, p2, p3 = vertices[0], vertices[1], vertices[2]
        vect_prod = Convex_Polygons.calc_z_vect_prod(p1, p2, p3)
        if vect_prod > 0:  # => по часовой стрелке расположены вершины => реверс списка
            vv = vertices[1:]
            return [vertices[0]] + vv[::-1]
        else:
            return vertices

    @staticmethod
    def calc_angle(p1, p2, p3):
        """Считает угол при вершине p2 между лучами p2->p1 и p2->p3.
 
        Args:
            p1 (tuple[float, float]): Первая точка.
            p2 (tuple[float, float]): Вершина угла.
            p3 (tuple[float, float]): Третья точка.
 
        Returns:
            float: Угол в градусах.
        """
        vect_prod = Convex_Polygons.calc_z_vect_prod(p1, p2, p3)   
        scal_prod = Convex_Polygons.calc_scal_prod(p1, p2, p3)
        phi =  math.degrees( math.atan2(abs(vect_prod), scal_prod) )
        return phi

    @staticmethod
    def calc_square_triangle(p1, p2, p3):
        """Считает площадь треугольника через векторное произведение.
 
        Args:
            p1 (tuple[float, float]): Первая вершина треугольника.
            p2 (tuple[float, float]): Вторая вершина треугольника.
            p3 (tuple[float, float]): Третья вершина треугольника.
 
        Returns:
            float: Площадь треугольника (неотрицательная).
        """
        return abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2

    

    def calc_square(self):
        """Считает площадь многоугольника как сумму площадей треугольников триангуляции.
 
        Returns:
            float: Площадь многоугольника.
        """
        list_triangles = self.triangulate()
        square = 0
        for tr in list_triangles:
            square += self.calc_square_triangle(tr[0], tr[1], tr[2])
        return square

    def calc_perimeter(self):
        """Считает периметр многоугольника.
 
        Складываются длины всех сторон, включая замыкающую сторону от
        последней вершины к первой.
 
        Returns:
            float: Периметр многоугольника.
        """
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
        """Создаёт многоугольник по списку вершин и проверяет его выпуклость.
 
        Args:
            vertices (list[tuple[float, float]]): Вершины в порядке обхода
                (по или против часовой стрелки).
 
        Raises:
            ValueError: Если многоугольник невыпуклый или вырожденный:
                меньше трёх вершин, совпадающие вершины, три подряд идущие
                вершины на одной прямой, самопересечение.
        """
        self.vertices = vertices
        self.n = len(vertices)
        self.flag_convex = self.isConvex()

        if not self.isConvex():
            raise ValueError("многоугольник невыпуклый или вырожденный")

        self.vertices = self.set_order(vertices)


    def triangulate(self):    # для выпуклого!
        """Разбивает многоугольник на треугольники.
 
        Из первой вершины проводятся диагонали ко всем вершинам, кроме двух
        соседних. Корректно только для выпуклого многоугольника.
 
        Returns:
            list[list[tuple[float, float]]]: n - 2 треугольников, каждый
                задан списком из трёх вершин.
        """
        n = self.n
        v = self.vertices
        ans = []
        # [p1, p2, p3, p4, p5, p6, p7]
        for i in range(1, n-1):
            ans.append([v[0], v[i], v[i+1]])
        return ans

    def clip_segment(self, A, B):
        """Обрезает отрезок AB многоугольником (алгоритм Кируса-Бека).
 
        Args:
            A (tuple[float, float]): Начало отрезка.
            B (tuple[float, float]): Конец отрезка.
 
        Returns:
            tuple[tuple[float, float], tuple[float, float]] | None: Пара
                точек (P_in, P_out), ограничивающая часть отрезка внутри
                многоугольника, или None, если отрезок лежит снаружи.
        """
        v, n = self.vertices, self.n
        t_in, t_out = 0.0, 1.0
        for i in range(n):
            C, D = v[i], v[(i + 1) % n]
            sA = self.calc_z_vect_prod(D, C, A)  # C->D, C->A
            sB = self.calc_z_vect_prod(D, C, B)  # C->D, C->B
            d = sB - sA
            if d == 0:                      # параллелен ребру
                if sA < 0:
                    return None
                continue
            t = -sA / d
            if d > 0:
                t_in = max(t_in, t)
            else:
                t_out = min(t_out, t)
            if t_in > t_out:
                return None
        P = lambda t: (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
        return P(t_in), P(t_out)

    def clip_by_lines(self, other):
        """Обрезает рёбра многоугольника other многоугольником self.
 
        Каждое ребро other передаётся в clip_segment, отрезки, оказавшиеся
        снаружи self, отбрасываются.
 
        Args:
            other (Convex_Polygons): Многоугольник, рёбра которого
                обрезаются.
 
        Returns:
            list[tuple[tuple[float, float], tuple[float, float]]]: Список
                отрезков (P_in, P_out), лежащих внутри self.
        """
        iter_vertices_other = itertools.cycle(other.vertices)
        fir = next(iter_vertices_other)
        sec = next(iter_vertices_other)
        m = other.n
        ans1 = []
        for _ in range(m):
            el = self.clip_segment(fir, sec)
            fir = sec
            sec = next(iter_vertices_other)
            if el == None:
                continue
            else:
                ans1.append(el)
        return ans1


    @staticmethod
    def same(p, q, eps=1e-9):
        """Сравнивает две точки с учётом погрешности float.
 
        Args:
            p (tuple[float, float]): Первая точка.
            q (tuple[float, float]): Вторая точка.
            eps (float): Допустимое отличие каждой координаты.
 
        Returns:
            bool: True, если обе координаты отличаются меньше чем на eps.
        """
        return abs(p[0] - q[0]) < eps and abs(p[1] - q[1]) < eps

    def intersect(self, other):
        """Находит пересечение двух выпуклых многоугольников.
 
        Собираются концы обрезанных рёбер обоих многоугольников, повторяющиеся
        точки удаляются, остальные сортируются по полярному углу вокруг
        центра. Если общая область вырождена (пусто, точка или отрезок),
        пересечения нет.
 
        Args:
            other (Convex_Polygons): Второй многоугольник.
 
        Returns:
            Convex_Polygons | None: Многоугольник-пересечение или None, если
                пересечение пусто или вырождено (касание).
        """
        segments = self.clip_by_lines(other) + other.clip_by_lines(self)

        pts = []
        for seg in segments:
            for p in seg:
                if not any(self.same(p, q) for q in pts):
                    pts.append(p)
        if len(pts) < 3:
            return None

        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))


        return Convex_Polygons(pts)

    def __repr__(self):
        return f"Convex_Polygon {self.vertices}"


    def includes(self, other):
        """Проверяет, что многоугольник other лежит внутри self.
 
        Граница считается принадлежащей многоугольнику. Проверка основана
        на сравнении площадей: если площадь пересечения равна площади other,
        то other лежит внутри self.
 
        Args:
            other (Convex_Polygons): Проверяемый многоугольник.
 
        Returns:
            bool: True, если other целиком лежит в self, иначе False.
        """
        inter = self.intersect(other)
        if inter is None: return False
        if math.isclose(inter.calc_square(), other.calc_square(), abs_tol=1e-9):
            return True
        return False

