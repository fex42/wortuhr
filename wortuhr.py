from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from cadquery import *

front_th = 2.0
diffusor_th = 0.4 #- 0.4

led_dx = 16.6
led_dy = 18.94

cnt_x = 3 # 11
cnt_y = 3 # 10

size_x = 240 # 2*border + (cnt_x - 1) * led_dx
size_y = 240 # 2*border + (cnt_y - 1) * led_dy

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

# sunken letters
result = (Workplane("XY")
          .box(size_y, size_x, front_th + diffusor_th)
          .faces(">Z").workplane()
          .rarray(led_dy, led_dx, cnt_y, cnt_x)
          .eachpoint(lambda loc: (Workplane().workplane(offset=-diffusor_th)
                 .text(next(letters), 10, -front_th)
                 .rotate((0, 0, 1),(0, 0, 2), 90)
                 .val().moved(loc)), combine='s')
    )

# holes for corner LEDs
result = (result.rarray(cled_dy, cled_dx, 2, 2)
          .eachpoint(lambda loc: (Workplane().workplane(offset=-diffusor_th)
                                  .circle(corner_led_dia/2).extrude(-front_th)
                                  .val().moved(loc)), combine='s')
)


# boxes for letter LEDs
result = (result.faces("<Z").workplane()
          .rect(wall_th + cnt_y * led_dy, wall_th + cnt_x * led_dx)
          .rarray(led_dy, led_dx, cnt_y, cnt_x)
          .rect(led_dy - wall_th, led_dx - wall_th)
          .extrude(grid_height)
)

# boxes for corner LEDs
result = (result.rarray(cled_dy, cled_dx, 2, 2)
          .rect(led_dy - wall_th, led_dx - wall_th) # .extrude(10.0)
          .rect(led_dy + wall_th, led_dx + wall_th)
          .extrude(grid_height)
)

logger.info(f"size_x = {size_x}")
logger.info(f"size_y = {size_y}")

show(result)