import pygame
import sys
import polygon_and_centroid as pol

pygame.init()


def calc_magnitude(coord):
    return (coord[0] ** 2 + coord[1] ** 2) ** 0.5


def find_projection(dot, normal, normal_mag):
    return dot[0] * (normal[0] / normal_mag) + dot[1] * (normal[1] / normal_mag)


def return_dot_projection(box_coord, start_normal, end_normal, first=False):
    """Find minimum or maximum dot distance from normal's start"""
    normal_normalized = [end_normal[0] - start_normal[0],
                         end_normal[1] - start_normal[1]]

    box_max, box_min, length_to_dot, dot_cord = 0, float('inf'), 0, 0
    normal_magnitude = calc_magnitude(normal_normalized)

    if first:
        vector_1type = False  # axis x, y < 0  without abs
        vector_2type = False  # x, y > 0
        if normal_normalized[0] < 0 and normal_normalized[1] < 0:
            vector_1type = True
        elif normal_normalized[0] > 0 and normal_normalized[1] > 0:
            vector_2type = True

        normal_normalized = [abs(normal_normalized[0]), abs(normal_normalized[1])]

        for i in range(len(box_coord)):
            if vector_1type:
                dot = [abs(box_coord[i][0] - start_normal[0]), start_normal[1] - box_coord[i][1]]
            elif vector_2type:
                dot = [box_coord[i][0] - start_normal[0], -(start_normal[1] - box_coord[i][1])]
            else:
                dot = [box_coord[i][0] - start_normal[0], start_normal[1] - box_coord[i][1]]

            projection = abs(find_projection(dot, normal_normalized, normal_magnitude))
            if projection > box_max:
                box_max = projection
                dot_cord = (box_coord[i][0], box_coord[i][1])
        return dot_cord,  abs(round(box_max))
    else:
        for i in range(len(box_coord)):
            dot = [start_normal[0] - box_coord[i][0], start_normal[1] - box_coord[i][1]]
            projection = abs(find_projection(dot, normal_normalized, normal_magnitude))
            if projection < box_min:
                box_min = projection
                dot_cord = (box_coord[i][0], box_coord[i][1])
        return dot_cord, abs(round(box_min))


def message(yes):
    font_obj = pygame.font.Font('freesansbold.ttf', 32)
    if yes:
        text_surf_obj = font_obj.render('Penetrated!', True, dict_colors['BLACK'])
        text_rect_obj = text_surf_obj.get_rect()
    else:
        text_surf_obj = font_obj.render('Not yet!', True, dict_colors['BLACK'])
        text_rect_obj = text_surf_obj.get_rect()
    sc.blit(text_surf_obj, text_rect_obj)


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

W = 500
H = 500

sc = pygame.display.set_mode((W, H))
sc.fill(dict_colors['WHITE'])

points = [(0, 0), (10, 0), (10, 10), (0, 10)]
p1 = pol.Polygon(sc, dict_colors['BLUE_DARK'], points, 70, size=5, bold=2, posx=175, posy=150)
p2 = pol.Polygon(sc, dict_colors['BLUE_DARK'], points, 20, size=5, bold=2, posx=240, posy=150)

p1.draw_polygon()
p2.draw_polygon()

pygame.display.flip()

move_origin = 6
move = 0
move_y = 0
normal = 1

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                move = -move_origin
            elif i.key == pygame.K_RIGHT:
                move = move_origin
            elif not (i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT):
                move = 0
            if i.key == pygame.K_UP:
                move_y = -move_origin
            elif i.key == pygame.K_DOWN:
                move_y = move_origin
            elif not (i.key == pygame.K_UP or i.key == pygame.K_DOWN):
                move_y = 0
            p2.posx += move
            p2.posy += move_y

            for c in range(len(p2.cord)):
                p2.cord[c][0] += move
                p2.cord[c][1] += move_y

            arr_collisions = []
            for normal in range(len(p1.cord)):
                dot_cord_1, normal_dot1 = return_dot_projection(p1.cord, p1.cord[normal], p1.cord[normal - 1],
                                                                first=True)
                dot_cord_2, normal_dot2 = return_dot_projection(p2.cord, p1.cord[normal], p1.cord[normal - 1])
                dot_cord_2_2, normal_dot2_2 = return_dot_projection(p2.cord, p1.cord[normal-1], p1.cord[normal])

                yes = False
                # collusion detection right-left and left-right
                if normal_dot2 - normal_dot1 < 0 and normal_dot2_2 - normal_dot1 < 0:
                    yes = True
                arr_collisions.append(yes)
            sc.fill(dict_colors['WHITE'])
            p1.draw_polygon()
            p2.draw_polygon()
            message(False not in arr_collisions)

            pygame.display.flip()

    fps_clock.tick(FPS)
