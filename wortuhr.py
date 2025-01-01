from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

front_th = 2.0 # thickness without diffusor
diffusor_th = 0.4 # diffusor thickness

led_dx = 16.6  # x distance of LEDs
led_dy = 18.94 # Y distance of LEDs

cnt_x = 2
cnt_y = 3

wall_th = 1.2
border = 0.2 + wall_th

size_x = 2*border + (cnt_x + 2) * led_dx + wall_th
size_y = 2*border + (cnt_y + 2) * led_dy + wall_th

cled_dx = led_dx * (cnt_x + 1)
cled_dy = led_dy * (cnt_y + 1)

grid_height = 10.0

corner_led_dia = 3

mag_dia = 8.2
mag_dep = 3.8
mag_dx = (cnt_x + 1) * led_dx
mag_dy = (cnt_y + 1) * led_dy

letters = iter(list(
    "x1234567890A" +
#    "ESKISTAFÜNF" + 
#    "ZEHNZWANZIG" + 
#    "DREIVIERTEL" + 
#    "VORFUNKNACH" + 
#    "HALBAELFÜNF" + 
#    "EINSDCWZWEI" + 
#    "DREIAUJVIER" + 
#    "SECHSNLACHT" + 
#    "SIEBENZWÖLF" + 
    "ZEHNEUNKUHR" ))

# Sunken letters and holes
result = Box(size_y, size_x, front_th + diffusor_th,
             align=(Align.CENTER, Align.CENTER, Align.MAX))
txt_pl = Plane(result.faces().sort_by(Axis.Z).last)

# Letters
letter_sk = Sketch() + [
    txt_pl * loc * Text(next(letters), 10, rotation=90)
    for loc in GridLocations(led_dy, led_dx, cnt_y, cnt_x)
]
result -= extrude(letter_sk, -front_th)

# Holes for corner LEDs
holes_sk = Sketch() + [
    txt_pl * loc * Circle(corner_led_dia/2)
    for loc in GridLocations(cled_dy, cled_dx, 2, 2)
]
result -= extrude(letter_sk + holes_sk, -front_th)

result = result.mirror(Plane.ZX)
# boxes for letters
lboxes_sk = Rectangle(wall_th + cnt_y * led_dy, wall_th + cnt_x * led_dx,
                         align=(Align.CENTER, Align.CENTER, Align.MIN)) - [
    loc * Rectangle(led_dy - wall_th, led_dx - wall_th)
    for loc in GridLocations(led_dy, led_dx, cnt_y, cnt_x)
]
result += extrude(lboxes_sk, grid_height)

# boxes for corner LEDs
cboxes_sk = Sketch() + [
    loc * Rectangle(led_dy + wall_th, led_dx + wall_th) 
    - loc * Rectangle(led_dy - wall_th, led_dx - wall_th)
    for loc in GridLocations(cled_dy, cled_dx, 2, 2)
]
result += extrude(cboxes_sk, grid_height)


# magnet sockets
mag_locations = Locations(
    (-mag_dy/2 , 0),
    (+mag_dy/2 , 0),
    (0, -mag_dx/2),
    (0, +mag_dx/2)
)
mag_sk = Sketch() + [
    loc * Rectangle(mag_dia + 2*wall_th, mag_dia + 2*wall_th)
    for loc in mag_locations
]
result += extrude(mag_sk, grid_height)

mag_pl = Plane.XY.offset(grid_height)
mag_sk = Sketch() + [
    mag_pl * loc * Circle(mag_dia/2)
    for loc in mag_locations
]
result -= extrude(mag_sk, -mag_dep)


print(f"size_x = {size_x}") 
print(f"size_y = {size_y}")

show_object(result)

filename = "wortuhr-front"
export_step(result, f"{filename}.step")
export_stl(result, f"{filename}.stl")
