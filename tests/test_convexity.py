"""Тесты проверки выпуклости при инициализации и вычисления угла."""
import pytest

from convex_polygons import Convex_Polygons


def signed_area2(v):
    """Удвоенная площадь со знаком: > 0 при обходе против часовой стрелки."""
    n = len(v)
    return sum(v[i][0] * v[(i + 1) % n][1] - v[(i + 1) % n][0] * v[i][1]
               for i in range(n))


VALID = {
    "triangle": [(0, 0), (4, 0), (0, 3)],
    "triangle_cw": [(0, 0), (1, 2), (5, 6)],
    "square_ccw": [(0, 0), (4, 0), (4, 4), (0, 4)],
    "square_cw": [(0, 0), (0, 4), (4, 4), (4, 0)],
    "parallelogram": [(0, 0), (4, 0), (5, 3), (1, 3)],
    "pentagon": [(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)],
    "hexagon": [(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)],
    "fractional": [(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)],
}

INVALID = {
    # слишком мало вершин
    "empty": [],
    "one_point": [(0, 0)],
    "two_points": [(0, 0), (1, 1)],
    # вырожденные случаи
    "three_collinear": [(0, 0), (1, 1), (2, 2)],
    "four_collinear": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "duplicate_adjacent": [(0, 0), (4, 0), (4, 0), (0, 4)],
    "duplicate_non_adjacent": [(0, 0), (4, 0), (4, 4), (0, 0)],
    # по принятому решению вершина на ребре (угол 180°) не допускается
    "vertex_on_edge": [(0, 0), (2, 0), (4, 0), (4, 4), (0, 4)],
    # невыпуклые
    "arrow": [(0, 0), (4, 2), (0, 4), (1, 2)],
    "concave_pentagon": [(0, 0), (4, 0), (4, 4), (2, 1), (0, 4)],
    "L_shape": [(0, 0), (6, 0), (6, 3), (4, 3), (4, 6), (0, 6)],
    # самопересечения
    "bowtie": [(0, 0), (4, 4), (4, 0), (0, 4)],
    "pentagram": [(0, 0), (5, 3), (-1, 3), (4, 0), (2, 5)],
}


# ---------- выпуклые принимаются ----------

@pytest.mark.parametrize("vertices", VALID.values(), ids=VALID.keys())
def test_convex_polygon_is_accepted(vertices):
    poly = Convex_Polygons(list(vertices))
    assert poly.n == len(vertices)
    assert poly.isConvex() is True


@pytest.mark.parametrize("vertices", VALID.values(), ids=VALID.keys())
def test_vertices_are_normalized_counterclockwise(vertices):
    poly = Convex_Polygons(list(vertices))
    assert signed_area2(poly.vertices) > 0


@pytest.mark.parametrize("vertices", VALID.values(), ids=VALID.keys())
def test_normalization_keeps_the_same_vertices(vertices):
    poly = Convex_Polygons(list(vertices))
    assert set(poly.vertices) == set(vertices)
    assert len(poly.vertices) == len(vertices)


def test_clockwise_and_counterclockwise_input_give_same_vertex_set():
    ccw = Convex_Polygons([(0, 0), (4, 0), (4, 4), (0, 4)])
    cw = Convex_Polygons([(0, 0), (0, 4), (4, 4), (4, 0)])
    assert set(ccw.vertices) == set(cw.vertices)


# ---------- невыпуклые и вырожденные отвергаются ----------

@pytest.mark.parametrize("vertices", INVALID.values(), ids=INVALID.keys())
def test_invalid_polygon_raises_value_error(vertices):
    with pytest.raises(ValueError):
        Convex_Polygons(list(vertices))


# ---------- вычисление угла ----------

@pytest.mark.parametrize("p1, p2, p3, expected", [
    ((8, 0), (0, 0), (2, 2), 45),
    ((1, 0), (0, 0), (0, 1), 90),
    ((1, 0), (0, 0), (-1, 1), 135),
    ((1, 0), (0, 0), (-1, 0), 180),
    ((1, 0), (0, 0), (2, 0), 0),
    ((0, 0), (1, 1), (2, 2), 180),
], ids=["45", "90", "obtuse_135", "straight_180", "zero", "collinear_through_vertex"])
def test_calc_angle(p1, p2, p3, expected):
    assert Convex_Polygons.calc_angle(p1, p2, p3) == pytest.approx(expected)


def test_angle_is_symmetric_in_outer_points():
    a, b, c = (8, 0), (0, 0), (2, 2)
    assert Convex_Polygons.calc_angle(a, b, c) == pytest.approx(
        Convex_Polygons.calc_angle(c, b, a))


def test_angle_is_never_negative_for_clockwise_triple():
    # (0,0) -> (0,4) -> (4,4) поворачивает по часовой стрелке
    assert Convex_Polygons.calc_angle((0, 0), (0, 4), (4, 4)) == pytest.approx(90)


def test_angle_sum_of_valid_polygons_equals_180_n_minus_2():
    for vertices in VALID.values():
        n = len(vertices)
        total = sum(
            Convex_Polygons.calc_angle(vertices[i - 1], vertices[i], vertices[(i + 1) % n])
            for i in range(n))
        assert total == pytest.approx(180 * (n - 2), abs=1e-6)