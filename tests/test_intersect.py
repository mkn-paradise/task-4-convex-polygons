"""Тесты пересечения многоугольников и проверки вложенности (includes)."""
import math
import random

import pytest

from convex_polygons import Convex_Polygons


def square(x, y, s):
    return Convex_Polygons([(x, y), (x + s, y), (x + s, y + s), (x, y + s)])


def has_same_points(poly, expected, tol=1e-9):
    """Совпадает ли набор вершин с ожидаемым (порядок и начальная точка не важны)."""
    if len(poly.vertices) != len(expected):
        return False
    return all(
        any(math.isclose(v[0], e[0], abs_tol=tol) and math.isclose(v[1], e[1], abs_tol=tol)
            for v in poly.vertices)
        for e in expected)


# ---------- пересечение есть ----------

def test_overlapping_squares():
    result = square(0, 0, 4).intersect(square(2, 2, 4))
    assert result is not None
    assert has_same_points(result, [(2, 2), (4, 2), (4, 4), (2, 4)])
    assert math.isclose(result.calc_square(), 4)


def test_cross_shaped_rectangles():
    a = Convex_Polygons([(0, 0), (6, 0), (6, 2), (0, 2)])
    b = Convex_Polygons([(2, -2), (4, -2), (4, 4), (2, 4)])
    result = a.intersect(b)
    assert result is not None
    assert has_same_points(result, [(2, 0), (4, 0), (4, 2), (2, 2)])
    assert math.isclose(result.calc_square(), 4)


def test_triangle_corner_inside_square():
    sq = square(0, 0, 4)
    tri = Convex_Polygons([(3, 3), (8, 3), (3, 8)])
    result = sq.intersect(tri)
    assert result is not None
    assert has_same_points(result, [(3, 3), (4, 3), (4, 4), (3, 4)])
    assert math.isclose(result.calc_square(), 1)


def test_hexagon_and_triangle_with_fractional_vertices():
    hexagon = Convex_Polygons([(0, 2), (2, 4), (4, 4), (6, 2), (4, 0), (2, 0)])
    triangle = Convex_Polygons([(3, 0), (1, 4), (5, 4)])
    result = hexagon.intersect(triangle)
    assert result is not None
    expected = [(3, 0), (14 / 3, 10 / 3), (4, 4), (2, 4), (4 / 3, 10 / 3)]
    assert has_same_points(result, expected, tol=1e-9)
    # площадь вычислена вручную: 8 (весь треугольник) минус два угла по 1/3
    assert math.isclose(result.calc_square(), 22 / 3, rel_tol=1e-9)


def test_result_is_convex_polygon_object():
    result = square(0, 0, 4).intersect(square(2, 2, 4))
    assert isinstance(result, Convex_Polygons)
    assert result.isConvex()


def test_clockwise_input_gives_same_result():
    ccw = square(0, 0, 4)
    cw = Convex_Polygons([(2, 2), (2, 6), (6, 6), (6, 2)])   # по часовой
    result = ccw.intersect(cw)
    assert result is not None
    assert math.isclose(result.calc_square(), 4)


# ---------- вложенность ----------

def test_inner_polygon_inside_outer():
    outer, inner = square(0, 0, 10), square(2, 2, 3)
    result = outer.intersect(inner)
    assert result is not None
    assert math.isclose(result.calc_square(), 9)
    assert has_same_points(result, inner.vertices)


def test_inner_polygon_sharing_a_corner_with_outer():
    outer, inner = square(0, 0, 4), square(0, 0, 2)
    result = outer.intersect(inner)
    assert result is not None
    assert math.isclose(result.calc_square(), 4)


def test_identical_polygons():
    a = square(0, 0, 4)
    b = square(0, 0, 4)
    result = a.intersect(b)
    assert result is not None
    assert math.isclose(result.calc_square(), 16)


# ---------- пересечения нет ----------

def test_disjoint_returns_none():
    assert square(0, 0, 1).intersect(square(5, 5, 1)) is None


def test_touching_by_side_returns_none():
    assert square(0, 0, 4).intersect(square(4, 0, 4)) is None


def test_touching_by_partial_side_returns_none():
    assert square(0, 0, 4).intersect(square(4, 1, 2)) is None


def test_touching_by_vertex_returns_none():
    assert square(0, 0, 4).intersect(square(4, 4, 4)) is None


def test_touching_triangle_with_square_returns_none():
    sq = square(0, 0, 4)
    tri = Convex_Polygons([(4, 0), (8, 0), (4, 3)])   # ребро (4,0)-(4,3) лежит на стороне квадрата
    assert sq.intersect(tri) is None


# ---------- симметрия ----------

PAIRS = {
    "overlapping_squares": (lambda: square(0, 0, 4), lambda: square(2, 2, 4)),
    "hexagon_triangle": (
        lambda: Convex_Polygons([(0, 2), (2, 4), (4, 4), (6, 2), (4, 0), (2, 0)]),
        lambda: Convex_Polygons([(3, 0), (1, 4), (5, 4)])),
    "nested": (lambda: square(0, 0, 10), lambda: square(2, 2, 3)),
    "identical": (lambda: square(0, 0, 4), lambda: square(0, 0, 4)),
    "disjoint": (lambda: square(0, 0, 1), lambda: square(5, 5, 1)),
    "touching": (lambda: square(0, 0, 4), lambda: square(4, 0, 4)),
}


@pytest.mark.parametrize("make_a, make_b", PAIRS.values(), ids=PAIRS.keys())
def test_intersection_is_symmetric(make_a, make_b):
    a, b = make_a(), make_b()
    ab, ba = a.intersect(b), b.intersect(a)
    assert (ab is None) == (ba is None)
    if ab is not None:
        assert math.isclose(ab.calc_square(), ba.calc_square(), rel_tol=1e-9)


def test_intersection_with_itself_keeps_area():
    a = Convex_Polygons([(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)])
    result = a.intersect(a)
    assert result is not None
    assert math.isclose(result.calc_square(), a.calc_square(), rel_tol=1e-9)


# ---------- includes ----------

def test_includes_big_contains_small():
    assert square(0, 0, 10).includes(square(2, 2, 3)) is True


def test_includes_small_does_not_contain_big():
    assert square(2, 2, 3).includes(square(0, 0, 10)) is False


def test_includes_identical_polygons():
    assert square(0, 0, 4).includes(square(0, 0, 4)) is True


def test_includes_with_shared_boundary():
    assert square(0, 0, 4).includes(square(0, 0, 2)) is True


def test_includes_partial_overlap_is_false_both_ways():
    a, b = square(0, 0, 4), square(2, 2, 4)
    assert a.includes(b) is False
    assert b.includes(a) is False


def test_includes_disjoint_is_false_without_error():
    assert square(0, 0, 1).includes(square(5, 5, 1)) is False


def test_includes_touching_is_false_without_error():
    assert square(0, 0, 4).includes(square(4, 0, 4)) is False


# ---------- случайные проверки свойств ----------

def random_convex(k, r=10, shift=10):
    angles = sorted(random.uniform(0, 2 * math.pi) for _ in range(k))
    cx, cy = random.uniform(-shift, shift), random.uniform(-shift, shift)
    return [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in angles]


def test_random_polygons_properties():
    random.seed(12345)
    checked = 0
    for _ in range(300):
        try:
            a = Convex_Polygons(random_convex(random.randint(3, 8)))
            b = Convex_Polygons(random_convex(random.randint(3, 8)))
        except ValueError:
            continue          # сам входной многоугольник оказался вырожденным

        ab = a.intersect(b)   # здесь ValueError не ловим: это настоящая ошибка
        ba = b.intersect(a)
        assert (ab is None) == (ba is None)
        if ab is None:
            continue

        checked += 1
        s_ab, s_ba = ab.calc_square(), ba.calc_square()
        assert math.isclose(s_ab, s_ba, rel_tol=1e-9, abs_tol=1e-9)
        assert s_ab <= min(a.calc_square(), b.calc_square()) + 1e-9

        aa = a.intersect(a)
        assert aa is not None
        assert math.isclose(aa.calc_square(), a.calc_square(), rel_tol=1e-9)

    assert checked > 50       # тест осмысленный: пересечения реально встречались