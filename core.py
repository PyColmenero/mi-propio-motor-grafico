import pygame
import numpy as np
from time import sleep
from enum import Enum
import math
import json
from line_plane_intersection import isect_line_plane_v3
from points_to_normal import points_to_normal

width, height = 800, 800


class Color():
    def __init__(self, rgb, name):
        self.rdb = rgb
        self.name = name

COLORS = {
    "background": (50, 50, 50),
    "edge": (200, 200, 200)
}
# COLOR_BACKGROUND = Color( (50, 50, 50), "background" )
# COLOR_EDGES = Color( (200, 200, 200), "edge" )

    # background = (50, 50, 50)
    # polygon = (200, 200, 200)

def screenpoint__camera_point(percentages):
    return int(width * (percentages[0]/100)), int(height * (percentages[1]/100))

def rotate_3d_point(cx, cy,cz, anglex, angley, px, py,pz):
    x,z = rotate_point(cx,cz,anglex,px,pz)
    y,z = rotate_point(cy,cz,angley,py,z)

    return x,y,z
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


def angles_to_screenpoint(x,y):
    x_camera_screen_point_inter_distance = math.tan(math.radians(x))
    y_camera_screen_point_inter_distance = math.tan(math.radians(y)) # * hipotenusa
    xp = ( 100 / ( (camera_total_inter_distance*2) / (x_camera_screen_point_inter_distance+camera_total_inter_distance) ) ) 
    yp = 100 -( 100 / ( (camera_total_inter_distance*2) / (y_camera_screen_point_inter_distance+camera_total_inter_distance) ) ) 
    return xp,yp

def worldscreenpoint__camera_point(
    first_point_x: float = 0,
    first_point_y: float = 0,
    first_point_z: float = 0,
    second_point_x: float = 0,
    second_point_y: float = 0,
    second_point_z: float = 0,
    rotation_about_first_point_x: float = 0,
    rotation_about_first_point_y: float = 0
):

    x,y,z = rotate_3d_point(
        first_point_x, first_point_y, first_point_z,
        -rotation_about_first_point_x, -rotation_about_first_point_y,
        second_point_x,second_point_y,second_point_z
    )

    leg1 = z - first_point_z
    
    leg2 = x - first_point_x
    hipo = math.sqrt((leg2*leg2) + (leg1*leg1))
    xangle = math.degrees(np.arcsin(leg2/hipo))

    leg2 = y - first_point_y
    hipo = math.sqrt((leg2**2) + (leg1**2)) or 1
    yangle = math.degrees(np.arcsin(leg2/hipo))
        
    
    return xangle, yangle

def point_to_intersection(camera,vector,p1,p2):

    inter = isect_line_plane_v3(
        (p1["x"], p1["y"], p1["z"]),
        (p2["x"], p2["y"], p2["z"]),
        (camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"]),
        vector
    )

    if inter:

        return worldscreenpoint__camera_point(
            camera["coordinates"]["x"], 
            camera["coordinates"]["y"], 
            camera["coordinates"]["z"], 
            inter[0],
            inter[1],
            inter[2],
            camera["angle"]["x"],
            camera["angle"]["y"]
        )


def get_angles_from_ver_inter(point_one_angles, point_two_angles):

    p1 = [camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"]]
    p2 = [camera["coordinates"]["x"]+1,camera["coordinates"]["y"]+1,camera["coordinates"]["z"]+1]
    p3 = [camera["coordinates"]["x"]-1,camera["coordinates"]["y"]+2,camera["coordinates"]["z"]+2]
    normal_up = points_to_normal(p1,p2,p3, camera)
    p1 = [camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"]]
    p2 = [camera["coordinates"]["x"]+1,camera["coordinates"]["y"]-1,camera["coordinates"]["z"]+1]
    p3 = [camera["coordinates"]["x"]-1,camera["coordinates"]["y"]-2,camera["coordinates"]["z"]+2]
    normal_down = points_to_normal(p1,p2,p3, camera)

    # igriegases
    if point_two_angles[1] > MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_up
        point_two_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_two_angles
    if point_two_angles[1] < -MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_down
        point_two_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_two_angles
    if point_one_angles[1] > MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_up
        point_one_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_one_angles
    if point_one_angles[1] < -MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_down
        point_one_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_one_angles

    return point_one_angles, point_two_angles

def get_angles_from_depth_inter(point_one, point_two):

    p1 = [camera["coordinates"]["x"], camera["coordinates"]["y"],   camera["coordinates"]["z"]]
    p2 = [camera["coordinates"]["x"]+2,camera["coordinates"]["y"]-1,camera["coordinates"]["z"]]
    p3 = [camera["coordinates"]["x"]-1,camera["coordinates"]["y"]+2,camera["coordinates"]["z"]]
    normal_depth = points_to_normal(p1,p2,p3, camera)

    return point_to_intersection(
        camera=camera,
        vector=normal_depth,
        p1=point_one,
        p2=point_two
    )

def get_angles_from_hor_inter(point_one_angles, point_two_angles):

    p1 = [camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"]]
    p2 = [camera["coordinates"]["x"]+1,camera["coordinates"]["y"]+1,camera["coordinates"]["z"]+1]
    p3 = [camera["coordinates"]["x"]+2,camera["coordinates"]["y"]-1,camera["coordinates"]["z"]+2]
    normal_right = points_to_normal(p1,p2,p3, camera)
    p1 = [camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"]]
    p2 = [camera["coordinates"]["x"]-1,camera["coordinates"]["y"]+1,camera["coordinates"]["z"]+1]
    p3 = [camera["coordinates"]["x"]-2,camera["coordinates"]["y"]-1,camera["coordinates"]["z"]+2]
    normal_left = points_to_normal(p1,p2,p3,camera)

    # equises
    if point_two_angles[0] > MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_right
        point_two_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_two_angles
    if point_two_angles[0] < -MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_left
        point_two_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_two_angles
    if point_one_angles[0] > MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_right
        point_one_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_one_angles
    if point_one_angles[0] < -MAX_CAMERA_ANGLE:
        normal_vector_to_plane = normal_left
        point_one_angles = point_to_intersection(
            camera=camera,
            vector=normal_vector_to_plane,
            p1=point_one,
            p2=point_two
        ) or point_one_angles

    return point_one_angles, point_two_angles

def get_polygon_from_file(filename):

    filename += ".json"

    with open(filename,"r",encoding="UTF-8") as file_object:

        polygon = json.load(file_object)
    
        return polygon


ii = 0.01
# camera = 
CAMERA_ANGLE = 50
speed = .5
camera_total_inter_distance = math.tan(math.radians(CAMERA_ANGLE)) # * hipotenusa
camera = {
    "coordinates": {"x": 100, "y": 10, "z": 100},
    "angle": {"x":10,"y":0}
}

size = 10
ALLOWED_LOG = True
MAX_CAMERA_ANGLE = 45

polygons = []
# polygons.append( get_polygon_from_file("line") )
polygons.append( get_polygon_from_file("cube") )

for x in range(26):
    polygons.append( 
        {
            "coordinates": {"x": (x*size), "y": 0, "z": 0},
            "angles": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
            "points": [
                {"x": -1, "y": -1, "z": 0},
                {"x": 1, "y": -1, "z": 250}
            ],
            "relations": [
                [0,1]
            ]
        } 
    )
for x in range(26):
    polygons.append( 
        {
            "coordinates": {"x": 0, "y": 0, "z": (x*size)},
            "angles": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
            "points": [
                {"x": 0, "y": -1, "z": -1},
                {"x": 250, "y": -1, "z": 1}
            ],
            "relations": [
                [0,1]
            ]
        } 
    )

pygame.init()
screen = pygame.display.set_mode((height, width))
screen.fill(COLORS["background"])

font = pygame.font.SysFont(None, 24)


while True:

    if True:
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pygame.event.set_grab(True)
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0] or 1
        mouse_y = mouse[1] or 1
        mouse_x = 100 / ( width / mouse_x )
        mouse_y = 100 - ( 100 / ( height / mouse_y )) 
        max_angle = 180
        camera["angle"]["x"] =  -( ((max_angle*2)*(mouse_x/100))-max_angle )
        camera["angle"]["y"] =  -( ((max_angle*2)*(mouse_y/100))-max_angle )


    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LCTRL]:
        camera["coordinates"]["y"] -= speed
    if keys[pygame.K_SPACE]:
        camera["coordinates"]["y"] += speed
    if keys[pygame.K_a]:
        camera["coordinates"]["x"] -= speed
    if keys[pygame.K_d]:
        camera["coordinates"]["x"] += speed
    if keys[pygame.K_w]:
        camera["coordinates"]["z"] += speed
    if keys[pygame.K_s]:
        camera["coordinates"]["z"] -= speed
    for event in events:

        

        if event.type == pygame.KEYDOWN:

            ALLOWED_LOG = True
            
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


    screen.fill(COLORS["background"])
    img = font.render(str(str(camera["coordinates"]["x"])+","+str(camera["coordinates"]["y"])+","+str(camera["coordinates"]["z"])), True, (150,150,150))
    screen.blit(img, (10,10))


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


        polygon_screen = [worldscreenpoint__camera_point(
            camera["coordinates"]["x"], 
            camera["coordinates"]["y"], 
            camera["coordinates"]["z"], 
            point["x"],
            point["y"],
            point["z"],
            camera["angle"]["x"],
            camera["angle"]["y"]
        ) for point in coordinates]

        for i, r in enumerate(relations):

            point_one = coordinates[r[0]]
            point_two = coordinates[r[1]]
            point_one_angles = polygon_screen[r[0]]
            point_two_angles = polygon_screen[r[1]]
            x,y,z = rotate_3d_point(
                camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"], 
                -camera["angle"]["x"], -camera["angle"]["y"],
                point_one["x"], point_one["y"], point_one["z"]
            )
            point_one_rot = {"x":x,"y":y,"z":z}
            x,y,z = rotate_3d_point(
                camera["coordinates"]["x"], camera["coordinates"]["y"], camera["coordinates"]["z"], 
                -camera["angle"]["x"], -camera["angle"]["y"],
                point_two["x"], point_two["y"], point_two["z"]
            )
            point_two_rot = {"x":x,"y":y,"z":z}

            # si ambos puntos están detrás de la cámara, no renderizar
            if point_one_rot["z"] <= camera["coordinates"]["z"] and point_two_rot["z"] <= camera["coordinates"]["z"]:
                continue

            # si uno de los 2 puntos está detrás, mover el punto a la intersección
            if point_one_rot["z"] <= camera["coordinates"]["z"]:
                point_one_angles  = get_angles_from_depth_inter(point_one, point_two)
            if point_two_rot["z"] <= camera["coordinates"]["z"]:
                point_two_angles  = get_angles_from_depth_inter(point_one, point_two)


            # si ambos puntos de la linea, están fuera del rango de visión, continue
            if point_two_angles[1] < -MAX_CAMERA_ANGLE and point_one_angles[1] < -MAX_CAMERA_ANGLE:
                continue
            if point_two_angles[1] > MAX_CAMERA_ANGLE and point_one_angles[1] > MAX_CAMERA_ANGLE:
                continue
            if point_two_angles[0] < -MAX_CAMERA_ANGLE and point_one_angles[0] < -MAX_CAMERA_ANGLE:
                continue
            if point_two_angles[0] > MAX_CAMERA_ANGLE and point_one_angles[0] > MAX_CAMERA_ANGLE:
                continue

            #         if point_one_angles[0] < -MAX_CAMERA_ANGLE and point_one_angles[1] > MAX_CAMERA_ANGLE :

            #             # true = horizontal
            #             hor_ver = abs(point_one_angles[0]) > abs(point_one_angles[1])
                        
            #             if hor_ver:
            #                 point_one_angles, point_two_angles = get_angles_from_hor_inter(point_one_angles, point_two_angles)
            #             else:
            #                 point_one_angles, point_two_angles = get_angles_from_ver_inter(point_one_angles, point_two_angles)

            #         elif point_two_angles[0] < -MAX_CAMERA_ANGLE and point_two_angles[1] > MAX_CAMERA_ANGLE :

            #             hor_ver = abs(point_two_angles[0]) > abs(point_two_angles[1])

            #             if not hor_ver:
            #                 point_one_angles, point_two_angles = get_angles_from_hor_inter(point_one_angles, point_two_angles)
            #             else:
            #                 point_one_angles, point_two_angles = get_angles_from_ver_inter(point_one_angles, point_two_angles)


            # 
            point_one_angles, point_two_angles = get_angles_from_hor_inter(point_one_angles, point_two_angles)
            point_one_angles, point_two_angles = get_angles_from_ver_inter(point_one_angles, point_two_angles)

                

            point_one_percentage = angles_to_screenpoint(point_one_angles[0], point_one_angles[1])
            point_two_percentage = angles_to_screenpoint(point_two_angles[0], point_two_angles[1])
            
            xs = screenpoint__camera_point( point_one_percentage )
            ys = screenpoint__camera_point( point_two_percentage )

            # if i == 0:
            #     text = str(str(round(point["x"],1))+","+str(round(point["y"],1))+","+str(round(point["z"],1)))
            #     img = font.render(text, True, (150,150,150))
            #     screen.blit(img, xs)
            # if ((-10000 <= xs[0] <= 10000) and (-10000 <= xs[1] <= 10000)) and ((-10000 <= ys[0] <= 10000) and (-10000 <= ys[1] <= 10000)):
            pygame.draw.line(
                screen, 
                COLORS["edge"],
                xs,
                ys,
                2
            )

    ALLOWED_LOG = False

    # polygon["angles"]["x"] += 1
    # polygon["angles"]["y"] += 1
    # polygon["angles"]["z"] += 1


    sleep(0.05)


    pygame.display.flip()
