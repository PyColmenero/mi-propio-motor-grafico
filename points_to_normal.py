import numpy as np
import math

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

def points_to_normal(p1,p2,p3, camera):

    points = [p1,p2,p3]
    # print(points)
    for i, p in enumerate(points):

        y,z = rotate_point(
            camera["coordinates"]["y"], camera["coordinates"]["z"],
            camera["angle"]["y"],
            p[1],
            p[2]
        )
        x,z = rotate_point(
            camera["coordinates"]["x"], camera["coordinates"]["z"],
            camera["angle"]["x"],
            p[0],
            z
        )
        points[i] = (x,y,z)
    # print(points)
    p0, p1, p2 = points
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    ux, uy, uz = u = [x1-x0, y1-y0, z1-z0] #first vector
    vx, vy, vz = v = [x2-x0, y2-y0, z2-z0] #sec vector

    u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx] #cross product

    # point  = np.array(p1)
    normal = np.array(u_cross_v)

    return tuple(normal)

# p1 = [100,100,100]
# p2 = [101,98,101]
# p3 = [102,97,102]
# camera = {
#     "coordinates": {"x": 100, "y": 100, "z": 100},
#     "angle": {"x":-10,"y":0}
# }
# r = points_to_normal(p1,p2,p3, camera, False)

# print(r)