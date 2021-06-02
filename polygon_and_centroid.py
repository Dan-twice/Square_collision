import pygame
import sys
import math


class Polygon:
    """Creates polygon with rotation angle,
     points it's a shape of the object
     from left-top corner (0, 0)
     + position on canvas"""
    contain = []

    def __init__(self, surface, color, cord, angle, posx=0, posy=0, size=3, bold=0):
        self.image = surface
        self.color = color
        self.bold = bold
        self.cord = cord
        self.cord_len = len(cord)
        self.posx = posx
        self.posy = posy

        self.centry = self.centroid(self.cord)
        self.cord = [pygame.math.Vector2(i[0] - self.centry[0], i[1] - self.centry[1]) for i in cord]
        self.cord_rot = [i.rotate(angle) for i in self.cord]  # self.dir.normalize(),
        self.cord = [[self.posx + i[0] * size, self.posy + i[1] * size] for i in self.cord_rot]

    def draw_polygon(self):
        pygame.draw.polygon(self.image, self.color, self.cord, self.bold)

    def draw_center(self, color, radius=5):
        pygame.draw.circle(self.image, color, [self.posx, self.posy], radius)

    def centroid(self, cord):
        """Find the center of the shape"""
        numeratorx, numeratory, denominator = 0, 0, []
        for i in range(self.cord_len):
            j = (i + 1) % self.cord_len
            denominator.append(cord[i][0] * cord[j][1] - cord[j][0] * cord[i][1])
            numeratorx += (cord[i][0] + cord[j][0]) * denominator[-1]
            numeratory += (cord[i][1] + cord[j][1]) * denominator[-1]

        return (numeratorx / sum(denominator) * (1/3), numeratory / sum(denominator) * (1/3))


class Polygon2:
    """Creates stretch with rotation angle by first point"""
    contain = []

    def __init__(self, surface, color, cord, angle):
        self.image = surface
        self.color = color
        self.c = math.cos(math.radians(angle))
        self.s = math.sin(math.radians(angle))
        self.width = cord[1][0] - cord[0][0]
        self.cord = [[cord[0][0], cord[0][1]],
                     [cord[1][0] - (self.width - self.c * self.width), cord[1][1] + (0 - self.s * self.width)]]

    def draw_stretch(self):
        pygame.draw.polygon(self.image, self.color, self.cord, 2)


class Polygon3:
    """Creates kinda perspective form triangles. Not for use, for fun"""
    contain = []

    def __init__(self, surface, color, cord, angle, bold=0):
        self.image = surface
        self.color = color
        self.c = math.cos(math.radians(angle))
        self.s = math.sin(math.radians(angle))
        self.width = 50
        self.bold = bold
        self.cord = [[cord[0][0], cord[0][1]],
                      [cord[1][0] - (self.width - self.c * self.width), cord[1][1] + (0 - self.s * self.width)],
                      [cord[2][0] - (0 - self.c * self.width), cord[2][1] - (self.width - self.s * self.width)]]

    def draw_triangle(self):
        pygame.draw.polygon(self.image, self.color, self.cord, self.bold)


if __name__ == '__main__':
    dict_colors = {
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'BLUE': (173, 223, 237),
        'RED': (252, 61, 3),
        'ORANGE': (252, 186, 3),
        'YELLOW': (200, 255, 200),
        'BLUE_DARK': (56, 89, 115)
    }

    FPS = 60
    fps_clock = pygame.time.Clock()

    W = 1000
    H = 500

    sc = pygame.display.set_mode((W, H))
    sc.fill(dict_colors['WHITE'])

    # pygame.math.Vector2(0, 0) is the center of ration and ACCIDENTALLY first point of the shape
    points = [(0, 0), (10, 0), (10, 10), (0, 10)]

    # orange square
    for i in range(0, 360, 10):
        Polygon(sc, dict_colors['ORANGE'], points, i, posx=70, posy=100, bold=4, size=5).draw_polygon()

    # black stretch
    for i in range(0, 100, 45):
        Polygon2(sc, dict_colors['BLACK'], [[250, 150], [350, 150]], i).draw_stretch()

    # red triangle (perspective)
    Polygon3(sc, dict_colors['RED'], [[400, 75], [450, 100], [400, 125]], 0).draw_triangle()
    Polygon3(sc, dict_colors['RED'], [[400, 75], [450, 100], [400, 125]], 100).draw_triangle()

    # random polygon
    points_polygon = [(0, 0), (5, -10), (10, -1), (20, 5), (9, 14), (4, 12), (3, 4)]
    c = 10
    for i in range(0, 360, 50):
        r1 = Polygon(sc, dict_colors['BLUE_DARK'], points_polygon, i, posx=100 + c, posy=250)
        r1.draw_polygon()
        r1.draw_center(dict_colors['RED'])
        c += 100

    # square with center in center
    for i in range(0, 360, 40):
        Polygon(sc, dict_colors['BLUE_DARK'], points, i, posx=70, posy=150, size=6)

    # blue square with red point
    Polygon(sc, dict_colors['BLUE_DARK'], points, 0, posx=200, posy=350, bold=2, size=4).draw_polygon()
    Polygon(sc, dict_colors['BLUE_DARK'], points, 20, posx=200, posy=350, bold=2, size=4).draw_polygon()
    Polygon(sc, dict_colors['BLUE_DARK'], points, 50, posx=200, posy=350, bold=2, size=4).draw_polygon()

    pygame.draw.rect(sc, dict_colors['BLACK'], pygame.Rect(120, 30, 50, 50))

    pygame.display.flip()

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        fps_clock.tick(FPS)

    # for block in Square.contain:
    #     block.draw_square()

    # pygame.display.flip()

