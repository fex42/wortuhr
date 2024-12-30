from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

front_th = 2.0 # thickness without diffusor
diffusor_th = 0.4 # diffusor thickness

led_dx = 16.6  # x distance of LEDs
led_dy = 18.94 # Y distance of LEDs

cnt_x = 11
cnt_y = 10

border = 42

size_x = 2*border + (cnt_x - 1) * led_dx
size_y = 2*border + (cnt_y - 1) * led_dy

wall_th = 1.2

cled_dx = led_dx * (cnt_x + 1)
cled_dy = led_dy * (cnt_y + 1)

grid_height = 10.0

corner_led_dia = 3

letters = iter(list(
    "ESKISTAFÜNF" + 
    "ZEHNZWANZIG" + 
    "DREIVIERTEL" + 
    "VORFUNKNACH" + 
    "HALBAELFÜNF" + 
    "EINSDCWZWEI" + 
    "DREIAUJVIER" + 
    "SECHSNLACHT" + 
    "SIEBENZWÖLF" + 
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

print(f"size_x = {size_x}") 
print(f"size_y = {size_y}")

show_object(result)