import pygame
import numpy as np
from time import sleep
from enum import Enum
import math

width, height = 800, 800


class Colors(Enum):
    background = (50, 50, 50)
    polygon = (200, 200, 200)

def screenpoint__camera_point(percentages):
    return int(800 * (percentages[0]/100)), int(800 * (percentages[1]/100))

def rotate_point(cx, cy, angle, px, py):

    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))

    px -= cx
    py -= cy

    xnew = px * c - py * s
    ynew = px * s + py * c

    px = xnew + cx
    py = ynew + cy
    return px,py



def worldscreenpoint__camera_point(camera, spot, t):

    x,z = rotate_point(
        camera["coordinates"]["x"],
        camera["coordinates"]["z"],
        -camera["angle"]["x"],
        spot["x"],
        spot["z"]
    )
    y,z = rotate_point(
        camera["coordinates"]["y"],
        camera["coordinates"]["z"],
        -camera["angle"]["y"],
        spot["y"],
        z
    )
    

    leg2 = x - camera["coordinates"]["x"]
    leg1 = z - camera["coordinates"]["z"]
    hipo = math.sqrt((leg2*leg2) + (leg1*leg1))
    xangle = math.degrees(np.arcsin(leg2/hipo)) # + camera["angle"]["x"]
    x_camera_screen_point_inter_distance = math.tan(math.radians(xangle))

    leg2 = y - camera["coordinates"]["y"]
    leg1 = z - camera["coordinates"]["z"]
    hipo = math.sqrt((leg2**2) + (leg1**2))
    yangle = math.degrees(np.arcsin(leg2/hipo)) # + camera["angle"]["y"]
    y_camera_screen_point_inter_distance = math.tan(math.radians(yangle)) # * hipotenusa


    xp = ( 100 / ( (camera_total_inter_distance*2) / (x_camera_screen_point_inter_distance+camera_total_inter_distance) ) ) 
    yp = ( 100 / ( (camera_total_inter_distance*2) / (y_camera_screen_point_inter_distance+camera_total_inter_distance) ) ) 

    return xp, yp


def screenpoint_of_point(camera, point, t):

    percentages = worldscreenpoint__camera_point(camera, point,t)
    sp = screenpoint__camera_point(percentages)

    return sp

LOG = True
ii = 0.01
# camera = 
CAMERA_ANGLE = 50
speed = .5
camera_total_inter_distance = math.tan(math.radians(CAMERA_ANGLE)) # * hipotenusa
camera = {
    "coordinates": {"x": 100, "y": 100, "z": 100},
    "angle": {"x":0,"y":0}
}

size = 10
polygon1 = {
    "coordinates": {'x': 100, 'y': 100, 'z': 110},
    "angles": {'x': 0, 'y': 0, 'z': 0},
    "scale": {'x': 3, 'y': 3, 'z': 3},
    "points": (
        {'x': -1, 'y': -1, 'z': -1},
        {'x': -1, 'y': 1, 'z': -1},
        {'x': 1, 'y': 1, 'z': -1},
        {'x': 1, 'y': -1, 'z': -1},
        {'x': -1, 'y': -1, 'z': 1},
        {'x': -1, 'y': 1, 'z': 1},
        {'x': 1, 'y': 1, 'z': 1},
        {'x': 1, 'y': -1, 'z': 1},
    ),
    "relations": (
        (1,0),
        (1,2),
        (3,0),
        (3,2),
        (5,4),
        (5,6),
        (7,4),
        (7,6),
        (0,4),
        (1,5),
        (2,6),
        (3,7),
    )
}
polygons = [polygon1]

pygame.init()
screen = pygame.display.set_mode((height, width))
screen.fill(Colors.background.value)
print(Colors.background)

font = pygame.font.SysFont(None, 24)


while True:

    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0] or 1
    mouse_y = mouse[1] or 1

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LCTRL]:
        camera["coordinates"]["y"] += speed
    if keys[pygame.K_SPACE]:
        camera["coordinates"]["y"] -= speed
    if keys[pygame.K_a]:
        camera["coordinates"]["x"] -= speed
    if keys[pygame.K_d]:
        camera["coordinates"]["x"] += speed
    if keys[pygame.K_w]:
        camera["coordinates"]["z"] += speed
    if keys[pygame.K_s]:
        camera["coordinates"]["z"] -= speed
    for event in events:
        pygame.event.set_grab(True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        mouseClick = pygame.mouse.get_pressed()


    x_distance_camera_side = math.tan(math.radians(CAMERA_ANGLE))
    screen_bbox = (
        (camera["coordinates"]["x"] - x_distance_camera_side,
         camera["coordinates"]["y"] - x_distance_camera_side),
        (camera["coordinates"]["x"] + x_distance_camera_side,
         camera["coordinates"]["y"] + x_distance_camera_side)
    )


    screen.fill(Colors.background.value)
    img = font.render(str(str(camera["coordinates"]["x"])+","+str(camera["coordinates"]["y"])+","+str(camera["coordinates"]["z"])), True, (150,150,150))
    screen.blit(img, (10,10))


    mouse_x = 100 / ( 800 / mouse_x )
    mouse_y = 100 / ( 800 / mouse_y )
    max_angle = 90
    camera["angle"]["x"] =  -( ((max_angle*2)*(mouse_x/100))-max_angle )
    camera["angle"]["y"] =  -( ((max_angle*2)*(mouse_y/100))-max_angle )

   

    for polygon in polygons:

        abs_coordinates = polygon["coordinates"]
        scale = polygon["scale"]
        vertexs = polygon["points"]
        relations = polygon["relations"]

        x_degrees,y_degrees,z_degrees = polygon["angles"]["x"],polygon["angles"]["y"],polygon["angles"]["z"]

        vertexs = [ {
            "x": vertex["x"] * scale["x"],
            "y": vertex["y"] * scale["y"],
            "z": vertex["z"] * scale["z"]
        } for vertex in vertexs ]
        vertexs = [
            {
                "x": ( v["x"] * math.cos(math.radians(x_degrees)) ) - ( v["y"] * math.sin(math.radians(x_degrees)) ),
                "y": ( v["x"] * math.sin(math.radians(x_degrees)) ) + ( v["y"] * math.cos(math.radians(x_degrees)) ),
                "z": v["z"]
            } for v in vertexs
        ]
        vertexs = [
            {
                "x": ( v["x"] * math.cos(math.radians(y_degrees)) ) - ( v["z"] * math.sin(math.radians(y_degrees)) ),
                "z": ( v["x"] * math.sin(math.radians(y_degrees)) ) + ( v["z"] * math.cos(math.radians(y_degrees)) ),
                "y": v["y"]
            } for v in vertexs
        ]
        vertexs = [
            {
                "z": ( v["z"] * math.cos(math.radians(z_degrees)) ) - ( v["y"] * math.sin(math.radians(z_degrees)) ),
                "y": ( v["z"] * math.sin(math.radians(z_degrees)) ) + ( v["y"] * math.cos(math.radians(z_degrees)) ),
                "x": v["x"]
            } for v in vertexs
        ]
        
        coordinates = [ { 
            "x":abs_coordinates["x"]+c["x"],
            "y":abs_coordinates["y"]+c["y"],
            "z":abs_coordinates["z"]+c["z"]
        } for c in vertexs ]


        polygon_screen = [screenpoint_of_point(camera, point,True) for point in coordinates]

        for i, r in enumerate(relations):

            point = coordinates[r[0]]
            xs = polygon_screen[r[0]]
            ys = polygon_screen[r[1]]

            if i == 0:
                text = str(str(round(point["x"],1))+","+str(round(point["y"],1))+","+str(round(point["z"],1)))
                img = font.render(text, True, (150,150,150))
                screen.blit(img, xs)

            pygame.draw.line(
                screen, 
                Colors.polygon.value,
                xs,
                ys,
                1
            )


    # polygon["angles"]["x"] += 1
    # polygon["angles"]["y"] += 1
    # polygon["angles"]["z"] += 1


    sleep(0.05)


    pygame.display.flip()
