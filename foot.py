from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

tol = 0.2

foot_l = 25.0 # foot length
foot_th = 3.5 # foot thickness
screw_h = 39.0 # screw height
stand_h = 44 # stand height
clock_th = 19.0 + tol # clock thichness (and tolerance)
nups_h = 2.0

width = 16.0
hole_dia = 3.9

pts = [
    (0, 0),
    (0, stand_h),
    (foot_th, stand_h),
    (foot_th, 0),
    (foot_th + foot_l, 0),
    (foot_th + foot_l, -foot_th),
    (-clock_th - foot_th - foot_l, -foot_th),
    (-clock_th - foot_th - foot_l, 0),
    (-clock_th - foot_th, 0),
    (-clock_th - foot_th, nups_h),
    (-clock_th, nups_h),
    (-clock_th, 0),
    (0, 0)
]

ln = Polyline(pts)

foot_sk = make_face(Plane.YZ * ln)
foot = extrude(foot_sk, -width).clean()

hole_sk = Plane.XZ * Pos(width/2, screw_h) * Circle(hole_dia/2)
foot -= extrude(hole_sk,-10)

show(foot)

filename = "wortuhr-foot"
export_step(foot, f"{filename}.step")
export_stl(foot, f"{filename}.stl")
