"""Тесты площади, периметра и триангуляции.

Ожидаемые значения посчитаны вручную (геометрия), а не взяты из вывода программы.
"""
import math

import pytest

from convex_polygons import Convex_Polygons

S2 = math.sqrt(2)
S10 = math.sqrt(10)
S13 = math.sqrt(13)

# имя: (вершины, площадь, периметр)
CASES = {
    "right_triangle_3_4_5": ([(0, 0), (4, 0), (0, 3)], 6, 12),
    "right_isosceles": ([(0, 0), (1, 0), (0, 1)], 0.5, 2 + S2),
    "square_4": ([(0, 0), (4, 0), (4, 4), (0, 4)], 16, 16),
    "rectangle_5x2": ([(0, 0), (5, 0), (5, 2), (0, 2)], 10, 14),
    "parallelogram": ([(0, 0), (4, 0), (5, 3), (1, 3)], 12, 8 + 2 * S10),
    "hexagon": ([(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)], 16, 4 + 8 * S2),
    "pentagon": ([(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)], 21, 4 + 2 * S10 + 2 * S13),
    "diamond": ([(2, 0), (4, 2), (2, 4), (0, 2)], 8, 8 * S2),
    "negative_coords": ([(-3, -3), (-1, -3), (-1, -1), (-3, -1)], 4, 8),
    "fractional": ([(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)], 0.25, 2),
}

IDS = list(CASES.keys())
PARAMS = list(CASES.values())


def shoelace_area(v):
    """Независимый расчёт площади (формула шнурования) для сверки."""
    n = len(v)
    s = sum(v[i][0] * v[(i + 1) % n][1] - v[(i + 1) % n][0] * v[i][1]
            for i in range(n))
    return abs(s) / 2


# ---------- площадь ----------

@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_area(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    assert math.isclose(poly.calc_square(), area, rel_tol=1e-9)


def test_area_of_hexagon_is_exact_integer_value():
    # Раньше формула Герона давала 15.999999999999995
    poly = Convex_Polygons([(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)])
    assert poly.calc_square() == 16


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_area_does_not_depend_on_direction(vertices, area, perimeter):
    ccw = Convex_Polygons(list(vertices))
    cw = Convex_Polygons(list(vertices)[::-1])
    assert math.isclose(ccw.calc_square(), cw.calc_square(), rel_tol=1e-9)


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_area_does_not_depend_on_start_vertex(vertices, area, perimeter):
    v = list(vertices)
    shifted = Convex_Polygons(v[1:] + v[:1])
    assert math.isclose(shifted.calc_square(), area, rel_tol=1e-9)


# ---------- периметр ----------

@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_perimeter(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    assert math.isclose(poly.calc_perimeter(), perimeter, rel_tol=1e-9)


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_perimeter_does_not_depend_on_direction(vertices, area, perimeter):
    ccw = Convex_Polygons(list(vertices))
    cw = Convex_Polygons(list(vertices)[::-1])
    assert math.isclose(ccw.calc_perimeter(), cw.calc_perimeter(), rel_tol=1e-9)


def test_perimeter_includes_closing_edge():
    # Если не учесть ребро от последней вершины к первой, получится 12 вместо 16
    poly = Convex_Polygons([(0, 0), (4, 0), (4, 4), (0, 4)])
    assert poly.calc_perimeter() == 16


# ---------- триангуляция ----------

@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_triangulation_has_n_minus_2_triangles(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    assert len(poly.triangulate()) == len(vertices) - 2


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_triangulation_uses_only_polygon_vertices(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    allowed = set(poly.vertices)
    for tri in poly.triangulate():
        assert len(tri) == 3
        assert set(tri) <= allowed


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_triangulation_areas_sum_to_polygon_area(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    total = sum(shoelace_area(tri) for tri in poly.triangulate())
    assert math.isclose(total, area, rel_tol=1e-9)


@pytest.mark.parametrize("vertices, area, perimeter", PARAMS, ids=IDS)
def test_triangulation_triangles_are_not_degenerate(vertices, area, perimeter):
    poly = Convex_Polygons(list(vertices))
    for tri in poly.triangulate():
        assert shoelace_area(tri) > 0


def test_triangle_triangulates_into_itself():
    poly = Convex_Polygons([(0, 0), (4, 0), (0, 3)])
    result = poly.triangulate()
    assert len(result) == 1
    assert set(result[0]) == {(0, 0), (4, 0), (0, 3)}