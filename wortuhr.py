from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

front_th = 1.2 # thickness without diffusor
back_th = front_th # thickness of back
diffusor_th = 0.4 # diffusor thickness

led_dx = 16.6  # x distance of LEDs
led_dy = 18.94 # Y distance of LEDs

cnt_x = 2
cnt_y = 2

wall_th = 1.0
border = 0.2 + wall_th

size_x = 2*border + (cnt_x + 2) * led_dx + wall_th
size_y = 2*border + (cnt_y + 2) * led_dy + wall_th

cled_dx = led_dx * (cnt_x + 1)
cled_dy = led_dy * (cnt_y + 1)

grid_height = 10.0

corner_led_dia = 3

font_size = 12
font="FreeSans"
font_style = FontStyle.BOLD

mag_dia = 8.3
mag_dep = 3.8
mag_dx = (cnt_x + 1) * led_dx
mag_dy = (cnt_y + 1) * led_dy

led_stripe_w = 10.0
led_stripe_h = 2.0

letters = iter(list(
     "1234567890A" +
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


##########################################################
# Front
##########################################################

# Sunken letters and holes
front = Box(size_y, size_x, front_th + diffusor_th,
             align=(Align.CENTER, Align.CENTER, Align.MAX))
txt_pl = Plane(front.faces().sort_by(Axis.Z).last)

# Letters
letter_sk = Sketch() + [
    txt_pl * loc * Text(next(letters), font_size, font=font, font_style=font_style, rotation=90)
    for loc in GridLocations(led_dy, led_dx, cnt_y, cnt_x)
]
front -= extrude(letter_sk, -front_th)

# Holes for corner LEDs
holes_sk = Sketch() + [
    txt_pl * loc * Circle(corner_led_dia/2)
    for loc in GridLocations(cled_dy, cled_dx, 2, 2)
]
front -= extrude(letter_sk + holes_sk, -front_th)

front = front.mirror(Plane.ZX)
# boxes for letters
lboxes_sk = Rectangle(wall_th + cnt_y * led_dy, wall_th + cnt_x * led_dx,
                         align=(Align.CENTER, Align.CENTER, Align.MIN)) - [
    loc * Rectangle(led_dy - wall_th, led_dx - wall_th)
    for loc in GridLocations(led_dy, led_dx, cnt_y, cnt_x)
]
front += extrude(lboxes_sk, grid_height)

# boxes for corner LEDs
cboxes_sk = Sketch() + [
    loc * Rectangle(led_dy + wall_th, led_dx + wall_th) 
    - loc * Rectangle(led_dy - wall_th, led_dx - wall_th)
    for loc in GridLocations(cled_dy, cled_dx, 2, 2)
]
front += extrude(cboxes_sk, grid_height)


# magnet connectors
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
front += extrude(mag_sk, grid_height)

mag_pl = Plane.XY.offset(grid_height)
mag_sk = Sketch() + [
    mag_pl * loc * Circle(mag_dia/2)
    for loc in mag_locations
]
front -= extrude(mag_sk, -mag_dep)


print(f"size_x = {size_x}") 
print(f"size_y = {size_y}")

#show_object(front)

##########################################################
# Back
##########################################################

# magnet connectors
back = Box(size_y, size_x, back_th, 
           align=(Align.CENTER, Align.CENTER, Align.MAX))
mag_sk = Sketch() + [
    loc * (Rectangle(mag_dia + 2*wall_th, mag_dia + 2*wall_th) -
           Circle(mag_dia/2))
    for loc in mag_locations
]
back += extrude(mag_sk, mag_dep)

# letter LED stripes

base_sk = Rectangle(cnt_y * led_dy, cnt_x * led_dx)
back += extrude(base_sk, mag_dep)

plane = Plane.XY.offset(mag_dep)
cs = plane * Circle(10)

stripes_sk = Sketch() + [
    plane * loc * Rectangle(led_stripe_w + 0.2, cnt_x * led_dx)
    for loc in GridLocations(led_dy, led_dx, cnt_y, 1)
]

back -= extrude(stripes_sk, -led_stripe_h)

# corner LEDs

show(back)

filename = "wortuhr-front"
export_step(front, f"{filename}.step")
export_stl(front, f"{filename}.stl")
