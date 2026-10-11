from convex_polygons import Convex_Polygons


def main():
    a = Convex_Polygons([(0, 0), (4, 0), (4, 4), (0, 4)])
    b = Convex_Polygons([(2, 2), (6, 2), (6, 6), (2, 6)])

    print("a:", a)
    print("площадь:", a.calc_square())
    print("периметр:", a.calc_perimeter())
    print("триангуляция:", a.triangulate())
    print("пересечение:", a.intersect(b))
    print("a включает b:", a.includes(b))

    try:
        Convex_Polygons([(0, 0), (4, 2), (0, 4), (1, 2)])
    except ValueError as e:
        print("невыпуклый отвергнут:", e)


if __name__ == "__main__":
    main()